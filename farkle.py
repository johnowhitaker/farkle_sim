import random
import sys

# This method can be tweaked for testing
def dice(n): # Returns n dice numbers (totally random) - tested
    return [random.randint(1, 6) for i in range(n)]


# Some tests for different scoring combos:
def test_for_two_3s(roll):
    return False

def unique(roll):
    u = []
    for r in roll:
        if r not in u:
            u.append(r)
    return u

def test_for_3oak(roll):
    u = unique(roll)
    for r in u:
        if roll.count(r) >= 3: # <<<<<<<<<< cases with >3 handled by player
            return True, r
    return False, 0

def test_for_3pairs(roll):
    u = unique(roll)
    twos = 0
    for r in u:
        if roll.count(r) == 2:
            twos += 1
    if twos == 3:
        return True
    return False

def test_for_23s(roll):
    u = unique(roll)
    threes = 0
    for r in u:
        if roll.count(r) == 3:
            threes += 1
    if threes == 2:
        return True
    return False

def test_for_run(roll):
    if len(unique(roll)) == 6:
        return True
    return False

# This is the base class, that implements a simple player who keeps 1s and 5s and rolls again if they have 3 or more dice left.
# To build a more complex player, one simply adds a child class and overrides the process_roll function.
class BasicPlayer:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.temp_score = 0
        self.keeping = []

    def process_roll(self, roll):
        # Knows temp score, score and current roll. Adds dice to self.keeping and optionally rolls again.
        # Returns: (roll_again (bool), fail (bool - true if no points scored))
        # Go through dice looking for high scoring patterns << Add patterns
        self.kept = 0 # How many dice kept (must be at least 1 else turn ends)
        for d in roll:
            if d == 1:
                self.keeping.append(1)
                self.kept += 1
                self.temp_score += 100
            if d == 5:
                self.keeping.append(5)
                self.kept += 1
                self.temp_score += 50
        if (self.kept) == 0:
            return (False, True) # Scored no points this roll
        elif len(self.keeping) > 3:
            return (False, False) # Scored points, 2 or fewer dice remain (so don't roll again)
        else:
            return (True, False) # Scored points, and there are 3 or more dice to play with - recomment roll again.

    def turn(self, verbose=False):
        # Reset some variables
        self.temp_score = 0
        self.keeping = []
        # Roll the dice
        roll = dice(6)
        if verbose:print('Player %s: rolled ' % self.name + str(roll))
        # Process the roll. If roll_again is true, keep rolling until it isn't or a roll fails
        roll_again, fail = self.process_roll(roll)
        if fail:
            if verbose:print('     - %s: No points this roll, total score: ' % self.name + str(self.score))
            self.temp_score = 0
        elif roll_again:
            while roll_again:
                if verbose:print('     - %s: Keeping ' % self.name + str(self.keeping) + ' for temp_score of ' + str(self.temp_score) + ', total score: ' + str(self.score))
                # If all 6 used must roll again, with 6 dice (so empty keeping)
                if len(self.keeping) == 6:
                    self.keeping = []
                roll = dice(6 - len(self.keeping))
                if verbose:print('     - %s: rolled ' % self.name + str(roll))
                roll_again, fail = self.process_roll(roll)
                if fail:
                    if verbose:print('     - %s: No points this roll, total score: ' % self.name + str(self.score))
                    self.temp_score = 0
                # Otherwise, roll_again determines how many times this loop runs
        # Update the score - turn has ended.
        self.score += self.temp_score
        if verbose:print('     - %s: Turn over. ' % self.name + 'Kept:'+ str(self.keeping) + ', turn score:' + str(self.temp_score) + ', total score: ' + str(self.score))



