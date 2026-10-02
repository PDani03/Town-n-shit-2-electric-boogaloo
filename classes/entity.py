import random

class Entity:
    def __init__(self, hp, dmg, df, is_guarding=False):
        self.bases={
            "hp":hp,
            "dmg":dmg,
            "df":df
        }

        self.actuals={
            "hp":hp,
            "dmg":dmg,
            "df":df
        }

        self.current_hp=hp

        self.is_guarding=is_guarding
    
    def fullHeal(self):
        self.current_hp=self.actuals["hp"]

    def updateActuals(self):
        for key in self.actuals:
            if self.actuals[key] < self.bases[key]:
                self.actuals[key] = self.bases[key]
    
    def resetActuals(self):
        for key in self.actuals:
            self.actuals[key] = self.bases[key]

    def clampActuals(self):
        for key in self.actuals:
            self.actuals[key] = round(self.actuals[key],2)
        self.current_hp = round(self.current_hp,2)

    def takeDamage(self, incoming):
        defence=self.actuals["df"]
        if self.is_guarding:
            defence = (defence + 2)*1.7

        damage = round(incoming * (incoming / (incoming + defence*1.5)),2)
        damage = 0 if incoming<=0 else damage
        self.current_hp -= damage
        return damage
    
    def calcDamageOut(self):        
        return round(self.actuals["dmg"] * random.randint(80,120)/100,2)