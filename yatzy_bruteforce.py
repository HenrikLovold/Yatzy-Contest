from game import Game
from itertools import product, chain, combinations
import time

class BotGame:

    def __init__(self):
        self.game = Game(forcedMode=False)

    def playGame(self):
        while not self.game.isFinished():
            self.playRound()
        self.printFinalResults()

    def playRound(self):

        # First roll
        dice = self.game.rollDice()
        print("First roll:", dice)
        keep = self.getBestMove(dice, self.game.possibleMoves())
        print("keeping", keep)

        # Second roll
        dice = self.game.rollDice(dice=dice, keep=keep)
        print("Second roll:", dice)
        keep = self.getBestMove(dice, self.game.possibleMoves())
        print("keeping", keep)

        # Third roll
        dice = self.game.rollDice(dice=dice, keep=keep)
        print("Third roll:", dice)

        for c in self.game.possibleMoves():
            print(c)
        choice, score = self.evaluateMaxScore(dice, self.game.possibleMoves())
        print("--------")
        print("Bot choice:", choice)
        print("--------")

        time.sleep(1)
        self.game.registerRound(dice, choice)

        print(self.game)

    def printFinalResults(self):
        print("\nFINAL RESULT:")
        print(self.game)
        print("YOU SCORED:", self.game.getScore(), "POINTS!")

    
    def powerset(self, iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


    def getBestMove(self, dice: list, possible_moves: dict) -> list:
        """
        Finds which dice is best to keep
        """
        best = 0
        best_keep = []
        for replacement in self.powerset(range(5)): 
            score = self.testPossiblePermutations(dice, possible_moves, replacement)
            if score > best:
                best = score
                best_keep = list(set(range(5)) - set(replacement))

        return best_keep

    def testPossiblePermutations(self, dice:list, possible_moves: dict, change_idx: list):
        """
        Calculates a possible score based on what indexes should be changed.

        Returns the sum of score * probability_of_happening
        """

        possible_dice = product(range(0, 6), repeat=len(change_idx))

        total = 0
        for possible in possible_dice:
            new_dice = dice.copy()
            for i, change in enumerate(change_idx):
                new_dice[change] = possible[i]

            _, score = self.evaluateMaxScore(new_dice, possible_moves)
            total += score * ((1/6) ** len(change_idx))

        return total



    def evaluateMaxScore(self, dice: list, possible_moves: dict):
        """
        Finds the optimal move and corresponding score
        """

        table = self.game.buildTable()
        values = {}

        for move, func in table.items():
            if move not in possible_moves:
                continue
            if move in self.game.enumList[:6]:
                values[move] = func(dice, move)
            else:
                values[move] = func(dice)

        best_move = max(values, key=lambda k: values[k])
        return best_move, values[best_move]


if __name__ == "__main__":
    g = BotGame()
    g.playGame()