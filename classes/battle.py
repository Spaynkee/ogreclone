""" battle.py

This object represents a single battle between two units.

"""
class Battle():
    """ Contains all the properties and methods used in a battle object.
        Attributes:
            unit_close (Unit): the 'home' unit. 'players' unit. This is a Unit object.
            unit_far (Unit): the enemy unit.  This is a Unit object.
            units (List): A list containing both units for easy looping.
            round (int): An integer denoting the current round of combat.

    """
    no_turn = ['Para', 'Sleep', 'Stone'] # Which statuses prevent an action?

    def __init__(self, unit_1, unit_2):
        self.unit_close = unit_1
        self.unit_far = unit_2
        self.units = [unit_1, unit_2]
        self.round = 0

    def is_battle_finished(self):
        """ Determines if the battle is finished.

            Returns:
                True if either unit is defeated
                false if either unit has a character that can act

        """
        if self.is_a_unit_defeated():
            return True

        for unit in self.units:
            if unit.can_any_character_take_action_in_battle(self.round):
                return False

        return True

    def is_a_unit_defeated(self) -> bool:
        """ Determines if either unit in this battle is defeated completely.

            Returns:
                True if either of our units has only dead characters.

        """
        for unit in self.units:
            if unit.is_any_char_alive() is False:
                return True

        return False


    def is_round_finished(self):
        """ Determines if both units have performed all possible actions this round.

            Returns:
                True if a unit is defeated or false if either unit can still take an action.

        """
        if self.is_a_unit_defeated():
            return True

        can_unit_act = False
        for unit in self.units:
            if unit.can_any_character_take_action_in_round(self.round):
                can_unit_act = True

        if can_unit_act is True:
            return False

        return True

    @staticmethod
    def take_action(actor, action, enemy):
        """ This function performs an action by an actor on an enemy.

            Args:
                actor (Character): The character peforming the action.
                action (Action): The action being taken.
                enemy (Character): The character receiving the action.

        """
        # use stats from both characters to determine an outcome.
        # for now, we just subtract damage from char health.
        # actions damage can be calculated here?
        # check for a crit
        damage = action.get_damage(actor)
        # if crit:
        # move character back one row if possible.

        # damage = char.calculate_defense(damage) # reduces an attack by some amount.
        print(f"{enemy.char_name} takes {damage} damage from {actor.char_name}!")
        enemy.health -= damage
        print(f"{enemy.char_name}'s health is reduced to {enemy.health}!")
        if enemy.health <= 0:
            print(f"{enemy.char_name} dies!")
            enemy.is_alive = False

        actor.has_performed_action_this_round = True
        print("\n")
