""" base_class.py

contains all the info for a base class. Other classes should eventually extend this, probably?

"""
#pylint: disable=relative-beyond-top-level # it's fine for now.
#pylint: disable=too-few-public-methods # This is fine.
from ..actions.slash_action import SlashAction
class BaseClass():
    """ Contains all the properties and methods of a base class.
        This class really shouldn't be used unless something goes wrong I think.
        Perhaps other classes will inherit or extend this class, but I'm not sure right now.

        Attributes:
            class_id (int): The id associated with this class.
            actions (dict): A dict containing the type of actions this char
                will take. The key represents the row, so key=0 means in the front, the character
                will take this action.

            num_actions (dict): A dict containing the number of actions this character
                will get. The key represents the row, so key=0 means in the front, the character
                will take this many actions.

    """

    #
    def __init__(self):
        self.class_id = 0
        # includes how many stats per level
        # incldes promition requirements
        # set the actions here, the actions themselves are calculated on the fly?
        self.actions = {0: SlashAction(), 1: SlashAction(), 2: SlashAction()}

        # the key in dict is the row index. Front, Middle, Back
        self.num_actions = {0: 1, 1: 1, 2: 1}
