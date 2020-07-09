import random
# import math

from classes.color import BColors
# from classes.magic import *
# from classes.inventory import *
# from classes.objects import *



def spacer():
    line = 20 * "="
    print(f'{BColors.IGREEN}{line}{BColors.ENDC}')


def en_spacer():
    line = 20 * "="
    print(f'{BColors.IRED}{line}{BColors.ENDC}')


def choose_item(bag):
    i = 1
    print(f'{BColors.IYELLOW}{BColors.BOLD}ITEMS:{BColors.ENDC}')
    for item in bag.items:
        print(f"  {str(i)}: {item['item'].name} - {item['item'].description} ({item['quantity']}x)")
        i += 1


def choose_enemy(enemies):
    while True:
        i = 1
        print(f'{BColors.RED}{BColors.BOLD}ENEMIES:{BColors.ENDC}')
        for enemy in enemies:
            print(f"   {str(i)}: {enemy.name} ({enemy.cur_hp()} HP)")
            i += 1
        chosen = int(input(f"{BColors.RED}Pick enemy: {BColors.ENDC}")) - 1
        if chosen in range(0, len(enemies)):
            chosen_enemy = enemies[chosen]
        else:
            chosen_enemy = enemies[0]
        if chosen_enemy.get_hp() == 0:
            print(f'{BColors.RED}{BColors.BOLD}Enemy already dead!{BColors.ENDC}')
            continue
        else:
            return chosen_enemy


def choose_ally(party):
    i = 1
    print(f'{BColors.IGREEN}{BColors.BOLD}ALLIES:{BColors.ENDC}')
    for ally in party:
        print(f"   {str(i)}: {ally.name} ({ally.cur_hp()} HP)")
        i += 1
    chosen = int(input(f"{BColors.IGREEN}Pick ally: {BColors.ENDC}")) - 1
    if chosen in range(0, len(party)):
        return party[chosen]
    else:
        return party[0]


def draw_grid():
    print(f"{BColors.BOLD}{BColors.BGREY + ' '}{BColors.BDGREY}{BColors.GREY}{'NAME':^24}" +
          f"{BColors.BGREY + ' '}{BColors.ENDC}", end='   ')
    print(f"{BColors.BOLD}{BColors.BGREY + ' '}{BColors.GREY}{BColors.BDGREY}" +
          f"{'HEALTH':^11}{BColors.ENDC}", end='')
    print(f"{BColors.BOLD}{BColors.BGREY + ' '}{BColors.BDGREY}{BColors.GREY}{'HEALTH BAR':^36}" +
          f"{BColors.BGREY + ' '}{BColors.ENDC}", end='   ')
    print(f"{BColors.BOLD}{BColors.BGREY + ' '}{BColors.GREY}{BColors.BDGREY}" +
          f"{'MANA/RAGE':^11}{BColors.ENDC}", end='')
    print(f"{BColors.BOLD}{BColors.BGREY + ' '}{BColors.BDGREY}{BColors.GREY}{'MANA/RAGE BAR':^18}" +
          f"{BColors.BGREY + ' '}{BColors.ENDC}")


def draw_statuses(party, enemies):
    draw_grid()
    for player in party:
        print('')
        player.draw_status()
    print('')
    for enemy in enemies:
        print('')
        enemy.draw_enstatus()


