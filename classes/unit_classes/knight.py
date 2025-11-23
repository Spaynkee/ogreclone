"""knight.py

contains all the info for the knight class.

"""

# pylint: disable=relative-beyond-top-level # it's fine for now.
# pylint: disable=too-few-public-methods # This is fine.
from ..actions.slash_action import SlashAction
from .base_class import BaseClass


class KnightClass(BaseClass):
    """The knight is a basic melee class with average and balanced stats.

    Attributes:
        class_id (int): The id associated with this class.
        actions (dict): A dict containing the type of actions this char
            will take. The key represents the row, so key=0 means in the front, the character
            will take this action.

        stats_per_level (dict): A dict containing the stats per level a character of this class will gain.
        num_actions (dict): A dict containing the number of actions this character
            will get. The key represents the row, so key=0 means in the front, the character
            will take this many actions.

    """

    def __init__(self):
        self.class_id = 1
        self.class_name = "Knight"
        self.actions = {0: SlashAction(), 1: SlashAction(), 2: SlashAction()}
        self.stats_per_level = {
            "max_health": 10,
            "agility": 3,
            "strength": 3,
            "vitality": 3,
            "wisdom": 3,
            "intelligence": 2,
        }

        # front, middle, back.
        self.num_actions = {0: 2, 1: 1, 2: 1}
