""" battle.py

This object represents a single battle between two units.

"""
import time
class Battle():
    """ Contains all the properties and methods used in a battle object.
        Attributes:
            game (Game): The current state of the game.
            unit_close (Unit): the 'home' unit. 'players' unit. This is a Unit object.
            unit_far (Unit): the enemy unit.  This is a Unit object.
            units (List): A list containing both units for easy looping.
            round (int): An integer denoting the current round of combat.

    """
    no_turn = ['Para', 'Sleep', 'Stone'] # Which statuses prevent an action?

    def __init__(self, game, unit_1, unit_2):
        self.unit_close = unit_1
        self.game = game
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
    def take_action(actor, action, enemy, enemy_unit):
        """ This function performs an action by an actor on an enemy.

            Args:
                actor (Character): The character peforming the action.
                action (Action): The action being taken.
                enemy (Character): The character receiving the action.
                enemy_unit (Unit): The unit of the character receiving the action.

        """
        # use stats from both characters to determine an outcome.
        # for now, we just subtract damage from char health.
        # actions damage can be calculated here?
        # check for a crit
        is_crit = action.determine_crit(actor)
        if is_crit:
            damage = action.get_damage(actor, is_crit=True)
            enemy_pos = enemy_unit.get_character_position(enemy)
            enemy_unit.move_character(enemy, enemy_pos, enemy_pos+3, temp=True)
        else:
            damage = action.get_damage(actor, is_crit=False)

        # determine if it's blocked.
        # damage = char.calculate_defense(damage) # reduces an attack by some amount.
        if is_crit:
            print(f"{enemy.char_name} gets CRIT ON! {damage} damage from {actor.char_name}!")
        else:
            print(f"{enemy.char_name} takes {damage} damage from {actor.char_name}!")

        enemy.health -= damage
        print(f"{enemy.char_name}'s health is reduced to {enemy.health}!")
        if enemy.health <= 0:
            print(f"{enemy.char_name} dies!")
            enemy.is_alive = False

        actor.has_performed_action_this_round = True
        print("\n")

    def available_rows(self):
        """ Gets the first row with available actions for each function in this battle object.

            Returns:
                The the first row indicies for each of the units involved in the battle, or -1 if
                the unit does not have a row that can still take an action.
        """
        return self.unit_close.which_row_can_go(), self.unit_far.which_row_can_go()

    def determine_turn_order_and_enemy_unit(self, row_index_for_unit_close, row_index_for_unit_far):
        """ Determines the turn order, 'friendly' and 'enemy' units for a round of battle.

            Args:
                row_index_for_unit_close (int): The first row that can go for the close unit
                row_index_for_unit_far (int): The first row that can go for the far unit

            Returns:
                char_order: A list of characters in turn order
                friendly_unit: The unit taking actions this round.
                enemy_unit: The unit to be acted upon.
        """
        if row_index_for_unit_close >= 0 and row_index_for_unit_far >= 0:
            agi_close = self.unit_close.get_agi_by_row(row_index_for_unit_close)
            agi_far = self.unit_far.get_agi_by_row(row_index_for_unit_far)

            # we call a function that determines turn order and 'friendly/enemy' unit.
            if agi_close > agi_far:
                char_order = self.unit_close.determine_turn_order(row_index_for_unit_close)
                enemy_unit = self.unit_far
            elif agi_close < agi_far:
                char_order = self.unit_far.determine_turn_order(row_index_for_unit_far)
                enemy_unit = self.unit_close
            elif agi_close == agi_far:
                # coin flip for who goes.
                # hard set to unit close for now.
                char_order = self.unit_close.determine_turn_order(row_index_for_unit_close)
                enemy_unit = self.unit_far

        # only one of the two units can go this turn, but which unit?
        elif row_index_for_unit_close >= 0:
            char_order = self.unit_close.determine_turn_order(row_index_for_unit_close)
            enemy_unit = self.unit_far
        elif row_index_for_unit_far >= 0:
            char_order = self.unit_far.determine_turn_order(row_index_for_unit_far)
            enemy_unit = self.unit_close

        friendly_unit = self.game.get_unit_by_id(char_order[0].unit_id)

        return char_order, enemy_unit, friendly_unit

    def fight_it_out(self):
        """ This function does the majority of the combat logic. Combat will continue until no
            characters can take an action, or until all the characters in a unit are dead.

        """
        self.round = 1
        while not self.is_battle_finished():

            print(f"Round: {self.round}")
            while not self.is_round_finished():
                row_index_for_unit_close, row_index_for_unit_far = self.available_rows()

                char_order, enemy_unit, friendly_unit =\
                        self.determine_turn_order_and_enemy_unit(\
                        row_index_for_unit_close,\
                        row_index_for_unit_far)

                # each character in this row takes their action
                for char in char_order:
                    action = char.get_action_by_row()
                    enemy = char.determine_target(enemy_unit, friendly_unit.targeting_mode)

                    print(f"{char.char_name} uses {action} on {enemy.char_name}!")
                    self.take_action(char, action, enemy, enemy_unit)

                time.sleep(2)

            self.round += 1

            # reset  has_acted for all chars.
            for unit in [self.unit_far, self.unit_close]:
                unit.reset_has_performed_action_this_round()

        # reset statuses maybe

        # reset position for all characters? selfs over I guess.
        for unit in [self.unit_far, self.unit_close]:
            unit.reset_character_positions()