def player_action(player, party, enemies, partybag):
    turn = True
    while turn:
        if check_death(enemies) or player.get_hp() == 0:
            break
        spacer()
        print(f"{BColors.IGREEN}{BColors.BOLD}{player.name.upper()} TURN ({player.klas.upper()}){BColors.ENDC}")
        player.choose_action()
        choice = input(f"{BColors.IGREEN}Pick action: {BColors.ENDC}")
        try:
            idx = int(choice) - 1
        except:
            print(f'{BColors.IGREEN}{BColors.BOLD}Wrong choice!{BColors.ENDC}')
            continue

        if idx == 0:
            print(f"{BColors.RED}You've chosen to Attack!{BColors.ENDC}")
            enemy = choose_enemy(enemies)
            dmg = player.gen_dmg(enemy)
            enemy.take_dmg(dmg)
            player.build_rage()
            spacer()
            print(f"You attacked {enemy.name} for {dmg} points of dmg!")
            print(f"{enemy.name} HP is now {enemy.hp}.")
            break
        elif idx == 1:
            if player.klas in ['Mage', 'Priest']:
                try:
                    print(f"{BColors.IBLUE}You've chosen to use Magic!{BColors.ENDC}")
                    player.choose_magic()
                    magic_choice = int(input(f"{BColors.IGREEN}Pick a spell: {BColors.ENDC}")) - 1
                    if magic_choice == -1:
                        continue
                    spell = player.mgk[magic_choice]
                    mdmg = spell.gen_mdmg(player)
                    print(f"{BColors.IBLUE}You've chosen to cast {spell.name}!{BColors.ENDC}")
                    current_mp = player.get_mp()
                    if spell.cost > current_mp:
                        print(f"{BColors.BLUE}...but you don't have enough MP!{BColors.ENDC}")
                        continue
                    spacer()
                    player.mp -= spell.cost
                    if spell.stype == "Black":
                        enemy = choose_enemy(enemies)
                        enemy.take_dmg(mdmg)
                        print(f"Your {spell.name} did {mdmg} points of dmg to {enemy.name}!")
                        print(f"{enemy.name} HP is now {enemy.hp}.")
                    elif spell.stype == "Red":
                        print(f"Your {spell.name} did {mdmg} points of dmg to enemies!")
                        for enemy in enemies:
                            if enemy.hp > 0:
                                enemy.take_dmg(mdmg)
                                print(f"{enemy.name} HP is now {enemy.hp}.")

                    elif spell.stype == "White":
                        ally = choose_ally(party)
                        ally.heal(mdmg)
                        print(f"You healed {ally.name} for {mdmg} points.")

                    elif spell.stype == "Green":
                        print(f"You healed allies for {mdmg} points.")
                        for ally in party:
                            ally.heal(mdmg)
                            print(f"{ally.name} HP is now {ally.hp}.")
                except:
                    print(f"{BColors.BLUE}Not a valid spell! Try again.{BColors.ENDC}")
                    continue
                else:
                    break
            else:
                try:
                    print(f"{BColors.VIOLET}You've chosen to use Abilities!{BColors.ENDC}")
                    player.choose_ability()
                    ability_choice = int(input(f"{BColors.VIOLET}Pick an ability: {BColors.ENDC}")) - 1
                    if ability_choice == -1:
                        continue
                    ability = player.mgk[ability_choice]
                    admg = ability.gen_mdmg(player)
                    print(f"{BColors.VIOLET}You've chosen to use {ability.name}!{BColors.ENDC}")
                    current_rge = player.get_rge()
                    if ability.cost > current_rge:
                        print(f"{BColors.VIOLET}...but you don't have enough RAGE!{BColors.ENDC}")
                        continue
                    spacer()
                    player.rge -= ability.cost
                    if ability.stype == "ABlack":
                        enemy = choose_enemy(enemies)
                        enemy.take_dmg(admg)
                        print(f"Your {ability.name} did {admg} points of dmg to {enemy.name}!")
                        print(f"{enemy.name} HP is now {enemy.hp}.")
                    elif ability.stype == "ARed":
                        print(f"Your {ability.name} did {admg} points of dmg to enemies!")
                        for enemy in enemies:
                            if enemy.hp > 0:
                                enemy.take_dmg(admg)
                                print(f"{enemy.name} HP is now {enemy.hp}.")
                    elif ability.stype == "AWhite":
                        ally = choose_ally(party)
                        ally.heal(admg)
                        print(f"You healed {ally.name} for {admg} points.")
                        print(f"{ally.name} HP is now {ally.hp}.")
                except:
                    print(f"{BColors.BLUE}Not a valid ability! Try again.{BColors.ENDC}")
                    continue
                else:
                    break
        elif idx == 2:
            try:
                print(f"{BColors.IYELLOW}You've chosen to use Item!{BColors.ENDC}")
                choose_item(partybag)
                item_choice = int(input(f"{BColors.IYELLOW}Pick an item: {BColors.ENDC}")) - 1
                if item_choice == -1:
                    continue
                if partybag.items[item_choice]["quantity"] == 0:
                    print(f"{BColors.YELLOW}None left...{BColors.ENDC}")
                    continue
                item = partybag.items[item_choice]['item']
                print(f"{BColors.IYELLOW}You've chosen to use {item.name}!{BColors.ENDC}")
                spacer()
                if item.itype == "attack":
                    enemy = choose_enemy(enemies)
                    enemy.take_dmg(item.prop)
                    print(f"Your {item.name} did {item.prop} points of dmg to {enemy.name}!")
                    print(f"{enemy.name} HP is now {enemy.hp}.")
                elif item.itype == "grenade":
                    print(f"Your {item.name} damaged ALL enemies for {item.prop} points.")
                    for enemy in enemies:
                        if enemy.hp > 0:
                            enemy.take_dmg(item.prop)
                            print(f"{enemy.name} HP is now {enemy.hp}.")

                elif item.itype == "hpotion":
                    ally = choose_ally(party)
                    ally.heal(item.prop)
                    print(f"You healed {ally.name} for {item.prop} points.")
                    print(f"{ally.name} HP is now {ally.hp}.")
                elif item.itype == "mpotion":
                    ally = choose_ally(party)
                    ally.restmana(item.prop)
                    print(f"You restored {item.prop} mana to {ally.name}.")
                    print(f"{ally.name} MP is now {ally.mp}.")
                elif item.itype == "elixir":
                    for ally in party:
                        ally.heal(item.prop)
                        ally.restmana(item.prop)
                    print(f"You used magical elixir!")
                    print(f"{item.prop} HP/MP is now restored for all party members.")
            except:
                print(f"{BColors.YELLOW}Not a valid item! Try again.{BColors.ENDC}")
                continue
            else:
                partybag.items[item_choice]["quantity"] -= 1
                if partybag.items[item_choice]["quantity"] == 0:
                    partybag.items.remove(partybag.items[item_choice])
                break
        else:
            print(f"{BColors.IVIOLET}Not a valid choice! Try again.{BColors.ENDC}")
            continue


