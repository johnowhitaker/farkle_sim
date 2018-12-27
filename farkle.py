import random
import sys

# This method can be tweaked for testing
def dice(n): # Returns n dice numbers (totally random) - tested
    return [random.randint(1, 6) for i in range(n)]

class Player:
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
        self.temp_score = 0
        roll = dice(6)
        if verbose:print('Player %s: rolled ' % self.name + str(roll))
        self.keeping = []

        roll_again, fail = self.process_roll(roll)
        if fail:
            if verbose:print('     - %s: No points this roll, total score: ' % self.name + str(self.score))
            self.temp_score = 0
        elif roll_again:
            while roll_again:
                if verbose:print('     - %s: Keeping ' % self.name + str(self.keeping) + ' for temp_score of ' + str(self.temp_score) + ', total score: ' + str(self.score))
                roll = dice(6 - len(self.keeping))
                if verbose:print('     - %s: rolled ' % self.name + str(roll))
                roll_again, fail = self.process_roll(roll)
                if fail:
                    if verbose:print('     - %s: No points this roll, total score: ' % self.name + str(self.score))
                    self.temp_score = 0
                # Otherwise, roll_again determines how many times this loop runs

        self.score += self.temp_score



def score_player(player, n_rounds):
    for i in range(n_rounds):
        p.turn()

    return(p.score/float(n_rounds))



# print(dice(50))

p = Player('test')
score = score_player(p, 20)
print(score)

p.score = 0
p.turn(verbose=True)
