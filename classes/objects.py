import math
import random
import copy

from classes.color import BColors
from classes.magic import Spell
from classes.game import spacer
from classes.inventory import Item


class Character:

    def __init__(self, name, klas, hp, mp, atk, defnd, mgk, actions, lvl=1, xp=0, rge=0, callout=""):
        self.name = name
        self.callout = callout
        self.klas = klas
        self.lvl = lvl
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atk_h = atk + 10
        self.atk_l = atk - 10
        self.defnd = defnd
        self.mgk = mgk
        self.actions = actions
        self.rge = rge
        self.max_rge = 100
        self.xp = xp
        self.max_xp = 100

    def gen_dmg(self, target):
        dmg = random.randint(self.atk_l, self.atk_h) + ((self.lvl - 1) *5) - target.defnd
        if dmg > 0:
            return dmg
        else:
            return 0

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        return self.hp

    def restmana(self, dmg):
        self.mp += dmg
        if self.mp > self.max_mp:
            self.mp = self.max_mp
        return self.mp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def cur_hp(self):
        return f'{self.hp}/{self.max_hp}'

    def hp_bar_color(self):
        if self.hp/self.max_hp > 0.7:
            return BColors.BIGREEN
        elif self.hp/self.max_hp < 0.4:
            return BColors.BIRED
        else:
            return BColors.BIYELLOW

    def hp_per(self):
        return math.ceil(36*self.hp/self.max_hp)

    def hp_pere(self):
        return 36-math.ceil(36*self.hp/self.max_hp)

    def draw_name(self, name, color):
        print(f"{BColors.BOLD}{BColors.BGREY + ' '}{BColors.BDGREY}{color}{name+' ('+str(self.klas)+')':^24}" +
              f"{BColors.BGREY + ' '}{BColors.ENDC}", end='   ')

    def draw_hp(self):
        print(f"{BColors.BOLD}{BColors.BGREY + ' '}{BColors.DGREY}{self.hp_bar_color()}" +
              f"{self.cur_hp():^11}{BColors.ENDC}", end='')
        print(f"{BColors.BGREY + ' '}{BColors.BDGREY}{self.hp_pere() * ' '}{self.hp_bar_color()}{self.hp_per() * ' '}"
              f"{BColors.BGREY + ' '}{BColors.ENDC}", end='   ')

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def cur_mp(self):
        return f'{self.mp}/{self.max_mp}'

    def reduce_mp(self, cost):
        self.mp -= cost

    def mp_bar_color(self):
        if self.mp / self.max_mp > 0.7:
            return BColors.BCYAN
        elif self.mp / self.max_mp < 0.4:
            return BColors.BBLUE
        else:
            return BColors.BIBLUE

    def mp_per(self):
        return math.ceil(18*self.mp/self.max_mp)

    def mp_pere(self):
        return 18-math.ceil(18*self.mp/self.max_mp)

    def draw_mp(self):
        if self.max_mp > 15:
            print(f"{BColors.BOLD}{BColors.FG}{BColors.BGREY + ' '}{self.mp_bar_color()}" +
                  f"{self.cur_mp():^11}{BColors.ENDC}", end='')
            print(f"{BColors.BGREY + ' '}{BColors.BDGREY}{self.mp_pere() * ' '}{self.mp_bar_color()}"
                  f"{self.mp_per() * ' '}{BColors.BGREY + ' '}{BColors.ENDC}")
        else:
            print(' ')

    def get_rge(self):
        return self.rge

    def cur_rge(self):
        return f'{self.rge}/{self.max_rge}'

    def build_rage(self):
        self.rge += 20
        if self.rge > self.max_rge:
            self.rge = self.max_rge
        return self.rge

    def rge_per(self):
        return 18*self.rge//self.max_rge

    def rge_pere(self):
        return 18-(18*self.rge//self.max_rge)

    def rge_bar_color(self):
        if self.rge/self.max_rge > 0.7:
            return BColors.BIVIOLET
        else:
            return BColors.BVIOLET

    def draw_rge(self):
        print(f"{BColors.BOLD}{BColors.FG}{BColors.BGREY + ' '}{self.rge_bar_color()}" +
              f"{self.cur_rge():^11}{BColors.ENDC}", end='')
        print(f"{BColors.BGREY + ' '}{self.rge_bar_color()}{self.rge_per() * ' '}"
              f"{BColors.BDGREY}{self.rge_pere() * ' '}{BColors.BGREY + ' '}{BColors.ENDC}")

    def cur_xp(self):
        return f'{self.xp}/{self.max_xp}'

    def xp_per(self):
        return 70*self.xp//self.max_xp

    def xp_pere(self):
        return 70-(70*self.xp//self.max_xp)

    def draw_xp(self):
        print(f"{BColors.BOLD}{BColors.BGREY + ' '}{BColors.BDGREY}{BColors.YELLOW}"
              f"{f'EXPERIENCE (LVL {self.lvl})':^24}{BColors.BGREY + ' '}{BColors.ENDC}", end='  ')
        print(f"{BColors.BOLD}{BColors.DGREY}{BColors.BGREY + ' '}{BColors.BYELLOW}" +
              f"{self.cur_xp():^11}{BColors.ENDC}", end='')
        print(f"{BColors.BGREY + ' '}{BColors.BYELLOW}{self.xp_per() * ' '}{BColors.BDGREY}{self.xp_pere() * ' '}"
              f"{BColors.BGREY + ' '}{BColors.ENDC}")

    def draw_status(self):
        self.draw_name(self.name, BColors.IGREEN)
        self.draw_hp()
        if self.klas in ['Mage', 'Priest']:
            self.draw_mp()
        else:
            self.draw_rge()

    def draw_enstatus(self):
        self.draw_name(self.name, BColors.RED)
        self.draw_hp()
        if self.klas in ['Mage', 'Priest']:
            self.draw_mp()
        else:
            self.draw_rge()

    def choose_action(self):
        i = 1
        print(f'{BColors.IGREEN}{BColors.BOLD}ACTIONS:{BColors.ENDC}')
        for action in self.actions:
            print(f" {str(i)}: {action}")
            i += 1

    def choose_magic(self):
        i = 1
        print(f'{BColors.IBLUE}{BColors.BOLD}MAGIC:{BColors.ENDC}')
        for spell in self.mgk:
            print(f"  {str(i)}: {spell.name} (cost: {spell.cost}, strength: {spell.dmg+self.lvl*50})")
            i += 1

    def choose_ability(self):
        i = 1
        print(f'{BColors.VIOLET}{BColors.BOLD}ABILITIES:{BColors.ENDC}')
        for ability in self.mgk:
            print(f"  {str(i)}: {ability.name} (cost: {ability.cost}, strength: {ability.dmg+self.lvl*50})")
            i += 1


# black magic
fire = Spell("Fire", 10, 150, "Black")
thunder = Spell("Thunder", 20, 300, "Black")
meteor = Spell("Meteor", 40, 600, "Black")
# red magic
blizzard = Spell("Blizzard - AoE", 30, 300, "Red")
quake = Spell("Earth Quake - AoE", 50, 500, "Red")
# white magic
cure = Spell("Cure", 10, 150, "White")
curea = Spell("Super Cure", 20, 400, "White")
# green magic
cureaoe = Spell("Healing Rays - AoE", 30, 200, "Green")
# abilities
heavyat = Spell("Heavy Attack", 20, 300, "ABlack")
dcut = Spell("Deep Cut", 10, 300, "ABlack")
bstab = Spell("Backstab", 20, 800, "ABlack")
spin = Spell("Whirlwind - AoE", 30, 300, "ARed")
# enemy abilities/spells
smash = Spell("Smashyy Smash", 20, 200, "ABlack")
stomp = Spell("Stompyy Stomp", 40, 200, "ARed")
spit = Spell("Spit", 20, 150, "ABlack")
puke = Spell("Puke", 40, 150, "ARed")
rockt = Spell("Rock Throw", 20, 100, "ABlack")
noise = Spell("Deafening Squeak", 40, 100, "ARed")
# items
hpotion = Item("Health Potion", "hpotion", "Heals 100 HP", 100)
hbigpotion = Item("Big Health Potion", "hpotion", "Heals 250 HP", 250)
hsuppotion = Item("Super Health Potion", "hpotion", "Heals 500 HP", 500)
mpotion = Item("Mana Potion", "mpotion", "Restores 100 MP", 50)
mbigpotion = Item("Big Mana Potion", "mpotion", "Restores 250 MP", 250)
msuppotion = Item("Super Mana Potion", "mpotion", "Restores 500 MP", 500)
elixir = Item("Elixir", "elixir", "Restores 200 HP/MP of all characters", 200)
bigelixir = Item("Big Elixir", "elixir", "Fully restores HP/MP of all characters", 9999)

grenade = Item("Powder Bomb", "grenade", "Deals 400 dmg to all enemies", 400)

items_list = [hpotion, hbigpotion, hsuppotion, mpotion, mbigpotion, msuppotion, elixir, bigelixir, grenade]
# bag
plitems = [{"item": hpotion, "quantity": 4}, {"item": hsuppotion, "quantity": 4},
           {"item": mpotion, "quantity": 4}, {"item": mbigpotion, "quantity": 4},
           {"item": elixir, "quantity": 4}, {"item": grenade, "quantity": 4}]

shop_items = [{"item": hpotion, "price": 20}, {"item": hbigpotion, "price": 30},
           {"item": mpotion, "price": 20}, {"item": mbigpotion, "price": 30},
           {"item": elixir, "price": 40}, {"item": grenade, "price": 40}]

# characters
mage_magic = [fire, thunder, meteor, blizzard, quake]
mage = {'klas': 'Mage', 'health': 450, 'mana': 100, 'attack': 60, 'defence': 35,
        'spells': mage_magic, 'actions': ["Attack", "Magic", "Items"]}

priest_magic = [cure, curea, cureaoe]
priest = {'klas': 'Priest', 'health': 450, 'mana': 100, 'attack': 60, 'defence': 35,
          'spells': priest_magic, 'actions': ["Attack", "Magic", "Items"]}

warrior_magic = [heavyat, spin]
warrior = {'klas': 'Warrior', 'health': 900, 'mana': 10, 'attack': 120, 'defence': 60,
           'spells': warrior_magic, 'actions': ["Attack", "Abilities", "Items"]}

rogue_magic = [dcut, bstab]
rogue = {'klas': 'Rogue', 'health': 350, 'mana': 10, 'attack': 240, 'defence': 35,
         'spells': rogue_magic, 'actions': ["Attack", "Abilities", "Items"]}

klasses = [['Mage', mage], ['Priest', priest], ['Warrior', warrior], ['Rogue', rogue]]


def choose_klas(classes):
    i = 1
    print(f'{BColors.IGREEN}{BColors.BOLD}CLASSES:{BColors.ENDC}')
    for item in classes:
        print(f"  {str(i)}: {item[0]}")
        i += 1
    klasa = int(input(f"{BColors.IGREEN}Pick a character class: {BColors.ENDC}")) - 1
    try:
        return classes[klasa][1]
    except:
        return classes[0][1]


def create_party():
    spacer()
    print(f"{BColors.IGREEN}{BColors.ITAL}You must create your party before venturing forth.{BColors.ENDC}")
    spacer()
    print(f'{BColors.IGREEN}{BColors.BOLD}PARTY CREATION:{BColors.ENDC}')
    print('  1: Create own Party')
    print('  2: Premade Party')
    party_choice = int(input(f"{BColors.IGREEN}Decide: {BColors.ENDC}"))
    if party_choice == 1:
        print(f'{BColors.IGREEN}{BColors.BOLD}You decided to create your own party.{BColors.ENDC}')
        play1n = str(input(f"{BColors.IGREEN}Enter name of first Party Member: {BColors.ENDC}"))
        play1k = choose_klas(klasses)
        play2n = str(input(f"{BColors.IGREEN}Enter name of second Party Member: {BColors.ENDC}"))
        play2k = choose_klas(klasses)
        play3n = str(input(f"{BColors.IGREEN}Enter name of third Party Member: {BColors.ENDC}"))
        play3k = choose_klas(klasses)
        play4n = str(input(f"{BColors.IGREEN}Enter name of fourth Party Member: {BColors.ENDC}"))
        play4k = choose_klas(klasses)

        play1 = Character(play1n, play1k['klas'], play1k['health'], play1k['mana'],
                          play1k['attack'], play1k['defence'], play1k['spells'], play1k['actions'])
        play2 = Character(play2n, play2k['klas'], play2k['health'], play2k['mana'],
                          play2k['attack'], play2k['defence'], play2k['spells'], play2k['actions'])
        play3 = Character(play3n, play3k['klas'], play3k['health'], play3k['mana'],
                          play3k['attack'], play3k['defence'], play3k['spells'], play3k['actions'])
        play4 = Character(play4n, play4k['klas'], play4k['health'], play4k['mana'],
                          play4k['attack'], play4k['defence'], play4k['spells'], play4k['actions'])

    else:
        print(f'{BColors.IGREEN}{BColors.BOLD}You decided to use a party composed of local vagrants.{BColors.ENDC}')
        play1k = mage
        play2k = priest
        play3k = warrior
        play4k = rogue

        play1 = Character("Vukain", play1k['klas'], play1k['health'], play1k['mana'],
                          play1k['attack'], play1k['defence'], play1k['spells'], play1k['actions'])
        play2 = Character("Pirak", play2k['klas'], play2k['health'], play2k['mana'],
                          play2k['attack'], play2k['defence'], play2k['spells'], play2k['actions'])
        play3 = Character("Conhen", play3k['klas'], play3k['health'], play3k['mana'],
                          play3k['attack'], play3k['defence'], play3k['spells'], play3k['actions'])
        play4 = Character("Azgot", play4k['klas'], play4k['health'], play4k['mana'],
                          play4k['attack'], play4k['defence'], play4k['spells'], play4k['actions'])
    spacer()
    adventure = "...and so the fellowship leaves the city.\nThe adventure... or death awaits."
    print(f"{BColors.IGREEN}{BColors.ITAL}{adventure}{BColors.ENDC}")
    return [play1, play2, play3, play4]


def create_enemies():
    trol_abi = [smash, stomp]
    trol1 = Character("Oldeyyyy", 'Troll', 4800, 65, 120, 35, trol_abi, [], callout="Trolls")
    trol2 = Character("Boldeyyy", 'Troll', 4600, 65, 120, 35, trol_abi, [])
    trol3 = Character("Coldeyyy", 'Troll', 4400, 65, 120, 35, trol_abi, [])
    gob_abi = [spit, puke]
    gobl1 = Character("Alz", 'Goblin', 2200, 65, 160, 25, gob_abi, [], callout="Goblins")
    gobl2 = Character("Coz", 'Goblin', 2200, 65, 160, 25, gob_abi, [])
    gobl3 = Character("Hoz", 'Goblin', 2200, 65, 160, 25, gob_abi, [])
    gobl4 = Character("Likz", 'Goblin', 2200, 65, 160, 25, gob_abi, [])
    kob_abi = [rockt, noise]
    kob1 = Character("Hnugh", 'Kobold', 1600, 65, 100, 15, kob_abi, [], callout="Kobolds")
    kob2 = Character("Hnughey", 'Kobold', 1600, 65, 100, 15, kob_abi, [])
    kob3 = Character("Hnugheygh", 'Kobold', 1600, 65, 100, 15, kob_abi, [])
    kob4 = Character("Henry", 'Kobold', 1600, 65, 100, 15, kob_abi, [])

    enemy_list = [[trol1, trol2, trol3], [gobl1, gobl2, gobl3, gobl4], [kob1, kob2, kob3, kob4]]
    chosen_enemies = random.choice(enemy_list)
    return chosen_enemies


def boss(source):
    mir0, mir1, mir2, mir3 = None, None, None, None
    mirror = [mir0, mir1, mir2, mir3]
    idx = 0
    for partymember in source:
        mirror[idx] = copy.deepcopy(partymember)
        mirror[idx].name = mirror[idx].name[::-1].capitalize()
        mirror[idx].callout = "Mirror"
        mirror[idx].xp = 120
        idx += 1
    mirror.reverse()
    return mirror


story = {"Trolls": {"start": "While walking through a barren wasteland, you noticed three big rocks close to each other"
                             ".\nFinally a place to rest in a shadow!\nWhen you stood close to the biggest rock "
                             "trying to choose the best spot for the camp...\n"
                             "Suddenly it shaken and moved a bit.\n"
                             "Those aren't rocks, those are Mountain Trolls you genius...",
                    "ending": "All Trolls are now stone cold and they still cast a nice shadow...",
                    "killed": "The terrain excluding the 3 big rocks is flat again, just like your party.",
                    "xp": 100},
         "Goblins": {"start": "While walking through a forest you saw a fire shimmering between the trees.\n"
                              "Since it was a cold dusk, you decided to walk closer and check, if people near "
                              "the fire didn't need a company to drink with.\n"
                              "With immeasurable sadness you discovered that the fire was surrounded by "
                              "Drunk Goblins which didn't look friendly at all.\n"
                              "Oh well, you got noticed - \"Ghiev ouz allll yourzzzie booooz, nowzzzz!\"\n"
                              "You looked at your companions... and saw determination on their faces with"
                              " an unanimous answer in their eyes. NEVER!",
                     "ending": "Well... those Goblins won't need the fire and the booze anymore...",
                     "killed": "You lost your lives and on top of that, you lost your booze. Goblin Party!",
                     "xp": 80},
         "Kobolds": {"start": "While traversing the cave you heard some distant noises.\n"
                              "\"Hnugh.. hgryfffttt... HNUGH, HNUGHHHH!\"\n"
                              "Kobolds... noisy, stinky Kobolds...",
                     "ending": "Sweet silence, no more \"hnugh, hnugh\".",
                     "killed": "HNUGH, HNUGH, HNUUUUUUUUGH! Happily the sounds don't disturb you anymore, "
                               "nothing does.",
                     "xp": 60},
         "Mirror": {"start": "While exploring the ruins something shiny glimpsed in the darkness.\n"
                             "As you came closer, you realized it was a big mirror surrounded by a silver, "
                             "engraved frame.\nYou stared at the reflection of your face and said "
                             "\"Hello there handsome one\".\n\"Hello\" answered your reflection and started laughing, "
                             "as the reflections of your party stepped out of the mirror.\n"
                             "Oh well, a Magic Mirror, sadly the world isn't big enough for more than one of you.",
                    "ending": "You just killed...yourselves, kinda strange.",
                    "killed": "Unluckily for you, the one that survived wasn't the real one.",
                    "xp": 120}}
