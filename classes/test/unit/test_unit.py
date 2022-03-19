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

if __name__ == "__main__":
    unittest.main()
