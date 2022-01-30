""" base_class.py

contains all the info for a base class. Other classes should eventually extend this, probably?

"""
from ..actions.slash_action import SlashAction
class BaseClass():

    #
    def __init__(self):
        self.class_id = 0
        # includes how many stats per level
        # incldes promition requirements
        # set the actions here, the actions themselves are calculated on the fly?
        self.actions = {0: SlashAction(), 1: SlashAction(), 2: SlashAction()}

        # the key in dict is the row index. Front, Middle, Back
        self.num_actions = {0: 1, 1: 1, 2: 1}


