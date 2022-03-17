""" slash_action.py

each one of these objects contains a collection of actions a unit can take?

"""
import random

class SlashAction():
    """ Contains all the properties and methods of a Slash action.
        The slash action is a basic attacking action. Similar to Crush or Thrust.

        Attributes:
            damage (int): An integer denoting the damage of the action.
            targets_back (bool): Does this action target the rear row of the unit?
            description (string): The description of the action.

        TODO:
            I think we can make a basic attack_action and inherit all of its propertys, then
            just override the get_damage function for each action?

    """

    def __str__(self):
        return f"{self.description}"

    def __init__(self):
        self.damage = 0
        self.targets_back = False
        self.description = "Slash"
        self.crit_rate = .1 # this may be a calculation based on dex at some point.
        self.can_crit = True

    @staticmethod
    def get_damage(char, is_crit) -> int:
        """ Calculates the damage of this action based on some stats.

            Args:
                char (Character): The character object using this action

            Returns:
                An integer denoting the raw damage of this action.

        """
        if is_crit:
            return char.strength * 2

        return char.strength

    def determine_crit(self, char) -> bool:
        """ Determines if we got a crit or not.

            Args:
                char (Character): The character object we determine a critical hit for.

            Returns:
                A boolean indicating if this action is a critical hit.
        """
        char_crit_chance = self.crit_rate + char.agility / 100
        crit_roll = random.random()
        if crit_roll <=  char_crit_chance:
            return True

        return False
