""" run.py 

This is the main script for running the game.

"""
from classes.character import Character
from classes.unit import Unit
from classes.game import Game
from classes.turn import Turn
from classes.battle import Battle
import time

def main():
    # I think this script just creates two units and runs a battle between them?
    # we create a number of units, assign them to unit positions, then make the units fight.
    # I could eventually make this kind of a text based game where I can move characters around
    # change classes and the like.
    game = Game()
    print("Creating some characters")
    pol_char = Character("Pol", char_id=1, agility=2, strength=2, health=1)
    fast_char = Character("PolFast", char_id=3, agility=4, strength=3, health=5)
    dio_char = Character("Dio", char_id=2, agility=4, strength=1, health=20)
    dio_clone_char = Character("Dioclone", char_id=4, agility=1, strength=1, health=10)

    pol_unit = Unit(pol_char, unit_id=1)
    dio_unit = Unit(dio_char, unit_id=2)


    print("\nadding chars to unit")
    pol_unit.add_char_to_unit(fast_char, 3)
    dio_unit.add_char_to_unit(dio_clone_char, 1)

    while True:
        display_menu()

        choice = input()

        if choice == "1":
            # print char by id? We don't have a global dict of Characters to index for this.
            pass

        elif choice == "2":
            start_battle(pol_unit, dio_unit)
        elif choice == "3":
            exit()

def start_battle(unit_one, unit_two):
    print(f"Commencing battle between units controlled by {unit_one.unit_leader.char_name} and " + \
            f"{unit_two.unit_leader.char_name}\n")

    battle = Battle(unit_one, unit_two)
    fight_it_out(battle)

def fight_it_out(battle):
    # cache the unit layouts so we can reset them if we get crit during battle.
    # can we also cache their stats by making a copy of the characters or something?
    # we need a global dict of chars that have all the base stats that we can adjust
    # something like that. it goes back to being a database I guess.
    while not battle.is_battle_finished():

        print(f"Round: {battle.round+1}")
        while not battle.is_round_finished():
            row_for_unit_one = battle.unit_close.which_row_can_go()
            row_for_unit_two = battle.unit_far.which_row_can_go()

            if row_for_unit_one >= 0 and row_for_unit_two >= 0:
                agi_one = battle.unit_close.get_agi_by_row(row_for_unit_one)
                agi_two = battle.unit_far.get_agi_by_row(row_for_unit_two)

                if agi_one > agi_two:
                    row, char_order = determine_turn_order(battle.unit_close, row_for_unit_one)
                    enemy_unit = battle.unit_far
                elif agi_one < agi_two:
                    row, char_order = determine_turn_order(battle.unit_far, row_for_unit_two)
                    enemy_unit = battle.unit_close
                elif agi_one == agi_two:
                    print(f"They had the same agi")
                    # coin flip for who goes.
                    # hard set to unit close for now.
                    row, char_order = determine_turn_order(battle.unit_close, row_for_unit_one)
                    enemy_unit = battle.unit_far

            elif row_for_unit_one >= 0:
                row, char_order = determine_turn_order(battle.unit_close, row_for_unit_one)
                enemy_unit = battle.unit_far
            elif row_for_unit_two >= 0:
                row, char_order = determine_turn_order(battle.unit_far, row_for_unit_two)
                enemy_unit = battle.unit_close

            for char in char_order:
                action = char.get_action_by_row(row)
                # determine target will always just return the first index of an alive unit
                # for now.
                enemy = char.determine_target(enemy_unit, action)
                print(f"{char.char_name} uses {action} on {enemy.char_name}!")
                battle.take_action(char, action, enemy)

            time.sleep(2)

        battle.round += 1

        # reset has_acted for all chars.
        for unit in [battle.unit_far, battle.unit_close]:
            for pos, char in unit.unit_chars.items():
                if char is not None:
                    char.has_performed_action_this_round = False

        # reset statuses maybe
        # after a row has gone, we need to recalc each characters num actions and what ability
        # they use.

def determine_turn_order(unit, unit_row):
    char_order = []

    for col in range(0,3):
        char = unit.unit_chars[unit_row*3+col]
        if char is not None and char.is_dead == False:
            char_order.append(char)
        else:
            continue

    char_order.sort(key=lambda x: x.agility, reverse=True)

    return unit_row, char_order

def display_menu():
    print("1. Print character by id")
    print("2. Run a battle")
    print("3. Exit")


if __name__ == "__main__":
    main()