import random
import colorama
# import copy

from classes.color import BColors
from classes.game import logo, draw_statuses, player_action, enemy_action, en_spacer, \
    check_death, gain_xp, shop, drop_loot
from classes.inventory import Bag
from classes.objects import create_party, create_enemies, plitems, spacer, story, items_list, \
    boss, shop_items
# from classes.magic import *


def main():
    colorama.init()
    logo()
    party = create_party()
    partybag = Bag(plitems)
    game = True
    while game:

        dice = random.randint(1, 10)
        if dice <= 4:
            enemies = boss(party)
        else:
            enemies = create_enemies()
        spacer()
        print(f"{BColors.RED}{BColors.ITAL}{story[enemies[0].callout]['start']}{BColors.ENDC}")
        spacer()
        draw_statuses(party, enemies)
        battle = True
        while battle:

            for player in party:
                player_action(player, party, enemies, partybag)
            spacer()
            for enemy in enemies:
                enemy_action(enemy, party, enemies)
            en_spacer()
            draw_statuses(party, enemies)

            if check_death(enemies):
                spacer()
                print(f"{BColors.IGREEN}{BColors.ITAL}{story[enemies[0].callout]['ending']}\nYou WON!{BColors.ENDC}")
                spacer()
                gain_xp(party, story[enemies[0].callout]['xp'])
                spacer()
                party[0].draw_xp()
                spacer()
                drop_loot(partybag, items_list)
                for player in party:
                    player.heal(50)
                    player.restmana(50)

                print(f"{BColors.BOLD}Each party member rested and recovered 50 HP/MP.{BColors.ENDC}")
                shop(partybag, shop_items)
                battle = False

            elif check_death(party):
                en_spacer()
                print(f"{BColors.RED}{BColors.ITAL}{story[enemies[0].callout]['killed']}\nYou LOST!{BColors.ENDC}")
                en_spacer()
                print("\n\n\n")
                battle = False
                game = False


if __name__ == "__main__":
    main()