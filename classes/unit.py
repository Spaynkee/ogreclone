""" unit.py

contains the class representing a unit. A unit consists of 9 tiles with a position assigned to each.

Front
0 1 2
3 4 5
6 7 8
back

"""
from classes.character import Character
class Unit():
    def __init__(self, leader, unit_id=0):
        self.unit_leader = leader
        self.unit_chars = {0: leader}

        for index in range(1,9):
            self.unit_chars[index] = None

        self.unit_id = unit_id
        leader.unit_id = self.unit_id

    def add_char_to_unit(self, char, position):
        if char.unit_id != -1:
            print(f"{char.char_name} is already in unit {char.unit_id}")
            return

        if self.unit_chars[position] is not None:
            print(f"Character already exists in position {position}, cannot add")
            return

        print(f"Adding {char.char_name} to unit {self.unit_id}")
        self.unit_chars[position] = char
        char.unit_id = self.unit_id
        char.base_position = position

    def get_char_by_id(self):
        """ returns a dictionary of {unit_id: unit}

        """
        char_ids = {}
        for position, char in self.unit_chars.items():
            if char is not None:
                char_ids[char.char_id] = char

        return char_ids

    def char_in_unit(char):
        # if the char is already in a unit, can't add again.
        pass

    def print_unit_map(self):
        print(f"\nUnit Map for {self.unit_id}")
        for position in self.unit_chars:
            print(position, self.unit_chars[position].char_name)

    def are_all_chars_dead(self):
        for pos, char in self.unit_chars.items():
            if char is not None:
                if char.is_dead == False:
                    return False

        print(f"{self.unit_leader.char_name}'s unit is crushed!")
        return True

    def can_any_character_take_action_in_battle(self, round_number):
        for pos, char in self.unit_chars.items():
            if char is not None:
                if char.get_num_actions() >= round_number and char.is_dead == False:
                    if char.status == None:
                        return True

        return False

    def can_any_character_take_action_in_round(self, round_number):
        for pos, char in self.unit_chars.items():
            if char is not None:
                if char.get_num_actions() > round_number and \
                        char.has_performed_action_this_round == False:
                    if char.status is None and char.is_dead == False:
                        return True

        return False

    def which_row_can_go(self):
        char_index = -1
        for pos, char in self.unit_chars.items():
            if char is not None:
                if char.has_performed_action_this_round == False and char.is_dead == False:
                    char_index = pos
                    break

        if char_index == -1:
            return -1
        
        if char_index <= 2:
            return 0

        if char_index <= 5:
            return 1

        if char_index <= 8:
            return 2

    def get_agi_by_row(self, row_index):
        row_agi = 0
        num_row_chars = 0
        row_chars = 0
        for col in range(0,3):
            char = self.unit_chars[row_index*3+col]
            if char is not None:
                row_chars += 1
                row_agi += char.agility

        return row_agi / row_chars

    def get_first_non_dead_char_in_unit(self):
        # this is a temp function that just returns the first non-dead char in the unit from 0 to 8
        
        for pos, char in self.unit_chars.items():
            if char is not None:
                if char.is_dead == False:
                    return char
