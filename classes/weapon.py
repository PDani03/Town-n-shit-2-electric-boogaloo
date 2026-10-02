import random
from .entity import Entity
from .enemy import Enemy


class Weapon:
    def __init__(self, value, type, equipped=False):
        self.value=value
        self.type=type
        self.equipped=equipped
        self.prefix=self.determinePrefix()
        self.sell_value=self.determineSellValue()
    
    def determinePrefix(self):
        val = self.value
        if val<1.3:
            return "dogshit"
        elif val<1.65:
            return "decent"
        elif val<2.1:
            return "good"
        elif val <2.7:
            return "great"
        else:
            return "legendary"
    
    def getWeaponString(self):
        return f"{self.prefix} {self.type}, {self.value}x"
    
    def determineSellValue(self):
        return int(self.value*self.value*14)

def makeWeapons(diff,enemy,guarantee=False):
    max = enemy.weapon_amount_max
    loot = enemy.loot
    guarantee = "boss" in enemy.name if guarantee==False else guarantee
    weapons=[]
    for i in loot:

        if guarantee:
            weapons.append(Weapon(determineQuality(diff), i))

        for j in range(max-guarantee):
            if random.randint(1,2)==1:
                weapons.append(Weapon(determineQuality(diff), i))

    return weapons


def determineQuality(quality): #quality = diff

    #upgrade chance
    if random.randint(1,10)==1:
        quality+=5

    expected = 1 + quality * 0.05
    return round(max(1, random.gauss(expected, expected * 0.1)),2)
    