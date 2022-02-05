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
        return f"{self.char_name}\nMax HP: {self.health}\nAgi: {self.agility}\n"

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

    def determine_target(self, unit, action) -> object:
        """ Get the target of this characters action given the enemy unit and the action to take.

            Args:
                unit:
                action:
                

            Returns:
                the enemy character we are to take an action against.

            TODO:
                Currently this function selects the first non-dead unit.
                It should first use our action to determine possible targets
                then it should check the targetting mode (auto, weakest, strongest, etc)
                to determine who to swing against.

            Implement this
                if our charcter is on one side, get chars for that side and the middle.
                if none, get chars from the third row

                if our char is in the middle, get a list of all chars.

                if action.targets_front:

        """
        return unit.get_first_non_dead_char_in_unit()
