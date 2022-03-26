""" test_unit.py

	This test suite contains all currently written unit tests for the unit.py class.

	There is one class for every unit function, so new test cases should be added as functions
	belonging to the classes in this file.

	Don't forget -- Run this from the root folder and use the command
	python -m unittest test.test_unit.py
"""
#pylint: disable=import-error # False positive.
#pylint: disable=no-self-use # Gotta keep self for unittest
import unittest
from unittest.mock import Mock
from classes.unit import Unit

class TestUnitAddCharToUnit(unittest.TestCase):
    """ Contains all the test cases for Unit.add_character_to_unit().
    """

    def test_char_added_successfully(self):
        """ Adds a character to a unit and ensures character was added and
            poisition/unit_id are set.
        """
        test_unit_id = 6
        test_position = 8

        leader = Mock()
        char = Mock()
        char.unit_id = -1 # this should be updated by the function.

        unit = Unit(leader, test_unit_id)

        # the unit ids are different before the function is called.
        self.assertNotEqual(unit.unit_id, char.unit_id)

        unit.add_char_to_unit(char, test_position)

        # the chars unit id is updated.
        self.assertEqual(unit.unit_id, char.unit_id)

        # the chars unit id is set to what we set the unit id to on creation.
        self.assertEqual(test_unit_id, char.unit_id)

        # the characters base position is set.
        self.assertEqual(char.base_position, test_position)

        # the character was added to the unit.
        self.assertEqual(unit.unit_chars[test_position], char)
        self.assertNotEqual(unit.unit_chars[test_position], None)

    def test_char_not_added_if_position_is_filled(self):
        """ Attempts to add a character to a spot that already has a character in it,
            so the add fails and nothing is updated.
        """
        test_unit_id = 7
        test_position = 5

        leader = Mock()
        existing_char = Mock()
        char = Mock()

        existing_char.unit_id = -1
        char.unit_id = -1
        char.base_position = -1

        unit = Unit(leader, test_unit_id)

        # the unit ids are different before the function is called.
        self.assertNotEqual(unit.unit_id, char.unit_id)

        # adding character to occupied spot.
        unit.add_char_to_unit(existing_char, test_position)
        unit.add_char_to_unit(char, test_position)

        # the chars unit id is not updated.
        self.assertNotEqual(unit.unit_id, char.unit_id)
        self.assertEqual(-1, char.unit_id)

        # the characters base position is not set.
        self.assertNotEqual(char.base_position, test_position)
        self.assertEqual(char.base_position, -1)

        # the character was not added to the unit.
        self.assertNotEqual(unit.unit_chars[test_position], char)

    def test_char_not_added_if_char_already_in_a_unit(self):
        """ Attempts to add a character that already is assigned to a unit
            so the add fails and nothing is updated.
        """
        test_unit_id = 7
        existing_unit_id = 3
        test_position = 3

        leader = Mock()
        char = Mock()

        char.unit_id = existing_unit_id
        char.base_position = -1

        unit = Unit(leader, test_unit_id)

        # the unit ids are different before the function is called.
        self.assertNotEqual(unit.unit_id, char.unit_id)

        # adding character that belongs to another unit.
        unit.add_char_to_unit(char, test_position)

        # the chars unit id is not updated.
        self.assertNotEqual(unit.unit_id, char.unit_id)
        self.assertEqual(existing_unit_id, char.unit_id)

        # the characters base position is not set.
        self.assertNotEqual(char.base_position, test_position)
        self.assertEqual(char.base_position, -1)

        # the character was not added to the unit.
        self.assertNotEqual(unit.unit_chars[test_position], char)

    def test_char_not_added_if_position_out_of_range_high(self):
        """ Attempts to add a character to a position higher than 8
            so the add fails and nothing is updated.
        """
        test_unit_id = 7
        test_position = 9

        leader = Mock()
        char = Mock()

        char.unit_id = -1
        char.base_position = -1

        unit = Unit(leader, test_unit_id)

        # the unit ids are different before the function is called.
        self.assertNotEqual(unit.unit_id, char.unit_id)

        # adding character to a position thats out of range.
        unit.add_char_to_unit(char, test_position)

        # the chars unit id is not updated.
        self.assertNotEqual(unit.unit_id, char.unit_id)
        self.assertEqual(-1, char.unit_id)

        # the characters base position is not set.
        self.assertNotEqual(char.base_position, test_position)
        self.assertEqual(char.base_position, -1)

    def test_char_not_added_if_position_out_of_range_low(self):
        """ Attempts to add a character to a position lower than 0
            so the add fails and nothing is updated.
        """
        test_unit_id = 7
        test_position = -1

        leader = Mock()
        char = Mock()

        char.unit_id = -1
        char.base_position = None

        unit = Unit(leader, test_unit_id)

        # the unit ids are different before the function is called.
        self.assertNotEqual(unit.unit_id, char.unit_id)

        # adding character to a position thats out of range.
        unit.add_char_to_unit(char, test_position)

        # the chars unit id is not updated.
        self.assertNotEqual(unit.unit_id, char.unit_id)
        self.assertEqual(-1, char.unit_id)

        # the characters base position is not set.
        self.assertNotEqual(char.base_position, test_position)
        self.assertEqual(char.base_position, None)

