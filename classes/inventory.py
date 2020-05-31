

class Item:

    def __init__(self, name, itype, description, prop):
        self.name = name
        self.itype = itype
        self.description = description
        self.prop = prop

    def __str__(self):
        return f"{self.name}"


class Bag:

    def __init__(self, items):
        self.items = items
        self.coins = 100

