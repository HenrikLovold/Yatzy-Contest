import random

class Game:

    """
    This class represents a single game of Yatzy. The public interface
    is as follows (other methods just used internally):

    rollDice
    registerRound
    getScore
    isFinished
    possibleMoves
    possibleMovesNumeric
    numericMoveToStr
    regiserRoundNumeric
    """

    def __init__(self, forcedMode=True):
        """
        Construct a new Game object

        :param forcedMode: specifies the turn of events in the game
        """
        self.forcedMode = forcedMode
        self.progression = 0
        self.score = 0
        self.bonus = 0
        self.enumList = self.buildEnumList()
        self.table = self.buildTable()
        self.finished = False

    def rollDice(self, dice=[], keep=[]):
        """
        Roll the dices once (called three times per round)

        :param dice: the dices to be rolled, if unspecified you get new random dices
        :param keep: list of dice indices to keep (ie. not reroll)
        """
        if not dice:
            for i in range(5):
                dice.append(random.randint(1, 6))
        else:
            for i in range(len(dice)):
                if i not in keep:
                    dice[i] = random.randint(1, 6)
        return dice

    def registerRound(self, dice, ref):
        """
        Registers that a round has passed, and runs function to check how
        many points the dices give, given the place in the table that the user
        selects (or is forced to select)

        :param dice: the dices to be evaluated
        :param ref: which index in the table to fill (specified as string)
        """
        self.progression += 1
        if ref in self.enumList[0:6]:
            self.table[ref] = self.table[ref](dice, ref)
        else:
            self.table[ref] = self.table[ref](dice)
        self.updateScores()
        if self.progression == len(self.table):
            self.finished = True

    def getScore(self):
        """
        Returns the current score
        """
        return self.score

    def isFinished(self):
        """
        Returns whether or not the game is finished
        """
        return self.finished

    def possibleMoves(self):
        """
        Returns a list of the possible moves as strings
        """
        moves = []
        for move in self.table:
            if type(self.table[move]) != int:
                moves.append(move)
        return moves

    def possibleMovesNumeric(self):
        """
        Returns a list of possible moves as ints (corresponding to the enumerated list)
        """
        moves = []
        for move in self.table:
            if type(self.table[move]) != int:
                moves.append(self.enumList.index(move))
        return moves

    def numericMoveToStr(self, num):
        """
        Takes a numeric move (according to enumerated list), and returns a
        string corresponding to the move at this number

        :param num: the numeric representation of the selected move
        """
        return self.enumList[num]

    def registerRoundNumeric(self, dice, num):
        """
        Same as register round, just with an integer representing move (AI practical)

        :param dice: the dices to be evaluated
        :param num: the numeric representation of the selected move
        """
        self.registerRound(dice, self.numericMoveToStr(num))
    
    def updateScores(self):
        """
        Updates the scoreboard.
        Internal method (should be private)
        """
        s = 0
        if self.forcedMode:
            lim = 41
        else:
            lim = 63
        for score in self.table:
            if type(self.table[score]) == int and score in self.enumList[0:6]:
                s += self.table[score]
        if s >= lim:
            self.bonus = 50
            s += 50
        for score in self.table:
            if type(self.table[score]) == int and score not in self.enumList[0:6]:
                s += self.table[score]
        self.score = s

    def simples(self, dice, val):
        """
        Internal method evaluating dices for choices 1-6

        :param dice: the dices to be evaluated
        :param val: 1 through 6, depending on value being evaluated
        """
        val = {"ones": 1, "twos": 2, "threes": 3, "fours": 4, "fives": 5, "sixes": 6}[val]
        s = 0
        for d in dice:
            if d == val:
                s += d
        return s

    def one_pair(self, dice):
        """
        Internal method evaluating dices for one pair

        :param dice: the dices to be evaluated
        """
        pairs = []
        for i in range(len(dice)):
            for j in range(len(dice)):
                if i != j and dice[i] == dice[j]:
                    pairs.append(dice[i])
        if pairs:
            return max(set(pairs))*2
        return 0

    def two_pairs(self, dice):
        """
        Internal method evaluating dices for two pairs

        :param dice: the dices to be evaluated
        """
        pairs = []
        for i in range(len(dice)):
            for j in range(len(dice)):
                if i != j and dice[i] == dice[j]:
                    pairs.append(dice[i])
        pairs = [x for x in set(pairs)]
        if len(pairs) > 1:
            return pairs[0]*2 + pairs[1]*2
        return 0

    def three_eq(self, dice):
        """
        Internal method evaluating dices for three equal

        :param dice: the dices to be evaluated
        """
        for i in range(len(dice)):
            cnt = 0
            for j in range(len(dice)):
                if i != j and dice[i] == dice[j]:
                    cnt += 1
            if cnt == 2:
                return dice[i] * 3
        return 0

    def four_eq(self, dice):
        """
        Internal method evaluating dices for four equal

        :param dice: the dices to be evaluated
        """
        for i in range(len(dice)):
            cnt = 0
            for j in range(len(dice)):
                if i != j and dice[i] == dice[j]:
                    cnt += 1
            if cnt == 3:
                return dice[i] * 3
        return 0

    def small_straight(self, dice):
        """
        Internal method evaluating dices for small straight

        :param dice: the dices to be evaluated
        """
        return 15 if set(dice) == set([1, 2, 3, 4, 5]) else 0
    
    def big_straight(self, dice):
        """
        Internal method evaluating dices for big straight

        :param dice: the dices to be evaluated
        """
        return 20 if set(dice) == set([2, 3, 4, 5, 6]) else 0

    def house(self, dice):
        """
        Internal method evaluating dices for house

        :param dice: the dices to be evaluated
        """
        alternatives = {}
        score = 0
        for d in dice:
            if d in alternatives.keys():
                alternatives[d] += 1
            else:
                alternatives[d] = 1
        if len(alternatives) == 2:
            for k in alternatives.keys():
                score += k * alternatives[k]
        return score

    def chance(self, dice):
        """
        Internal method evaluating dices for chance

        :param dice: the dices to be evaluated
        """
        return sum(dice)

    def yatzy(self, dice):
        """
        Internal method evaluating dices for yatzy

        :param dice: the dices to be evaluated
        """
        num = dice[0]
        for e in dice:
            if e != num:
                return 0
        return 50

    def buildEnumList(self):
        """
        Internal, called by constructor
        Builds the enumerated list of moves, practical for calculating indices
        of string represented moves.
        """
        moves = \
        ["ones",
        "twos",
        "threes",
        "fours",
        "fives",
        "sixes",
        "one_pair",
        "two_pairs",
        "three_eq",
        "four_eq",
        "small_straight",
        "big_straight",
        "house",
        "chance",
        "yatzy"]
        return moves

    def buildTable(self):
        """
        Internal: Builds the table of possible moves, quite nifty using
        references to methods, and changing them to ints (scores)
        whenever they are evaluated!
        """
        table = {}
        table["ones"] = self.simples
        table["twos"] = self.simples
        table["threes"] = self.simples
        table["fours"] = self.simples
        table["fives"] = self.simples
        table["sixes"] = self.simples
        table["one_pair"] = self.one_pair
        table["two_pairs"] = self.two_pairs
        table["three_eq"] = self.three_eq
        table["four_eq"] = self.four_eq
        table["small_straight"] = self.small_straight
        table["big_straight"] = self.big_straight
        table["house"] = self.house
        table["chance"] = self.chance
        table["yatzy"] = self.yatzy
        return table

    def __str__(self):
        """
        Just your average __str__ method
        """
        s = "\nCurrent board:\n"
        for move in self.table:
            if type(self.table[move]) == int:
                s += "{0:20} {1:<18}".format(move, self.table[move])
            else:
                s += "{0:20} {1:<18}".format(move, "-")
            s += "\n"
            if move == "sixes":
                s += "--------\n"
                s += "{0:20} {1:<18}".format("Bonus", self.bonus)
                s += "\n--------\n"
        s += "--------\n"
        s += "{0:20} {1:<18}".format("Current sum", self.getScore())
        s += "\n"
        return s
