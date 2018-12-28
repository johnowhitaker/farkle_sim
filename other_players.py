class ThreeOAKBasic(BasicPlayer):
    def process_roll(self, roll):
        # Knows temp score, score and current roll. Adds dice to self.keeping and optionally rolls again.
        # Returns: (roll_again (bool), fail (bool - true if no points scored))
        # Go through dice looking for high scoring patterns << Add patterns
        self.kept = 0 # How many dice kept (must be at least 1 else turn ends)

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

        # 3oak:
        thr, num = test_for_3oak(roll)
        if thr:
            for n in [num, num, num]:
                self.keeping.append(num)
                roll.remove(num)
            s = num*100 # The score for this
            if num == 1: s = 1000 # one is a special case
            s = s*(2**roll.count(num)) # If there are any extras of that number (more than three total), we double the score for each
            self.temp_score += s
            self.kept += 3


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
        elif len(self.keeping) > 3:
            return (False, False) # Scored points, 2 or fewer dice remain (so don't roll again)
        else:
            return (True, False) # Scored points, and there are 3 or more dice to play with - recomment roll again.

class ThreeOAKBasicG2(BasicPlayer): # Same as 3OAK but doesn't keep 2s
    def process_roll(self, roll):
        # Knows temp score, score and current roll. Adds dice to self.keeping and optionally rolls again.
        # Returns: (roll_again (bool), fail (bool - true if no points scored))
        # Go through dice looking for high scoring patterns << Add patterns
        self.kept = 0 # How many dice kept (must be at least 1 else turn ends)

        # 3oak:
        thr, num = test_for_3oak(roll)
        if (thr) and (num not in [2]):
            for n in [num, num, num]:
                self.keeping.append(num)
                roll.remove(num)
            if num == 1: self.temp_score += 1000
            else: self.temp_score += num*100
            self.kept += 3


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
        elif len(self.keeping) > 3:
            return (False, False) # Scored points, 2 or fewer dice remain (so don't roll again)
        else:
            return (True, False) # Scored points, and there are 3 or more dice to play with - recomment roll again.
