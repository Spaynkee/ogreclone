import pytest
from classes.actions.slash_action import SlashAction
from classes.character import Character
from classes.unit_classes.knight import KnightClass
from unittest.mock import Mock
from classes.unit import Unit


class TestCharacterGetActionByRow:
    """Contains all the test cases for Character.get_action_by_row()."""

    def test_get_action_by_row_for_front_row(self):
        character = Character("unit", KnightClass(), 1)
        assert type(character.get_action_by_row()) == type(SlashAction())

    def test_get_action_by_row_for_middle_row(self):
        character = Character("unit", KnightClass(), 1)
        assert type(character.get_action_by_row()) == type(SlashAction())

    def test_get_action_by_row_for_back_row(self):
        character = Character("unit", KnightClass(), 1)
        assert type(character.get_action_by_row()) == type(SlashAction())

    def test_get_action_by_row_for_unplaced_character(self):
        character = Character("unit", KnightClass(), 1)
        character.current_position = -1
        assert type(character.get_action_by_row()) == type(SlashAction())


class TestCharacterGetRowFromPosition:
    """Contains all the test cases for Character.get_row_from_position()"""

    def test_get_row_from_position_for_front_row(self):
        character = Character("unit", KnightClass(), 1)
        character.current_position = 1
        assert character.get_row_from_position() == 0

    def test_get_row_from_position_for_middle_row(self):
        character = Character("unit", KnightClass(), 1)
        character.current_position = 4
        assert character.get_row_from_position() == 1

    def test_get_row_from_position_for_back_row(self):
        character = Character("unit", KnightClass(), 1)
        character.current_position = 7
        assert character.get_row_from_position() == 2


class TestCharacterGetNumActions:
    """Contains all the test cases for Character.get_num_actions()"""

    def test_get_num_actions_for_character_in_front_row(self):
        char_class = KnightClass()
        mock_row = 0
        char_class.num_actions[mock_row] = 7  # No character should have 7 actions
        character = Character("unit", char_class, 1)
        assert character.get_num_actions() == char_class.num_actions[mock_row]

    def test_get_num_actions_for_character_in_middle_row(self):
        char_class = KnightClass()
        mock_row = 1
        char_class.num_actions[mock_row] = 7  # No character should have 7 actions
        character = Character("unit", char_class, 1)
        character.current_position = 3
        assert character.get_num_actions() == char_class.num_actions[mock_row]

    def test_get_num_actions_for_character_in_back_row(self):
        char_class = KnightClass()
        mock_row = 2
        char_class.num_actions[mock_row] = 7  # No character should have 7 actions?
        character = Character("unit", char_class, 1)
        character.current_position = 6
        assert character.get_num_actions() == char_class.num_actions[mock_row]


# Technically tested via determine_possible_targets and determine_po
class TestCharacterDetermineTarget:
    """Contains all the test cases for Character.determine_target()"""

    def setup_method(self, method):
        # Create characters
        self.leader = Character("friendly_unit", KnightClass())
        self.enemy_leader = Character("enemy_unit", KnightClass(), 100, vitality=10)
        self.enemy_char = Character("enemy_char", KnightClass())

        # Create units
        self.unit = Unit(self.leader, 0)
        self.unit.move_character(self.leader, 1)
        self.enemy_unit = Unit(self.enemy_leader)
        self.enemy_unit.add_char_to_unit(self.enemy_char, 2)

    def test_determine_target_autononous(self):
        self.enemy_char.vitality = 2
        assert self.unit.targeting_mode == "Auto"
        target = self.unit.unit_leader.determine_target(
            self.enemy_unit,
        )

        # So we should hit the char, not the leader because of vit
        assert self.enemy_leader.vitality > self.enemy_char.vitality
        assert target.char_id == self.enemy_char.char_id

    def test_determine_target_strong(self):
        self.unit.targeting_mode = "Strong"
        target = self.unit.unit_leader.determine_target(
            self.enemy_unit,
        )

        # hits the leader because leader has higher hp.
        assert self.enemy_leader.health > self.enemy_char.health
        assert target.char_id == self.enemy_leader.char_id

    def test_determine_target_weak(self):
        self.unit.targeting_mode = "Weak"
        target = self.unit.unit_leader.determine_target(
            self.enemy_unit,
        )

        # Hits char because char has lower hp.
        assert self.enemy_leader.health > self.enemy_char.health
        assert target.char_id == self.enemy_char.char_id

    def test_determine_target_leader(self):
        self.unit.targeting_mode = "Leader"
        target = self.unit.unit_leader.determine_target(
            self.enemy_unit,
        )

        # Hits leader, because we can.
        assert target.char_id == self.enemy_leader.char_id

    def test_determine_target_leader_not_visible(self):
        self.enemy_unit.move_character(self.enemy_leader, 5)
        self.unit.targeting_mode = "Leader"
        target = self.unit.unit_leader.determine_target(
            self.enemy_unit,
        )

        # Hits character, because leader is behind the char.
        assert target.char_id == self.enemy_char.char_id

    def test_determine_target_leader_back_row_ranged_attack(self):
        pass
