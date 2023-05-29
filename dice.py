import random


class Dice:
    type = "dice"

    def __init__(self, faces=6):
        self.faces = faces

    def __str__(self):
        return f"A {type(self).type} with {self.faces} faces !"

    def roll(self):
        return random.randint(1, self.faces)


class WoodDice(Dice):
    type = "wood dice"


class RiggedDice(Dice):
    type = "rigged dice"

    def roll(self, rigged=False):
        return super().roll() if not rigged else self.faces


if (__name__ == "__main__"):
    pass
