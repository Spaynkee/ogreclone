""" slash_action.py

each one of these objects contains a collection of actions a unit can take?

"""
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

    @staticmethod
    def get_damage(char) -> int:
        """ Calculates the damage of this action based on some stats.

            Args:
                char (Character): The character object using this action

            Returns:
                An integer denoting the raw damage of this action.

        """
        # this changes the damage of an action
        return char.strength
