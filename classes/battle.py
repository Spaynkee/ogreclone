""" battle.py

This object represents a single battle between two units.

"""
class Battle():
    # current_round?
    # max_rounds?
    # ?
    no_turn = ['Para', 'Sleep', 'Stone']

    def __init__(self, unit_1, unit_2):
        self.unit_close = unit_1
        self.unit_far = unit_2
        self.units = [unit_1, unit_2]
        self.characters = {} # yeah maybe so we can update after the battles over?
        self.round = 0

    def is_battle_finished(self):
        if self.is_a_unit_defeated():
            return True

        a_unit_can_act = False
        for unit in self.units:
            if not unit.can_any_character_take_action_in_battle(self.round):
                a_unit_can_act = True
        
        if a_unit_can_act == True:
            return True

        return False
    
    def is_a_unit_defeated(self):
        a_unit_is_dead = False
        for unit in self.units:
            if unit.are_all_chars_dead():
                a_unit_is_dead = True

        if a_unit_is_dead == True:
            return True

        return False


    def is_round_finished(self):
        if self.is_a_unit_defeated():
            return True

        can_unit_act = False
        for unit in self.units:
            if unit.can_any_character_take_action_in_round(self.round):
                can_unit_act = True
        
        if can_unit_act == True:
            return False

        return True

    def take_action(self, actor, action, enemy):
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
            enemy.is_dead = True

        actor.has_performed_action_this_round = True
        print("\n")

