"""berserker.py

contains all the info for the berserker class.

"""

# pylint: disable=relative-beyond-top-level # it's fine for now.
# pylint: disable=too-few-public-methods # This is fine.
from ..actions.crush_action import CrushAction
from base_class import BaseClass


class berserkerClass(BaseClass):
    """Contains all the properties and methods of the berserker class
    The berserker is a melee class with slightly higher offence than defense..

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
        self.class_id = 2
        self.actions = {0: CrushAction(), 1: CrushAction(), 2: CrushAction()}
        self.stats_per_level = {
            "health": 15,
            "agility": 3,
            "strength": 4,
            "vitality": 2,
            "wisdom": 2,
            "intelligence": 1,
        }

        # front, middle, back.
        self.num_actions = {0: 2, 1: 1, 2: 1}
