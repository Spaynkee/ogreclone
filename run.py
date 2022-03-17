""" run.py

This is the main script for running the game.

"""
import sys
from classes.game import Game
from classes.unit import Unit
from classes.battle import Battle
from classes.unit_classes.knight import KnightClass

def main():
    """ The main function of our program. Creates a couple characters, adds them to a couple units,
        then displays a menu that allows options to be selected.

    """
    game = Game()

    print("Creating some characters")
    pol_char = game.create_character("Pol", KnightClass(), agility=2, strength=10, health=100)
    fast_char = game.create_character("PolFast", KnightClass(), agility=4, strength=3, health=50)
    dio_char = game.create_character("Dio", KnightClass(), agility=4, strength=5, health=100)
    dio_clone_char = game.create_character("Clone", KnightClass(), agility=1, strength=5, health=10)

    pol_unit = game.create_unit(pol_char)
    pol_unit.move_character(pol_char, 0, 1, temp=False)

    dio_unit = game.create_unit(dio_char)
    dio_unit.move_character(dio_char, 0,7, temp=False)

    print("\nadding chars to unit")

    pol_unit.add_char_to_unit(fast_char, 2)
    dio_unit.add_char_to_unit(dio_clone_char, 2)
    pol_unit.print_unit_map()
    dio_unit.print_unit_map()

    print(pol_char)

    while True:
        display_menu()
        choice = input()

        if choice == "1":
            # print char by id. We don't have a dict of Characters to index for this right now.
            pass
        elif choice == "2":
            print("Which unit id?")
            unit_id = int(input())

            if unit_id not in game.units:
                print("Unit id does not exist")

            game.units[unit_id].print_unit_map()

        elif choice == "3":
            start_battle(game, pol_unit, dio_unit)
        elif choice == "4":
            sys.exit()

def start_battle(game, unit_one: Unit, unit_two: Unit):
    """ Creates a Battle Object and uses that battle object to begin a battle.

        Args:
            unit_one: The close unit
            unit_two: The far unit.

        TODO:
             can we also cache chars stats by making a copy of the characters or something?
             we need a global dict of chars that have all the base stats that we can adjust
             something like that. it goes back to being a database I guess.
    """
    print(f"Commencing battle between units controlled by {unit_one.unit_leader.char_name} and " + \
            f"{unit_two.unit_leader.char_name}\n")

    battle = Battle(game, unit_one, unit_two)
    battle.fight_it_out()

def display_menu():
    """ Displays the menu for our little program here.

    """
    print("1. Print character by id")
    print("2. Print unit map by id")
    print("3. Run a battle")
    print("4. Exit")


if __name__ == "__main__":
    main()