class AllRules(BasicPlayer):

    def pull_highs(self, roll):
        # 2 3OAKS
        if test_for_23s(roll):
            for d in roll:
                self.keeping.append(d)
                roll.remove(d)
                self.kept += 1
                self.temp_score += 2500

        # 3 pairs:
        if test_for_3pairs(roll):
            for d in roll:
                self.keeping.append(d)
                roll.remove(d)
                self.kept += 1
                self.temp_score += 2000

        # Run (1, 2, 3, 4, 5, 6)
        if test_for_run(roll):
            for d in roll:
                self.keeping.append(d)
                roll.remove(d)
                self.kept += 1
                self.temp_score += 1500
        return roll

    def pull_3oak(self, roll):
        # 3oak:
        thr, num = test_for_3oak(roll)
        if thr:
            for n in [num, num, num]:
                self.keeping.append(num)
                roll.remove(num)
                self.kept += 1
            s = num*100 # The score for this
            if num == 1: s = 1000 # one is a special case
            # If there are any extras of that number (more than three total), we double the score for each
            while roll.count(num) > 0:
                self.keeping.append(num)
                roll.remove(num)
                self.kept += 1
                s = s*2
            self.temp_score += s
        return roll


    def process_roll(self, roll):
        # Knows temp score, score and current roll. Adds dice to self.keeping and optionally rolls again.
        # Returns: (roll_again (bool), fail (bool - true if no points scored))
        # Go through dice looking for high scoring patterns << Add patterns
        self.kept = 0 # How many dice kept (must be at least 1 else turn ends)

        roll = self.pull_highs(roll)

        roll = self.pull_3oak(roll)


        # 1s and 5s:
        for d in roll:
            if d == 1:
                self.keeping.append(1)
                self.kept += 1
                self.temp_score += 100
            if d == 5:
                self.keeping.append(5)
                self.kept += 1
                self.temp_score += 50


        if (self.kept) == 0:
            return (False, True) # Scored no points this roll
        if len(self.keeping) == 6:
            return (True, False) # Used all 6 dice - must roll again
        elif len(self.keeping) > 3:
            return (False, False) # Scored points, 2 or fewer dice remain (so don't roll again)
        else:
            return (True, False) # Scored points, and there are 3 or more dice to play with - recomment roll again.

class AllRulesThreshForThreeOne(AllRules):

    def __init__(self, name, thresh3, thresh1):
        self.name = name
        self.score = 0
        self.temp_score = 0
        self.keeping = []
        self.thresh3 = thresh3
        self.thresh1 = thresh1

    def process_roll(self, roll):
        self.kept = 0

        roll = self.pull_highs(roll)

        roll = self.pull_3oak(roll)


        # 1s and 5s:
        for d in roll:
            if d == 1:
                self.keeping.append(1)
                self.kept += 1
                self.temp_score += 100
            if d == 5:
                self.keeping.append(5)
                self.kept += 1
                self.temp_score += 50


        if (self.kept) == 0:
            return (False, True) # Scored no points this roll
        if len(self.keeping) == 6:
            return (True, False) # Used all 6 dice - must roll again
        elif len(self.keeping) == 5 and self.temp_score > self.thresh1:
            return (True, False) # One dice left - risk it for the brisket
        elif len(self.keeping) > 3:
            return (False, False) # Scored points, 2 or fewer dice remain (so don't roll again)
        elif len(self.keeping) == 3 and self.temp_score > self.thresh3:
            return (False, False) # Don't roll with 3 left if score is above thresh
        else:
            return (True, False) # Scored points, and there are 3 or more dice to play with - recomment roll again.



def score_player(player, n_rounds):
    for i in range(n_rounds):
        player.turn()

    return(player.score/float(n_rounds))


# p4 = AllRules('All Rules')
# score = score_player(p4, 20000)
# print(score)



# for t in [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
#     p5 = AllRulesThreshForThree('3thresh', t)
#     score = score_player(p5, 200000)
#     print(score)


# for t in [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
#     p5 = AllRulesThreshForThreeOne('3thresh', 500, t)
#     score = score_player(p5, 20000)
#     print(score)

p6 =
