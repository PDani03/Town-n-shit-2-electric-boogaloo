from .entity import Entity
import random

class Enemy(Entity):
    def __init__(self, *args, name, loot, weapon_amount_max, diff=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.name=name
        self.loot=loot
        self.weapon_amount_max=weapon_amount_max
        self.diff=diff
        #diff determines weapon quality, weapon_amount_max determines how many weapons you will get (between 1 and weapon_amount_max)
    
    def applyGameDiff(self, game_diff):
        for key in self.actuals:
            self.actuals[key] *= game_diff
    
    def applyPlayerWeapon(self, wpn):
        match wpn.type:
            case "club":
                self.actuals["df"]=0
                self.bases["df"]=0

def makeEnemy(diff, boss=False):

    types={
        "Goblin":lambda:Enemy(15, 2, 1, name="Goblin", loot=["sword"], weapon_amount_max=1),
        "Bandit":lambda:Enemy(30, 4, 2, name="Bandit", loot=["shield","sword"], weapon_amount_max=2),
        "Kobold":lambda:Enemy(20, 6, 1, name="Kobold", loot=["bow","dagger"], weapon_amount_max=3),
        "Orc":lambda:Enemy(70, 6, 5, name="Orc", loot=["potion","club"], weapon_amount_max=4),
        "Varga Gyula":lambda:Enemy(100, 15, 10, name="Varga Gyula", loot=["sword","shield","dagger","bow","potion","club"], weapon_amount_max=6)
    }

    enemy_index=0
    for i in range(diff):
        if random.randint(1,20)==1:
            enemy_index+=1
    
    if boss:
        enemy_index=int(diff/10)-1

    enemy_index = min(enemy_index, len(types) - 1)

    enemy_name = list(types.keys())[enemy_index]
    enemy = types[enemy_name]()

    enemy_stat_multiplier = 1 + diff/10 + 0.5*diff*boss

    enemy.diff=diff
    enemy.actuals["hp"] = enemy.bases["hp"] * enemy_stat_multiplier *0.8
    enemy.actuals["dmg"] = enemy.bases["dmg"] * enemy_stat_multiplier *1.2
    enemy.actuals["df"] = enemy.bases["df"] * enemy_stat_multiplier *1.2

    if boss:
        enemy.name += " boss"
        
    return enemy