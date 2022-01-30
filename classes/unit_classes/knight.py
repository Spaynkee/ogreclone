""" knight.py

contains all the info for the knight class.

"""
from ..actions.slash_action import SlashAction
class KnightClass():

    #
    def __init__(self):
        self.class_id = 1
        # includes how many stats per level
        # incldes promition requirements
        # set the actions here, the actions themselves are calculated on the fly?
        self.actions = {0: SlashAction(), 1: SlashAction(), 2: SlashAction()}

        # front, middle, back.
        self.num_actions = {0: 2, 1: 1, 2: 1}


