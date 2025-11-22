from __future__ import annotations

""" character.py

This class represents a single character.

"""

# pylint: disable=too-many-instance-attributes # this is okay.
from classes.actions.slash_action import SlashAction
from classes.unit import Unit
from classes.unit_classes.base_class import BaseClass
import math
import itertools
from typing import List


class Character:
    """Contains all the properties and functions used by a single individual character.
    Attributes:
        char_name (str): The name of the character.
        char_id (int): The unique id of the character.
        unit_id (int): The ID of the unit this character is in, or -1 for no unit.
        max_health (int): The maximum health value for this character.
        health (int): The current health of this character.
        agility (int): The agility of this character. Determines order in battle.
        strength (int): The strength of this character. Can determine char damage.
        vitality (int): The vitality of this character. Reduces Physical Damage
        base_position (int): The position in the unit that this unit is placed in.
        current_position (int): The current position this char is in. Can change during battle.
        is_alive (bool): Is this character alive?
        has_performed_action_this_round (bool): Has this char taken an action in a given round.
        status (?): What status the character has.
        char_class (obj): What class the character is. (knight, berserker, mage, etc)

    TODO:
        Add more stats -  int, wis, const, alignment
        add props for base stats so those can change during battle?
        add a can_char_act() function that looks at status, is_alive, has performed_action etc.
        Determine reasonable values for stats at level 1. I think a base of 100 is an easy place to start. A max of 1000 per stat?
        I sort of want to try the rock paper scissors meaning knight->archer->mage->knight perhaps?

    """

    statuses = ["Paralyze", "Sleep", "Stone"]
    _id_gen = itertools.count(0)

    def __str__(self):
        return f"{self.char_name}\n\
Max HP: {self.max_health}\n\
Current HP: {self.health}\n\
Agi: {self.agility}\n"

    # pylint: disable=too-many-arguments # this is fine.
    def __init__(
        self,
        name: str,
        char_class=BaseClass(),
        # these values should be set using the classes formula, and there should be a level...
        health: int = 10,
        agility: int = 5,
        strength: int = 5,
        vitality: int = 5,
        intelligence: int = 5,
        wisdom: int = 5,
        level: int = 1,
    ):
        self.char_name = name
        self.char_id = next(Character._id_gen)
        self.max_health = health
        self.health = self.max_health
        self.agility = agility
        self.strength = strength
        self.vitality = vitality
        self.wisdom = wisdom
        self.intelligence = intelligence
        self.current_exp = 0
        self.level = level
        self.base_position = 0
        self.current_position = 0
        self.is_alive = True
        self.has_performed_action_this_round = False
        self.status = (
            None  # what var type should this be? I think string is probably fine?
        )
        self.char_class = char_class
        self.unit = None

    @property
    def is_left(self):
        return self.current_position in (0, 3, 6)

    @property
    def is_center(self):
        return self.current_position in (1, 4, 7)

    @property
    def is_right(self):
        return self.current_position in (2, 5, 8)

    @property
    def unit_id(self):
        if self.unit:
            return self.unit.unit_id

        return -1

    def get_action_by_row(self):
        """Gets this characters action from their class using their current position.

        Returns:
            the characters Action() for their row.
        """

        row = self.get_row_from_position()
        return self.char_class.actions[row]

    def get_row_from_position(self) -> int:
        """Gets this characters row by checking their current position.

        Returns:
            The index of the row this character is in. 0-2: 0, 3-5: 1 6-8: 2

        """
        if self.current_position <= 2:
            return 0

        if self.current_position > 2 and self.current_position <= 5:
            return 1

        return 2

    def get_num_actions(self) -> int:
        """Gets this characters number of actions per round by checking their class.

        Returns:
            The number of actions this character should take in a battle.

        """
        row = self.get_row_from_position()

        return self.char_class.num_actions[row]

    def determine_target(self, enemy_unit: Unit) -> object:
        """Get the target of this characters action given the enemy unit and the action to take.

        Args:
            enemy_unit (Unit): The enemy unit we're determing target from.
            targeting_mode (str): The targeting mode for this unit.
            action (Action): The action this character will take.

        Returns:
            the enemy character we are to take an action against.
        """

        targeting_mode = self.unit.targeting_mode
        action = self.get_action_by_row()
        targets = self.determine_possible_targets(enemy_unit, action)
        return self.determine_target_based_on_mode(targeting_mode, targets, enemy_unit)

    def determine_target_based_on_mode(self, targeting_mode, targets, enemy_unit):
        if targeting_mode == "Leader":
            if enemy_unit.unit_leader in targets:
                return enemy_unit.unit_leader

        # If using weak or strong, we'd still want to determine which to deal more damage to if there's a tie.
        if targeting_mode == "Strong":
            targets.sort(key=lambda x: x.health, reverse=True)
            return targets[0]

        if targeting_mode == "Weak":
            targets.sort(key=lambda x: x.health, reverse=False)
            return targets[0]

        # Fallthrough to auto.
        return self.get_highest_expected_damage(targets, self.get_action_by_row())

    def get_target_from_column(self, column: int, enemy_unit, targets_back: bool):
        starting_pos = -1
        ending_pos = -1

        if column > 2:
            return None

        if targets_back:
            step = -3
            starting_pos = column + 6
            ending_pos = 0
        else:
            step = 3
            starting_pos = column
            ending_pos = 9

        for i in range(starting_pos, ending_pos, step):
            enemy_char = enemy_unit.unit_chars[i]
            if enemy_char is not None and enemy_char.is_alive:
                return enemy_char

    # This should accept any action, not just slash...
    def determine_possible_targets(
        self, enemy_unit: Unit, action: SlashAction
    ) -> List[Character]:
        targets = []
        targets.append(self.get_target_from_column(1, enemy_unit, action.targets_back))
        if self.is_center:
            targets.append(
                self.get_target_from_column(0, enemy_unit, action.targets_back)
            )
            targets.append(
                self.get_target_from_column(2, enemy_unit, action.targets_back)
            )

        if self.is_left:
            # Left
            targets.append(
                self.get_target_from_column(0, enemy_unit, action.targets_back)
            )

            # We don't have left or middle targets, so we must consider right.
            if len(targets) == 0:
                targets.append(
                    self.get_target_from_column(2, enemy_unit, action.targets_back)
                )

        if self.is_right:
            # Right
            targets.append(
                self.get_target_from_column(2, enemy_unit, action.targets_back)
            )

            # We don't have right or middle targets, so we must consider left.
            if len(targets) == 0:
                targets.append(
                    self.get_target_from_column(0, enemy_unit, action.targets_back)
                )

        targets = [x for x in targets if x is not None]
        return targets

    @staticmethod
    def add_enemies_to_targets(pos_list, targets, enemy_unit):
        """This function adds valid characters from an enemy unit to the list of potential targets
        for a character.
        Args:
            pos_list (List[int]):
            targets (list[Character]): A list of characters that can be targeted.
            enemy_unit (Unit): The opposing unit that we're getting targets from.

        Returns:
            A list of Character objects that can be targets for a characters action.

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

    def get_highest_expected_damage(self, targets: List[Character], action):
        """Given a list of targets and an action, this function calculates the expected damage of
        an action to each target, and returns the target that would should take the most damage
        from the action.

        This is used by the 'Auto' targetting mode.

        # Returns a character...
        """

        best_target = None
        best_damage = -1
        target_hp = math.inf
        for target in targets:
            expected_damage = action.get_damage(self, target, is_crit=False)
            print(
                f"**{self.char_name} should do {expected_damage} to {target.char_name}",
            )
            if expected_damage > best_damage:
                best_damage = expected_damage
                best_target = target
                target_hp = target.health

            # If the damage would be the same for more than 1 character, take the one that has lower HP.
            # Eventually we probably have AutoWeak and AutoStrong to determine tie-breaker.
            elif expected_damage == best_damage:
                if target_hp > target.health:
                    target_hp = target.health
                    best_target = target

        if best_target:
            print(
                f"**{best_target.char_name} is the target with a damage of {best_damage}\n"
            )
            return best_target

        return None

    def can_character_act(self, round_number):
        if self.get_num_actions() >= round_number and self.is_alive is True:
            if self.status not in self.statuses:
                return True
        return False
