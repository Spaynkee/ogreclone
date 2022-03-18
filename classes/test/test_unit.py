""" test_unit.py

	This test suite contains all currently written unit tests for the unit.py class.

	There is one class for every unit function, so new test cases should be added as functions
	belonging to the classes in this file.

	Don't forget -- Run this from the root folder and use the command
	python -m unittest test.test_unit.py
"""

import unittest
from unittest.mock import Mock, MagicMock
from classes.unit import Unit
from classes.character import Character

#pylint: disable=no-self-use # Gotta keep self for unittest
class TestUnitAddCharToUnit(unittest.TestCase):
    """ Contains all the test cases for get_first_blood_kill_assist().
    """

    def test_char_added_successfully(self):
        """ Adds a character to a unit.
        """
        test_unit_id = 7
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