def enemy_action(enemy, party, enemies):
    if enemy.get_hp() > 0:
        turn = True
    else:
        turn = False

    if check_death(party):
        turn = False

    while turn:

        enemy_choice = random.randint(1, 10)

        if enemy_choice <= 5:
            while True:
                target = random.choice(party)
                if target.hp == 0:
                    continue
                else:
                    break
            edmg = enemy.gen_dmg(target)
            target.take_dmg(edmg)
            enemy.build_rage()
            en_spacer()
            print(f"{enemy.name} attacked {target.name} for {edmg} points of dmg!")
            print(f"{target.name} HP is now {target.hp}.")

        else:
            if enemy.klas not in ['Mage', 'Priest']:
                ability = enemy.mgk[random.randrange(0, len(enemy.mgk))]
                if ability.cost > enemy.rge:
                    continue
                admg = ability.gen_mdmg(enemy)
                if ability.stype == "ABlack":
                    while True:
                        target = random.choice(party)
                        if target.hp == 0:
                            continue
                        else:
                            break
                    target.take_dmg(admg)
                    enemy.rge -= ability.cost
                    en_spacer()
                    print(f"{enemy.name} used {ability.name} on {target.name} and did {admg} dmg.")
                    print(f"{target.name} HP is now {target.hp}.")
                elif ability.stype == "ARed":
                    print(f"{enemy.name} used {ability.name} and did {admg} dmg to the entire Party.")
                    for target in party:
                        if target.hp > 0:
                            target.take_dmg(admg)
                            print(f"{target.name} HP is now {target.hp}.")
                    enemy.rge -= ability.cost
                    en_spacer()

            else:
                spell = enemy.mgk[random.randrange(0, len(enemy.mgk))]
                if spell.cost > enemy.mp:
                    continue
                mdmg = spell.gen_mdmg(enemy)
                if spell.stype == "Black":
                    while True:
                        target = random.choice(party)
                        if target.hp == 0:
                            continue
                        else:
                            break
                    target.take_dmg(mdmg)
                    enemy.mp -= spell.cost
                    en_spacer()
                    print(f"{enemy.name} casted {spell.name} on {target.name} and did {mdmg} dmg.")
                    print(f"{target.name} HP is now {target.hp}.")
                elif spell.stype == "Red":
                    print(f"{enemy.name} casted {spell.name} on your entire party and did {mdmg} dmg.")
                    for target in party:
                        if target.hp > 0:
                            target.take_dmg(mdmg)
                            print(f"{target.name} HP is now {target.hp}.")
                    enemy.mp -= spell.cost
                    en_spacer()

                elif spell.stype == "White":
                    while True:
                        ally = random.choice(enemies)
                        counter = 0
                        if counter == len(enemies):
                            break
                        elif not ally.hp < ally.max_hp:
                            counter += 1
                            continue
                        else:
                            break
                    ally.heal(mdmg)
                    enemy.mp -= spell.cost
                    en_spacer()
                    print(f"{enemy.name} healed {ally.name} for {mdmg} points.")
                    print(f"{ally.name} HP is now {ally.hp}.")
                elif spell.stype == "Green":
                    print(f"{enemy.name} healed all enemies for {mdmg} points.")
                    for ally in enemies:
                        ally.heal(mdmg)
                        print(f"{ally.name} HP is now {ally.hp}.")
                    enemy.mp -= spell.cost
                    en_spacer()
        turn = False