class TestUnitPrintUnitMap(unittest.TestCase):
    """ Tests Unit.print_unit_map()
    """
    def test_print_unit_map_first_row(self):
        """ Populates the entire first row of a unit and prints the unit map.
            Asserts that the map is as expected.
        """
        test_unit_id = 7

        leader = Mock()
        first_char = Mock()
        second_char = Mock()
        third_char = Mock()

        first_char.char_name = "first"
        second_char.char_name = "second"
        third_char.char_name = "third"

        unit = Unit(leader, test_unit_id)

        unit.unit_chars[0] = first_char
        unit.unit_chars[1] = second_char
        unit.unit_chars[2] = third_char

        unit_map = unit.print_unit_map()
        expected_map = f"\nUnit Map for unit: {unit.unit_id}\n"
        expected_map += "    Front\n"
        expected_map += f"{first_char.char_name} {second_char.char_name} {third_char.char_name} \n"
        expected_map += "None None None \n"
        expected_map += "None None None \n"
        self.assertEqual(unit_map, expected_map)

    def test_print_unit_map_one_char_each_row(self):
        """ Populates the all three rows of a unit and prints the unit map.
            Asserts that the map is as expected.
        """
        test_unit_id = 7

        leader = Mock()
        first_char = Mock()
        second_char = Mock()
        third_char = Mock()

        first_char.char_name = "first"
        second_char.char_name = "second"
        third_char.char_name = "third"

        unit = Unit(leader, test_unit_id)

        unit.unit_chars[0] = first_char
        unit.unit_chars[3] = second_char
        unit.unit_chars[6] = third_char

        unit_map = unit.print_unit_map()
        expected_map = f"\nUnit Map for unit: {unit.unit_id}\n"
        expected_map += "    Front\n"
        expected_map += f"{first_char.char_name} None None \n"
        expected_map += f"{second_char.char_name} None None \n"
        expected_map += f"{third_char.char_name} None None \n"
        self.assertEqual(unit_map, expected_map)

    def test_print_unit_map_first_and_last_positions(self):
        """ Populates the first and last spots of the unit and asserts that the map is as expected.
        """
        test_unit_id = 7

        leader = Mock()
        first_char = Mock()
        second_char = Mock()

        first_char.char_name = "first"
        second_char.char_name = "second"

        unit = Unit(leader, test_unit_id)

        unit.unit_chars[0] = first_char
        unit.unit_chars[8] = second_char

        unit_map = unit.print_unit_map()
        expected_map = f"\nUnit Map for unit: {unit.unit_id}\n"
        expected_map += "    Front\n"
        expected_map += f"{first_char.char_name} None None \n"
        expected_map += "None None None \n"
        expected_map += f"None None {second_char.char_name} \n"
        self.assertEqual(unit_map, expected_map)

class TestUnitIsAnyCharAlive(unittest.TestCase):
    """ Tests Unit.is_any_char_alive()
    """

    def test_is_any_char_alive_true(self):
        """ Create a unit with one alive character and assert the function returns true.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True

        unit = Unit(leader, test_unit_id)
        self.assertTrue(unit.is_any_char_alive())

    def test_is_any_char_alive_false(self):
        """ Create a unit with one dead character and assert the function returns false.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = False

        unit = Unit(leader, test_unit_id)
        self.assertFalse(unit.is_any_char_alive())

    def test_is_any_char_alive_mixed_characters(self):
        """ Create a unit with one dead character, and one alive character,
             and assert the function returns true.
        """

        test_unit_id = 7
        leader = Mock()
        second_char = Mock()
        leader.is_alive = False
        second_char.is_alive = True

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[8] = second_char
        self.assertTrue(unit.is_any_char_alive())

    def test_is_any_char_alive_multiple_chars_alive(self):
        """ Create a unit with multiple characters alive and assert the function returns true.
        """

        test_unit_id = 7
        leader = Mock()
        second_char = Mock()
        leader.is_alive = True
        second_char.is_alive = True

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[8] = second_char
        self.assertTrue(unit.is_any_char_alive())

    def test_is_any_char_alive_multiple_chars_dead(self):
        """ Create a unit with multiple characters alive and assert the function returns true.
        """

        test_unit_id = 7
        leader = Mock()
        second_char = Mock()
        leader.is_alive = False
        second_char.is_alive = False

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[8] = second_char
        self.assertFalse(unit.is_any_char_alive())

