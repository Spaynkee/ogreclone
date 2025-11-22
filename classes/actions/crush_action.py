"""crush_action.py

each one of these objects contains an action a unit can take?

"""

from .base_melee_action import BaseMeleeAction


class CrushAction(BaseMeleeAction):
    """Contains all the properties and methods of a crush action.
    The crush action is a basic attacking action. Similar to Slash or Thrust
    with a slight additional crit rate.

    Attributes:
        damage (int): An integer denoting the damage of the action.
        targets_back (bool): Does this action target the rear row of the unit?
        description (string): The description of the action.

    """

    def __str__(self):
        return f"{self.description}"

    def __init__(self):
        super().__init__()
        self.description = "crush"
        self.crit_rate = 0.15