def check_death(group):
    death_counter = 0
    for person in group:
        if person.get_hp() == 0:
            death_counter += 1
    if death_counter == len(group):
        return True
    else:
        return False


def gain_xp(party, xp):
    for partymember in party:
        partymember.xp += xp
        if partymember.xp >= partymember.max_xp:
            partymember.xp -= partymember.max_xp
            partymember.lvl += 1
            partymember.max_hp += 50
            partymember.max_mp += 25
            partymember.max_xp += 10
            partymember.atk_l += 5
            partymember.atk_h += 5
            partymember.defnd += 5
            print(f"{BColors.BOLD}{BColors.IGREEN}LVL UP! {partymember.name:10} "
                  f"reached lvl {partymember.lvl}.{BColors.ENDC}")


def drop_loot(bag, items):
    item = random.choice(items)
    count = random.randint(1, 3)
    coins = random.randint(50, 100)
    dropped_item = {"item": item, "quantity": count}
    print(f"{BColors.BOLD}Enemies dropped {BColors.YELLOW}{coins} Coins{BColors.ENDC} {BColors.BOLD}and "
          f"{BColors.IYELLOW}{dropped_item['item'].name} ({dropped_item['quantity']}x){BColors.ENDC}")
    for item in bag.items:
        if dropped_item["item"] == item["item"]:
            item["quantity"] += dropped_item["quantity"]
            break
    else:
        bag.items.append(dropped_item)
    bag.coins += coins


def shop(bag, sitems):
    spacer()
    caravan = "You've encountered a caravan, finally a chance to buy some items."
    print(f"{BColors.YELLOW}{BColors.ITAL}{caravan}{BColors.ENDC}")
    shopping = True
    while shopping:
        spacer()
        i = 1
        print(f'{BColors.YELLOW}{BColors.BOLD}ITEMS:{BColors.ENDC}')
        print(f"  0: Quit shop.")
        for item in sitems:
            print(f"  {str(i)}: {item['item'].name} - {item['item'].description} ({item['price']} Coins)")
            i += 1
        print(f"You currently have {BColors.YELLOW}{bag.coins} Coins.{BColors.ENDC}")
        item_choice = int(input(f"{BColors.YELLOW}Pick an item: {BColors.ENDC}")) - 1
        if item_choice == -1:
            spacer()
            leave = "The prices were too high and you didn't need more items anyway, so you left the shop."
            print(f"{BColors.YELLOW}{BColors.BOLD}{leave}{BColors.ENDC}")
            break
        if sitems[item_choice]['price'] > bag.coins:
            print(f"{BColors.YELLOW}Not enough coins...{BColors.ENDC}")
            continue

        price = sitems[item_choice]['price']
        item = sitems[item_choice]['item']
        bag.coins -= price
        bought_item = {"item": item, "quantity": 1}
        spacer()
        print(f"{BColors.BOLD}{BColors.YELLOW}You bought {item.name} for {price} Coins.{BColors.ENDC}")
        for item in bag.items:
            if bought_item["item"] == item["item"]:
                item["quantity"] += bought_item["quantity"]
                break
        else:
            bag.items.append(bought_item)


