from game import Game

class ManualGame:

    def __init__(self):
        forced = True if input("Play forced? [y/N]: ") == "y" else False
        self.game = Game(forcedMode=forced)

    def playGame(self):
        while not self.game.isFinished():
            self.playRound()
        self.printFinalResults()

    def playRound(self):
        if self.game.forcedMode:
            print("Game is forced, you are rolling for:", self.game.enumList[self.game.progression])
        # First roll
        dice = self.game.rollDice()
        print("First roll:", dice)
        keep = input("Keep dices? Type indexes 1 through 5 (comma separated): ")
        keep = [int(x)-1 for x in keep.split(",")] if keep else []

        # Second roll
        dice = self.game.rollDice(dice=dice, keep=keep)
        print("Second roll:", dice)
        keep = input("Keep dices? Type indexes 1 through 5 (comma separated): ")
        keep = [int(x)-1 for x in keep.split(",")] if keep else []

        # Third roll
        dice = self.game.rollDice(dice=dice, keep=keep)
        print("Third roll:", dice)

        if not self.game.forcedMode:
            print("Where do you want to place the result? Possible:\n")
            for c in self.game.possibleMoves():
                print(c)
            choice = input("\nChoice: ")
            self.game.registerRound(dice, choice)
        else:
            self.game.registerRound(dice, self.game.enumList[self.game.progression])

        print(self.game)

    def printFinalResults(self):
        print("\nFINAL RESULT:")
        print(self.game)
        print("YOU SCORED:", self.game.getScore(), "POINTS!")


if __name__ == "__main__":
    g = ManualGame()
    g.playGame()
