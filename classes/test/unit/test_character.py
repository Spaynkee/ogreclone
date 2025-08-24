from classes.actions.slash_action import SlashAction
from classes.character import Character
from classes.unit_classes.knight import KnightClass


class TestCharacterGetActionByRow:
    """Contains all the test cases for Character.add_character_to_unit()."""

    def test_get_action_by_row_for_front_row(self):
        character = Character("unit", KnightClass(), 1)
        assert type(character.get_action_by_row()) == type(SlashAction())

    def test_get_action_by_row_for_middle_row(self):
        character = Character("unit", KnightClass(), 1)
        assert type(character.get_action_by_row()) == type(SlashAction())

    def test_get_action_by_row_for_unplaced_character(self):
        character = Character("unit", KnightClass(), 1)
        character.current_position = -1
        assert type(character.get_action_by_row()) == type(SlashAction())


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
        char_class.num_actions[mock_row] = 7  # No character should have 7 actions
        character = Character("unit", char_class, 1)
        character.current_position = 6
        assert character.get_num_actions() == char_class.num_actions[mock_row]


class TestCharacterDetermineActions:
    """Contains all the test cases for Character.determine_target()"""

    # create two units, one with one char, the other with 2
    # In each test, set the units targeting_mode
    # Then verify the correct character gets returned.

    def test_determine_target_autononous(self):
        pass