def logo():
    a = BColors.BBLUE
    b = BColors.BIBLUE
    c = BColors.BICYAN
    d = BColors.BCYAN
    e = BColors.BYELLOW
    f = BColors.BIGREEN
    g = BColors.BGREEN
    h = BColors.BDGREY
    j = BColors.BGREY
    z = BColors.ENDC

    print(f"{a}{114*' '}{z}")
    print(f"{a}{114*' '}{z}")
    print(f"{a}{6*' '}{j}{102*' '}{a}{6*' '}{z}")
    print(f"{a}{6*' '}{j}{3*' '}{h}{96*' '}{j}{3*' '}{a}{6*' '}{z}")
    print(f"{b}{6*' '}{j}{3*' '}{h}{9*' '}{b}{6*' '}{h}{9*' '}{b}{18*' '}{h}{3*' '}{b}{18*' '}{h}{3*' '}"
          f"{b}{18*' '}{h}{3*' '}{b}{6*' '}{h}{3*' '}{j}{3*' '}{b}{6*' '}{z}")
    print(f"{b}{6*' '}{j}{3*' '}{h}{6*' '}{b}{12*' '}{h}{6*' '}{b}{18*' '}{h}{3*' '}{b}{18*' '}{h}{3*' '}"
          f"{b}{18*' '}{h}{3*' '}{b}{6*' '}{h}{3*' '}{j}{3*' '}{b}{6*' '}{z}")
    print(f"{b}{6*' '}{j}{3*' '}{h}{6*' '}{b}{12*' '}{h}{12*' '}{b}{6*' '}{h}{9*' '}{b}{6*' '}{h}{6*' '}"
          f"{b}{6*' '}{h}{3*' '}{b}{6*' '}{h}{6*' '}{b}{6*' '}{h}{3*' '}{b}{6*' '}{h}{3*' '}{j}{3*' '}{b}{6*' '}{z}")
    print(f"{c}{6*' '}{j}{3*' '}{h}{3*' '}{c}{6*' '}{h}{6*' '}{c}{6*' '}{h}{9*' '}{c}{6*' '}{h}{9*' '}"
          f"{c}{6*' '}{h}{6*' '}{c}{6*' '}{h}{3*' '}{c}{6*' '}{h}{6*' '}{c}{6*' '}{h}{3*' '}{c}{6*' '}"
          f"{h}{3*' '}{j}{3*' '}{c}{6*' '}{z}")
    print(f"{c}{6*' '}{j}{3*' '}{h}{3*' '}{c}{6*' '}{h}{6*' '}{c}{6*' '}{h}{9*' '}{c}{6*' '}{h}{9*' '}"
          f"{c}{18*' '}{h}{3*' '}{c}{6*' '}{h}{6*' '}{c}{6*' '}{h}{3*' '}{c}{6*' '}{h}{3*' '}{j}{3*' '}{c}{6*' '}{z}")
    print(f"{c}{6*' '}{j}{3*' '}{h}{3*' '}{c}{18*' '}{h}{9*' '}{c}{6*' '}{h}{9*' '}{c}{15*' '}{h}{6*' '}"
          f"{c}{6*' '}{h}{6*' '}{c}{6*' '}{h}{3*' '}{c}{6*' '}{h}{3*' '}{j}{3*' '}{c}{6*' '}{z}")
    print(f"{d}{6*' '}{j}{3*' '}{h}{3*' '}{d}{18*' '}{h}{9*' '}{d}{6*' '}{h}{9*' '}{d}{15*' '}{h}{6*' '}"
          f"{d}{6*' '}{h}{6*' '}{d}{6*' '}{h}{3*' '}{d}{6*' '}{h}{3*' '}{j}{3*' '}{d}{6*' '}{z}")
    print(f"{d}{6*' '}{j}{3*' '}{h}{3*' '}{d}{6*' '}{h}{6*' '}{d}{6*' '}{h}{9*' '}{d}{6*' '}{h}{9*' '}"
          f"{d}{6*' '}{h}{6*' '}{d}{6*' '}{h}{3*' '}{d}{6*' '}{h}{6*' '}{d}{6*' '}{h}{12*' '}{j}{3*' '}{d}{6*' '}{z}")
    print(f"{e}{6*' '}{j}{3*' '}{h}{3*' '}{e}{6*' '}{h}{6*' '}{e}{6*' '}{h}{9*' '}{e}{6*' '}{h}{9*' '}"
          f"{e}{6*' '}{h}{6*' '}{e}{6*' '}{h}{3*' '}{e}{18*' '}{h}{3*' '}{e}{6*' '}{h}{3*' '}{j}{3*' '}{e}{6*' '}{z}")
    print(f"{f}{6*' '}{j}{3*' '}{h}{3*' '}{f}{3*' '}{h}{12*' '}{f}{3*' '}{h}{9*' '}{f}{6*' '}{h}{9*' '}"
          f"{f}{6*' '}{h}{9*' '}{f}{3*' '}{h}{3*' '}{f}{18*' '}{h}{3*' '}{f}{6*' '}{h}{3*' '}{j}{3*' '}{f}{6*' '}{z}")
    print(f"{f}{6*' '}{j}{3*' '}{h}{96*' '}{j}{3*' '}{f}{6*' '}{z}")
    print(f"{g}{6*' '}{j}{102*' '}{g}{6*' '}{z}")
    print(f"{g}{114*' '}{z}")
    print(f"{g}{114*' '}{z}")