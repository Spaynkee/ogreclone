""" slash_action.py

each one of these objects contains a collection of actions a unit can take?

"""
class SlashAction():

    def __str__(self):
        return f"{self.description}"

    def __init__(self):
        self.damage = 0
        self.targets_front = True
        self.targets_back = False
        self.description = "Slash"

    def get_damage(self, char):
        # this changes the damage of an action
        return char.strength


