""" character.py

This class represents a single character.

"""

#pylint: disable=too-many-instance-attributes # this is okay.
class Character():
    """ Contains all the properties and functions used by a single individual character.
        Attributes:
            char_name (str): The name of the character.
            char_id (int): The unique id of the character.
            unit_id (int): The ID of the unit this character is in, or -1 for no unit.
            max_health (int): The maximum health value for this character.
            health (int): The current health of this character.
            agility (int): The agility of this character. Determines order in battle.
            strength (int): The strength of this character. Can determine char damage.
            base_position (int): The position in the unit that this unit is placed in.
            current_position (int): The current position this char is in. Can change during battle.
            is_alive (bool): Is this character alive?
            has_performed_action_this_round (bool): Has this char taken an action in a given round.
            status (?): What status the character has.
            char_class (obj): What class the character is. (knight, berserker, mage, etc)

        TODO:
            Add more stats -  int, wis, const, alignment
            has_performed_action_this_round seems kinda weird. Does it belong elsewhere?
            add props for base stats so those can change during battle?

    """

    def __str__(self):
        return f"{self.char_name}\n\
Max HP: {self.max_health}\n\
Current HP: {self.health}\n\
Agi: {self.agility}\n"

    #pylint: disable=too-many-arguments # this is fine.
    def __init__(self, name: str, char_class, char_id: int, health: int = 0,\
            agility: int = 0, strength: int = 0):
        self.char_name = name
        self.char_id = char_id
        self.unit_id = -1
        self.max_health = health
        self.health = self.max_health
        self.agility = agility
        self.strength = strength
        self.base_position = 0
        self.current_position = 0
        self.is_alive = True
        self.has_performed_action_this_round = False
        self.status = None # what var type should this be? I think string is probably fine?
        self.char_class = char_class

    def get_action_by_row(self):
        """ Gets this characters action from their class using their current position.

            Returns:
                the characters Action() for their row.
        """

        row = self.get_row_from_position()
        return self.char_class.actions[row]

    def get_row_from_position(self) -> int:
        """ Gets this characters row by checking their current position.

            Returns:
                The index of the row this character is in. 0-2: 0, 3-5: 1 6-8: 2

        """
        if self.current_position <= 2:
            return 0

        if self.current_position > 2 and self.current_position <= 5:
            return 1

        return 2


    def get_num_actions(self) -> int:
        """ Gets this characters number of actions per round by checking their class.

            Returns:
                The number of actions this character should take in a battle.

        """
        row = self.get_row_from_position()

        return self.char_class.num_actions[row]

    def determine_target(self, enemy_unit, targeting_mode) -> object:
        """ Get the target of this characters action given the enemy unit and the action to take.

            Args:
                enemy_unit (Unit): The enemy unit we're determing target from.
                action (Action): The action this character will take.

            Returns:
                the enemy character we are to take an action against.
        """

        # there is an issue where units can target chars in the back. even if they're melee.
        # we have to add something that says if there's a front unit in a column, don't even think
        # about having another unit in targets. so one target per col, as actions target either
        # the front or the back, and can only hit one of the two of these.

        targets = []

        # always include the middle row as targets.
        targets = self.add_enemies_to_targets((1, 4, 7), targets, enemy_unit)

        # if our character is on the right side of their unit
        if self.current_position in (0, 3, 6):
            targets = self.add_enemies_to_targets((2, 5, 8), targets, enemy_unit)

            # if we don't have any targets in the middle or on the left side, we include right side.
            if len(targets) == 0:
                targets = self.add_enemies_to_targets((0, 3, 6), targets, enemy_unit)

        # if our character is on the left side of their unit
        if self.current_position in (2, 5, 8):
            # we have to get all chars from the right side of enemy_unit
            targets = self.add_enemies_to_targets((0, 3, 6), targets, enemy_unit)

            # if we don't have any targets in the middle or on enemy_units opposite side.
            if len(targets) == 0:
                targets = self.add_enemies_to_targets((2, 5, 8), targets, enemy_unit)
                # we get the left side.

        if targeting_mode == "Leader":
            # return the enemy units leader, if it is in targets. otherwise, auto.
            if enemy_unit.unit_leader in targets:
                return enemy_unit.unit_leader

            targeting_mode = "Auto"

        if targeting_mode == "Strong":
            targets.sort(key=lambda x: x.health, reverse=True)
            return targets[0]

        if targeting_mode == "Weak":
            targets.sort(key=lambda x: x.health, reverse=False)
            return targets[0]

        if targeting_mode == "Auto":
            # this will eventually be based on a chars right, left, and middle attack scores?
            # not really sure how those are calc'd.
            return enemy_unit.get_first_non_dead_char_in_unit()

        return enemy_unit.get_first_non_dead_char_in_unit()

    @staticmethod
    def add_enemies_to_targets(pos_list, targets, enemy_unit):
        """ This function adds valid characters from an enemy unit to the list of potential targets
            for a character.
            Args:
                pos_tuple (List[int]):
                targets (list[Character]): A list of characters that can be targeted.
                enemy_unit (Unit): The opposing unit that we're getting targets from.

            Returns:
                A list of potential targets for a characters action.

            TODO:
                This will eventually need to handle attacks that prioritize the back row.
                So I think it will have to return all potential targets, and we figure out how
                to select one of those when we go to determine_target
        """
        for pos in pos_list:
            enemy_char = enemy_unit.unit_chars[pos]
            if enemy_char is not None and enemy_char.is_alive:
                targets.append(enemy_char)
                return targets

        return targets
