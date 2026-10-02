from .entity import Entity

class Character(Entity): 
    def __init__(self, acc, pot, *args, weapons=None, armor=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.bases["acc"]=acc
        self.bases["pot"]=pot

        self.actuals["acc"]=acc
        self.actuals["pot"]=pot

        self.upgrade_amounts={
            "dmg":1,
            "df":1,
            "acc":0.07,
            "pot":1
        }

        self.upgrade_price_scaling={
            "dmg":1.5,
            "df":1.5,
            "acc":1.2,
            "pot":5
        }

        self.weapons = weapons if weapons is not None else []
        self.armor = armor if armor is not None else []

        self.equipped_wpn=self.getEquippedWeapon()
    
    def calcDamageOut(self):
        return super().calcDamageOut() * self.actuals["acc"]
    
    def updateActuals(self):
        for key in self.actuals:
            if self.actuals[key] < self.bases[key]:
                self.actuals[key] = self.bases[key]
        self.applyWeaponAttribute()

    def applyWeaponAttribute(self):
        equipped_wpn=False
        for i in self.weapons:
            if i.equipped:
                equipped_wpn=i

        if equipped_wpn:
            match equipped_wpn.type:
                case "sword":
                    self.actuals["dmg"] = self.bases["dmg"] * equipped_wpn.value
                case "shield":
                    self.actuals["df"] = self.bases["df"] * equipped_wpn.value
                case "dagger":
                    self.actuals["dmg"] = self.bases["dmg"] * equipped_wpn.value * 1.2
                    self.actuals["df"] = self.bases["df"] * 0.8
                case "bow":
                    self.actuals["acc"] = self.bases["acc"] * equipped_wpn.value * 0.9
                case "potion":
                    self.actuals["pot"] = self.bases["pot"] + round((equipped_wpn.value-1)*5) 
                case "club":
                    self.actuals["dmg"] = self.bases["dmg"] * equipped_wpn.value * 0.7
        
        self.clampActuals()
    
    def getEquippedWeapon(self):
        equipped_wpn=None
        for i in self.weapons:
            if i.equipped:
                equipped_wpn=i
        return equipped_wpn

    def listWeapons(self):
        self.sortWeaponsByType()
        self.sortWeaponsByValue()
        self.sortWeaponsByType()
        index=0
        for i in self.weapons:
            index+=1
            print(f"{'> ' if i.equipped else ''}{index}. {i.getWeaponString()}")
    
    def sortWeaponsByType(self):
        types_in_order=["sword","shield","dagger","bow","potion","club"]
        sorted=False
        while not sorted:
            sorted=True
            for index in range(len(self.weapons)):
                if index<len(self.weapons)-1:
                    current=self.weapons[index]
                    next=self.weapons[index+1]

                    if types_in_order.index(current.type)>types_in_order.index(next.type):
                        self.weapons[index] = next
                        self.weapons[index+1] = current
                        sorted=False
    
    def sortWeaponsByValue(self):
        sorted=False
        while not sorted:
            sorted=True
            for index in range(len(self.weapons)):
                if index<len(self.weapons)-1:
                    current=self.weapons[index]
                    next=self.weapons[index+1]

                    if current.value>next.value:
                        self.weapons[index] = next
                        self.weapons[index+1] = current
                        sorted=False
    
    
    
    