class TestUnitCanAnyCharacterTakeActionInBattle(unittest.TestCase):
    """ Tests Unit.can_any_character_take_action_in_battle()
    """

    def test_can_any_character_take_action_in_battle_true(self):
        """ Create a unit with a single character with no status that can take an action.
            Assert the function returns True.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.get_num_actions.return_value = 2
        round_number = 1

        unit = Unit(leader, test_unit_id)
        self.assertTrue(unit.can_any_character_take_action_in_battle(round_number))

    def test_can_any_character_take_action_in_battle_false(self):
        """ Create a unit with a single character with no status that has no actions left.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.get_num_actions.return_value = 1
        round_number = 2

        unit = Unit(leader, test_unit_id)
        self.assertFalse(unit.can_any_character_take_action_in_battle(round_number))

    def test_can_any_character_take_action_in_battle_actions_equals_round_number(self):
        """ Create a unit with a single character with no status whos num_actions = round number
            Assert the function returns True.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.get_num_actions.return_value = 2
        round_number = 2

        unit = Unit(leader, test_unit_id)
        self.assertTrue(unit.can_any_character_take_action_in_battle(round_number))

    def test_can_any_character_take_action_in_battle_with_sleep_status_false(self):
        """ Create a unit with a single character with an action and a status of Sleep.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = 'Sleep'
        leader.get_num_actions.return_value = 2
        round_number = 1

        unit = Unit(leader, test_unit_id)
        self.assertFalse(unit.can_any_character_take_action_in_battle(round_number))

    def test_can_any_character_take_action_in_battle_with_stone_status_false(self):
        """ Create a unit with a single character with a status of Stone.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = 'Stone'
        leader.get_num_actions.return_value = 2
        round_number = 1

        unit = Unit(leader, test_unit_id)
        self.assertFalse(unit.can_any_character_take_action_in_battle(round_number))

    def test_can_any_character_take_action_in_battle_with_poison_status_true(self):
        """ Create a unit with a single character with available actions and a status of poison.
            Assert the function returns True.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = 'Poison'
        leader.get_num_actions.return_value = 2
        round_number = 1

        unit = Unit(leader, test_unit_id)
        self.assertTrue(unit.can_any_character_take_action_in_battle(round_number))

    def test_can_any_character_take_action_in_battle_with_poison_status_no_action_false(self):
        """ Create a unit with a single character with no actions and a status of poison.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = 'Poison'
        leader.get_num_actions.return_value = 1
        round_number = 2

        unit = Unit(leader, test_unit_id)
        self.assertFalse(unit.can_any_character_take_action_in_battle(round_number))

    def test_can_any_character_take_action_in_battle_multiple_chars_true(self):
        """ Create a unit with multiple characters with no status that can take an action.
            Assert the function returns True.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None

        leader.get_num_actions.return_value = 2
        second_char.get_num_actions.return_value = 2
        round_number = 1

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[1] = second_char
        self.assertTrue(unit.can_any_character_take_action_in_battle(round_number))

    def test_can_any_character_take_action_in_battle_multiple_chars_false(self):
        """ Create a unit with multiple characters with no status that cannot take an action.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None

        leader.get_num_actions.return_value = 1
        second_char.get_num_actions.return_value = 1
        round_number = 3

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[1] = second_char
        self.assertFalse(unit.can_any_character_take_action_in_battle(round_number))

    def test_can_any_character_take_action_in_battle_multiple_chars_mixed_true(self):
        """ Create a unit with multiple characters with no status where one character can act.
            Assert the function returns True.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None

        leader.get_num_actions.return_value = 2
        second_char.get_num_actions.return_value = 1
        round_number = 2

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[1] = second_char
        self.assertTrue(unit.can_any_character_take_action_in_battle(round_number))

    def test_can_any_character_take_action_in_battle_multiple_chars_mixed_dead(self):
        """ Create a unit with multiple characters with no status where one character can act, but
            that character is dead.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = False
        leader.status = None

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None

        leader.get_num_actions.return_value = 2
        second_char.get_num_actions.return_value = 1
        round_number = 2

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[1] = second_char
        self.assertFalse(unit.can_any_character_take_action_in_battle(round_number))

    def test_can_any_character_take_action_in_battle_multiple_chars_mixed_status(self):
        """ Create a unit with multiple characters with no status where one character can act, but
            that character has a status
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = "Sleep"

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None

        leader.get_num_actions.return_value = 2
        second_char.get_num_actions.return_value = 1
        round_number = 2

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[1] = second_char
        self.assertFalse(unit.can_any_character_take_action_in_battle(round_number))

    def test_can_any_character_take_action_in_battle_multiple_chars_mixed_all_dead(self):
        """ Create a unit with multiple characters with no status where all characters can act, but
            they're all dead.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = False
        leader.status = None

        second_char = Mock()
        second_char.is_alive = False
        second_char.status = None

        leader.get_num_actions.return_value = 2
        second_char.get_num_actions.return_value = 2
        round_number = 2

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[1] = second_char
        self.assertFalse(unit.can_any_character_take_action_in_battle(round_number))

class TestUnitCanAnyCharacterTakeActionInRound(unittest.TestCase):
    """ Tests Unit.can_any_character_take_action_in_round()
    """

    def test_can_any_character_take_action_in_rounde_true(self):
        """ Create a unit with a single character with no status that can take an action.
            Assert the function returns True.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.get_num_actions.return_value = 2
        leader.has_performed_action_this_round = False
        round_number = 1

        unit = Unit(leader, test_unit_id)
        self.assertTrue(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_round_false(self):
        """ Create a unit with a single character with no status that has already taken an action.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.get_num_actions.return_value = 2
        leader.has_performed_action_this_round = True
        round_number = 1

        unit = Unit(leader, test_unit_id)
        self.assertFalse(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_round_actions_equals_round_number(self):
        """ Create a unit with a single character with no status whos num_actions = round number
            Assert the function returns True.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.get_num_actions.return_value = 2
        leader.has_performed_action_this_round = False
        round_number = 2

        unit = Unit(leader, test_unit_id)
        self.assertTrue(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_battle_with_round_status_false(self):
        """ Create a unit with a single character with an action and a status of Sleep.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = 'Sleep'
        leader.get_num_actions.return_value = 2
        leader.has_performed_action_this_round = False
        round_number = 1

        unit = Unit(leader, test_unit_id)
        self.assertFalse(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_round_with_stone_status_false(self):
        """ Create a unit with a single character with a status of Stone.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = 'Stone'
        leader.get_num_actions.return_value = 2
        leader.has_performed_action_this_round = False
        round_number = 1

        unit = Unit(leader, test_unit_id)
        self.assertFalse(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_round_with_poison_status_has_not_acted_true(self):
        """ Create a unit with a single character with available actions and a status of poison.
            Assert the function returns True.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = 'Poison'
        leader.has_performed_action_this_round = False
        leader.get_num_actions.return_value = 2
        round_number = 1

        unit = Unit(leader, test_unit_id)
        self.assertTrue(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_round_with_poison_status_no_action_false(self):
        """ Create a unit with a single character with no actions and a status of poison.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = 'Poison'
        leader.has_performed_action_this_round = False
        leader.get_num_actions.return_value = 1
        round_number = 2

        unit = Unit(leader, test_unit_id)
        self.assertFalse(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_round_with_poison_status_has_acted_false(self):
        """ Create a unit with a single character that has acted and a has status of poison.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = 'Poison'
        leader.has_performed_action_this_round = True
        leader.get_num_actions.return_value = 2
        round_number = 1

        unit = Unit(leader, test_unit_id)
        self.assertFalse(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_round_multiple_chars_true(self):
        """ Create a unit with multiple characters with no status that can take an action.
            Assert the function returns True.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.has_performed_action_this_round = False

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None
        second_char.has_performed_action_this_round = False

        leader.get_num_actions.return_value = 2
        second_char.get_num_actions.return_value = 2
        round_number = 1

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[1] = second_char
        self.assertTrue(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_round_multiple_chars_no_action_false(self):
        """ Create a unit with multiple characters with no status that cannot take an action.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.has_performed_action_this_round = False

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None
        second_char.has_performed_action_this_round = False

        leader.get_num_actions.return_value = 1
        second_char.get_num_actions.return_value = 1
        round_number = 3

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[1] = second_char
        self.assertFalse(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_round_multiple_chars_has_acted_false(self):
        """ Create a unit with multiple characters with no status that have actions but also have
            acted this round.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.has_performed_action_this_round = True

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None
        second_char.has_performed_action_this_round = True

        leader.get_num_actions.return_value = 3
        second_char.get_num_actions.return_value = 3
        round_number = 2

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[1] = second_char
        self.assertFalse(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_round_multiple_chars_mixed_true(self):
        """ Create a unit with multiple characters with no status where one character can act and
            has not acted this round.
            Assert the function returns True.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.has_performed_action_this_round = False

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None
        second_char.has_performed_action_this_round = True

        leader.get_num_actions.return_value = 2
        second_char.get_num_actions.return_value = 1
        round_number = 2

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[1] = second_char
        self.assertTrue(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_round_multiple_chars_mixed_has_acted_false(self):
        """ Create a unit with multiple characters with no status where one character can act and
            has acted this round.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.has_performed_action_this_round = True

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None
        second_char.has_performed_action_this_round = True

        leader.get_num_actions.return_value = 2
        second_char.get_num_actions.return_value = 1
        round_number = 2

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[1] = second_char
        self.assertFalse(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_round_multiple_chars_mixed_dead(self):
        """ Create a unit with multiple characters with no status where one character can act,
            and has not acted this round but that character is dead.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = False
        leader.status = None
        leader.has_performed_action_this_round = False

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None
        second_char.has_performed_action_this_round = True

        leader.get_num_actions.return_value = 2
        second_char.get_num_actions.return_value = 1
        round_number = 2

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[1] = second_char
        self.assertFalse(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_round_multiple_chars_mixed_status(self):
        """ Create a unit with multiple characters with no status where one character can act, but
            that character has a status
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = "Sleep"
        leader.has_performed_action_this_round = False

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None
        second_char.has_performed_action_this_round = True

        leader.get_num_actions.return_value = 2
        second_char.get_num_actions.return_value = 1
        round_number = 2

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[1] = second_char
        self.assertFalse(unit.can_any_character_take_action_in_round(round_number))

    def test_can_any_character_take_action_in_battle_multiple_chars_mixed_all_dead(self):
        """ Create a unit with multiple characters with no status where all characters can act, but
            they're all dead.
            Assert the function returns False.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = False
        leader.status = None
        leader.has_performed_action_this_round = False

        second_char = Mock()
        second_char.is_alive = False
        second_char.status = None
        second_char.has_performed_action_this_round = False

        leader.get_num_actions.return_value = 2
        second_char.get_num_actions.return_value = 2
        round_number = 2

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[1] = second_char
        self.assertFalse(unit.can_any_character_take_action_in_battle(round_number))

class TestUnitWhichRowCanGo(unittest.TestCase):
    """ Tests Unit.which_row_can_go()
    """

    def test_which_row_can_go_first_row_only(self):
        """ Create a unit with a character on row 0 that can act.
            Assert the function returns 0.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.has_performed_action_this_round = False

        unit = Unit(leader, test_unit_id)
        self.assertEqual(unit.which_row_can_go(), 0)

    def test_which_row_can_go_first_row_multiple_rows(self):
        """ Create a unit with multiple characters on rows 0, 1 that can act.
            Assert the function returns 0.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.has_performed_action_this_round = False

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None
        second_char.has_performed_action_this_round = False

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[4] = second_char
        self.assertEqual(unit.which_row_can_go(), 0)

    def test_which_row_can_go_second_row_multiple_rows(self):
        """ Create a unit with multiple characters on rows 0, 1 but only row 1 can go.
            Assert the function returns 1.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.has_performed_action_this_round = True

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None
        second_char.has_performed_action_this_round = False

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[4] = second_char
        self.assertEqual(unit.which_row_can_go(), 1)

    def test_which_row_can_go_no_rows_multiple_rows(self):
        """ Create a unit with multiple characters on rows 0, 1 but no row can go.
            Assert the function returns -1.
        """

        test_unit_id = 7
        leader = Mock()
        leader.is_alive = True
        leader.status = None
        leader.has_performed_action_this_round = True

        second_char = Mock()
        second_char.is_alive = True
        second_char.status = None
        second_char.has_performed_action_this_round = True

        unit = Unit(leader, test_unit_id)
        unit.unit_chars[4] = second_char
        self.assertEqual(unit.which_row_can_go(), -1)

if __name__ == "__main__":
    unittest.main()
