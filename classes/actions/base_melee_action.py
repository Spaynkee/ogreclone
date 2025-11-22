"""base_melee_action.py"""

import random


class BaseMeleeAction:
    """Contains all the properties and methods of a base melee action.

    Attributes:
        targets_back (bool): Does this action target the rear row of the unit?
        description (string): The description of the action.
        crit_rate (float): The base crit rate for this action

    """

    def __str__(self):
        return f"{self.description}"

    def __init__(self):
        self.targets_back = False
        self.description = "Base melee action"
        self.crit_rate = 0.1

    @staticmethod
    def get_damage(char, target, is_crit) -> int:
        """Calculates the damage of this action based on some stats.

        Args:
            char (Character): The character object using this action

        Returns:
            An integer denoting the raw damage of this action.

        """
        if is_crit:
            return max(char.strength * 2 - target.vitality, 1)

        return max(char.strength - target.vitality, 1)

    def determine_crit(self, char) -> bool:
        """Determines if we got a crit or not.

        Args:
            char (Character): The character object we determine a critical hit for.

        Returns:
            A boolean indicating if this action is a critical hit.

        Example:
            A knight using crush and having an agility of 150
            -> .1 + (150/1000) = .25
        """
        char_crit_chance = self.crit_rate + (char.agility / 1000)
        crit_roll = random.random()
        if crit_roll <= char_crit_chance:
            return True

        return False
