import random


class Spell:
    def __init__(self, name, cost, dmg, stype):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.stype = stype

    def gen_mdmg(self, user):
        mgk_l = self.dmg - 15 + (user.lvl*50)
        mgk_h = self.dmg + 15 + (user.lvl*50)
        return random.randint(mgk_l, mgk_h)

