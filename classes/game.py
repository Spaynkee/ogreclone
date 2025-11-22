"""game.py

contains all the global information for the game, including units, chars and the like.

"""

# pylint: disable=too-few-public-methods # This is fine.
# pylint: disable=too-many-arguments # This is also fine.
# pylint: disable=relative-beyond-top-level # Yes, still fine.
from .character import Character
from .unit import Unit


class Game:
    """The game object stores information about the game state, such as what characters exist
    what units exist, and so on.

    Attributes:
        char_index (int): An int denoting class index
        unit_index (int): An int denoting current unit index.
        chars (dict): A dict containing all the chars in this game.
        units (dict): A dict containing the units in this game.

    """

    chars = {}
    units = {}

    def __init__(self):
        pass

    @classmethod
    def create_character(cls, name, char_class, agility, strength, health, vitality):
        """Creates a character and adds the object to the games char dict."""
        char = Character(
            name,
            char_class,
            agility=agility,
            strength=strength,
            health=health,
            vitality=vitality,
        )
        cls.chars[char.char_id] = char
        return cls.chars[char.char_id]

    @classmethod
    def create_unit(cls, leader_char):
        """Creates a unit and adds the object to the games unit dict."""

        unit = Unit(leader_char)
        cls.units[unit.unit_id] = unit
        return cls.units[unit.unit_id]

    @classmethod
    def get_unit_by_id(cls, unit_id):
        """Gets a unit by id.
        Args:
            unit_id (int): the id of the unit we want to return

        Returns:
            A unit object from our global dict of units.

        """
        if unit_id in cls.units:
            return cls.units[unit_id]

        return None
