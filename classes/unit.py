""" unit.py

contains the class representing a unit. A unit consists of 9 tiles with a position assigned to each.

Front
0 1 2
3 4 5
6 7 8
back

"""
class Unit():
    """ Contains all the properties and methods used in a Unit object.
        A Unit is a collection of characters, with one character set as the leader of the group.

        Attributes:
            unit_leader (Character): the leader of the unit. If the leader dies, the unit cannot be
                given orders.
            unit_chars (dict): A dictionary of characters in a unit. The key is the
                position in the unit and the value is a Charcter object.
            unit_id (int): The unique ID of the unit.
            targeting_mode (str): The targeting mode of the unit.

    """
    def __init__(self, leader, unit_id=0):
        self.unit_leader = leader
        self.unit_chars = {0: leader}
        self.targeting_mode = "Strong" #other valus include Strong Weak Auto Leader

        for index in range(1,9):
            self.unit_chars[index] = None

        self.unit_id = unit_id
        leader.unit_id = self.unit_id

    def add_char_to_unit(self, char, position):
        """ Adds a character to a unit in a position.

            Args:
                char (Character): The character being added to this unit.
                position (int): The position the character is being placed in.

        """

        if position > 8 or position < 0:
            print("position index out of range")
            return

        if char.unit_id != -1:
            print(f"{char.char_name} is already in unit {char.unit_id}")
            return

        if self.unit_chars[position] is not None:
            print(f"{self.unit_chars[position].char_name} already exists in position \
                    {position}, cannot add")
            return

        print(f"Adding {char.char_name} to unit {self.unit_id}")
        char.unit_id = self.unit_id
        char.base_position = position
        self.unit_chars[position] = char

    def print_unit_map(self):
        """ Prints a map of the characters in this unit.
        """
        unit_map = ""
        unit_map = f"\nUnit Map for unit: {self.unit_id}\n    Front\n"

        for position, char in self.unit_chars.items():
            if position in (3,6):
                unit_map += "\n"
            if char is not None:
                unit_map += f"{char.char_name} "
            else:
                unit_map += "None "
        unit_map += "\n"
        return unit_map

    def is_any_char_alive(self):
        """ Determines if any character is alive in this unit.

            Returns:
                True if there is at least one character alive
                False if no characters are alive.
        """
        for _, char in self.unit_chars.items():
            if char is not None:
                if char.is_alive is True:
                    return True

        print(f"{self.unit_leader.char_name}'s unit is crushed!")
        return False

    def can_any_character_take_action_in_battle(self, round_number) -> bool:
        """ Determines if any character can take an action during this battle.
            Uses the current round number and the units total number of actions

            Ex: if a unit can go 2 times max, but it's round 3, that character cannot act.

            Args:
                round_number (int): The current round number for a battle.
            Returns:
                True: if there is at least one character that can still act during this battle.
                False: if no characters can act based on total number of actions and round num.
        """
        for _, char in self.unit_chars.items():
            if char is not None:
                if char.get_num_actions() >= round_number and char.is_alive is True:
                    if char.status is None:
                        return True

        return False

    def can_any_character_take_action_in_round(self, round_number) -> bool:
        """ Determines if any character can take an action during this round.

            Args:
                round_number (int): The current round number for a battle.
            Returns:
                True: if the a character has available actions, and has not acted this round.
                False: if no characters can act based on total number of actions, or if all chars
                    have acted.
        """
        for _, char in self.unit_chars.items():
            if char is not None:
                if char.get_num_actions() > round_number and \
                        char.has_performed_action_this_round is False:
                    if char.status is None and char.is_alive is True:
                        return True

        return False

    def which_row_can_go(self) -> int:
        """ Determines which row in this unit can act. The battle system uses rows to determine
            turn order. If both units in battle have rows that can act, they must be compared
            to figure out which row acts first.

            Returns:
                An integer denoting the row index for the first row that can act
        """
        char_index = -1
        for pos, char in self.unit_chars.items():
            if char is not None:
                if char.has_performed_action_this_round is False and char.is_alive is True:
                    char_index = pos
                    break

        if 0 <= char_index <= 2:
            return 0

        if 2 < char_index <= 5:
            return 1

        if 5 < char_index <= 8:
            return 2

        return -1

    def get_agi_by_row(self, row_index) -> float:
        """ Gets the average agility of characters in a particiular row in a unit.
            Used to determine turn order when both units have rows that can take action.

            Args:
                row_index (int): the row in this unit we're getting the average agi for.

            Returns:
                A number denoting a rows average agility.
        """
        row_agi = 0
        row_chars = 0
        for col in range(0,3):
            char = self.unit_chars[row_index*3+col]
            if char is not None:
                row_chars += 1
                row_agi += char.agility

        return row_agi / row_chars

    def get_first_non_dead_char_in_unit(self):
        """ Temp function wrote for selecting the first non-dead char in  unit.
            Currently used for determining target of actions, as I don't have target selection
            written yet.

            Returns:
                The first alive character in a unit based on unit position.
        """
        for _, char in self.unit_chars.items():
            if char is not None:
                if char.is_alive is True:
                    return char

        return None

    def move_character(self, char: object, old_pos: int, new_pos: int, temp: bool=False):
        """ Moves a character within a unit. A character cannot move to an occupied space.
            An empty space cannot be moved.

            Args:
                char (Character): The character object to be moved within the unit.
                old_pos (int):    The current position of the character
                new_pos (int):    The new position of the character
                temp (bool):      Is the movement temporary (such as a crit)

        """
        if new_pos > 8 or new_pos < 0:
            return

        if self.unit_chars[old_pos] is None:
            return

        if self.unit_chars[new_pos] is not None:
            return

        if not temp:
            char.base_position = new_pos

        self.unit_chars[new_pos] = self.unit_chars[old_pos]
        self.unit_chars[old_pos] = None

    def get_character_position(self, char: object) -> int:
        """ Gets a characters position within a unit.

            Args:
                char (Character): The character object to get the position of

            Returns:
                An integer with the position of the character in the unit.

        """
        return list(self.unit_chars.keys())[list(self.unit_chars.values()).index(char)]

    def reset_character_positions(self):
        """ Resets all characters of this unit back to their base positions.
        """
        for _, char in self.unit_chars.items():
            if char is not None:
                char_pos = self.get_character_position(char)
                self.move_character(char, char_pos, char.base_position, temp=False)

    def reset_has_performed_action_this_round(self):
        """ Resets all this units characters has_performed_action_this_round flag
        """
        for _, char in self.unit_chars.items():
            if char is not None:
                char.has_performed_action_this_round = False

    def determine_turn_order(self, row_index):
        """ This function accepts a unit and a units_row and determines the order the characters
            will act in.

            Args:
                unit:       A Unit object.
                unit_row:   A row index for this unit

            Returns:
                a list of Character() objects in the order they should do their actions.

            TODO:
                This might need to be a Unit() function.

        """
        char_order = []

        for col in range(0,3):
            char = self.unit_chars[row_index*3+col]
            if char is not None and char.is_alive is True:
                char_order.append(char)
            else:
                continue

        char_order.sort(key=lambda x: x.agility, reverse=True)

        return char_order
