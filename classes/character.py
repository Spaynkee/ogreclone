""" character.py

This class represents a single character.

"""
from .knight import KnightClass
class Character():
    # class
    # stats - Str, agi, int, wis, const, alignment 
    # derived stats
    def __str__(self):
        return f"{self.char_name}\nMax HP: {self.health}\nAgi: {self.agility}\n"

    def __init__(self, name="", health=0, agility=0, strength=0, char_id=-1):
        # do we need props for base stats so we can lower then mid-fight and restore them after?
        self.char_name = name
        self.char_id = char_id
        self.unit_id = -1
        self.max_health = health
        self.health = self.max_health
        self.agility = agility
        self.strength = strength
        self.base_position = 0
        self.current_position = 0
        self.is_dead = False
        self.has_performed_action_this_round = False
        self.status = None # what var type should this be?
        self.char_class = KnightClass()

    def get_action_by_row(self, row):
        return self.char_class.actions[row]

    def num_actions(self, pos):
        row = 0
        if pos >= 3 and pos <= 5:
            row = 1
        elif row >= 6:
            row = 2

        return self.char_class.num_actions[row]

    def determine_target(self, unit, action):
        # for now, return the first char in the unit. We have way too much untested code that we
        # need to ensure works. so pause new functionality here.
        return unit.get_first_non_dead_char_in_unit()

        # if our charcter is on one side, get chars for that side and the middle.
        # if none, get chars from the third row

        # if our char is in the middle, get a list of all chars.

        # if action.targets_front:

        # returns a char that we're attacking.
