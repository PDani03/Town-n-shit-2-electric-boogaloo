import random, pickle
from classes.character import Character
from classes.weapon import Weapon, makeWeapons
from classes.enemy import Enemy, makeEnemy
from classes.choicetoarea import choiceToArea

class GameState:
    def __init__(self):
        self.game_diff=1 # 3 * 0.25 + 0.25
        self.name=""
        self.upgrade_prices=[20,20,50,10]
        self.money = 10
        self.player = Character(1,0,100,4,1) #alap: acc 1, pot 0, hp 100, dmg 4, df 2
    
    def clampUpgradePrices(self):
        self.upgrade_prices = [round(price, 2) for price in self.upgrade_prices]
    
    def shortDescription(self):
        if self.name:
            return f"{self.name}, {self.gameDiffToString()}; money: {self.money}, damage: {self.player.bases['dmg']}, number of weapons: {len(self.player.weapons)}"
        else:
            return "New"
    
    def gameDiffToString(self, diff=None):
        diff = self.game_diff if diff==None else diff
        match diff:
            case 0.5:
                return "Easiest"
            case 0.75:
                return "Easier"
            case 1:
                return "Medium (default)"
            case 1.25:
                return "Hard"
            case 1.5:
                return "Harder"
    
    def applyGameDiff(self):
        self.upgrade_prices = [price * self.game_diff for price in self.upgrade_prices]
        for key in self.player.upgrade_price_scaling:
            self.player.upgrade_price_scaling[key] *= self.game_diff
            self.player.upgrade_price_scaling[key] = max(1, self.player.upgrade_price_scaling[key])


def save_game(state, save_number):
    filename="save"+str(save_number)+".dat"
    with open(filename, "wb") as f:
        pickle.dump(state, f)

def load_game(save_number) -> GameState:
    filename="save"+str(save_number)+".dat"
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return GameState()

def load_files():
    files=[]
    for i in range(4):
        files.append(load_game(i))
    return files


def mely(max=99999999,szoveg="Incorrect value, try again."):
    inputt=input("Choose: ")
    try:
        inputt=int(inputt)
        if max>=inputt:
            return inputt
    except:
        pass

    if inputt=="":
        return 1
    print(szoveg)
    return mely(max,szoveg)


def info(area,choice=False,wpn_to_be_sold=False):
    if choice:
        area=choiceToArea(State,area,choice,wpn_to_be_sold)
    print()
    match area:

        case "home":
            save_game(State, current_save_file_index)
            State.player.current_hp=State.player.actuals["hp"]
            State.player.resetActuals()
            print("Game saved, hp restored.")
            print(f"\033[30;43mmoney: {State.money}\033[30;40m")
            print("\033[32m- - - - - - - Town - - - - - - -")
            print("1. Shop")
            print("2. Weapons")
            print("3. Stats") #actual stuff, num of potions, upgrade costs
            print("4. Adventure")
            print("5. Quit\033[37m")

        case "shop":
            print(f"\033[30;43mmoney: {State.money}\033[30;40m")
            print("\033[33m- - - - - - - Shop - - - - - - -")
            print("1. Upgrade damage")
            print("2. Upgrade defense")
            print("3. Upgrade accuracy")
            print("4. Purchase more potions")
            print("5. Sell weapon")
            print("6. Back\033[37m")
        
        case "char_weapons":
            print("\033[32m- - - - - - - Equip a weapon - - - - - - -")
            State.player.listWeapons()
            print(f"{len(State.player.weapons)+1}. Back\033[37m")

        case "char_stats":
            State.player.updateActuals()
            print("\033[32m- - - - - - - Stats - - - - - - -")
            print(f"money: {State.money}")
            print(f"max hp: {State.player.actuals['hp']}")
            print(f"base, actual damage: {State.player.bases['dmg']}, {State.player.actuals['dmg']}")
            print(f"base, actual defense: {State.player.bases['df']}, {State.player.actuals['df']}")
            print(f"base, actual accuracy: {State.player.bases['acc']}, {State.player.actuals['acc']}")
            print(f"base, actual potions: {State.player.bases['pot']}, {State.player.actuals['pot']}")
            print("1. Back\033[37m")

        case "upgrade_dmg":
            print(f"\033[30;43mmoney: {State.money}\033[30;40m")
            print("\033[33m- - - - - - - Upgrade damage - - - - - - -")
            print(f"1. Upgrade ({State.upgrade_prices[0]})")
            print("2. Back\033[37m")
        
        case "upgrade_def":
            print(f"\033[30;43mmoney: {State.money}\033[30;40m")
            print("\033[33m- - - - - - - Upgrade defense - - - - - - -")
            print(f"1. Upgrade ({State.upgrade_prices[1]})")
            print("2. Back\033[37m")

        case "upgrade_acc":
            print(f"\033[30;43mmoney: {State.money}\033[30;40m")
            print("\033[33m- - - - - - - Upgrade accuracy - - - - - - -")
            print(f"1. Upgrade ({State.upgrade_prices[2]})")
            print("2. Back\033[37m")

        case "upgrade_pot":
            print(f"\033[30;43mmoney: {State.money}\033[30;40m")
            print("\033[33m- - - - - - - Purchase more potions - - - - - - -")
            print(f"1. Buy one more ({State.upgrade_prices[3]})")
            print("2. Back\033[37m")
        
        case "sell_wpn":
            print("\033[33m- - - - - - - Sell a weapon - - - - - - -")
            State.player.listWeapons()
            print(f"{len(State.player.weapons)+1}. Back\033[37m")
        
        case "q_sell_wpn": # question sell wpn: "are you sure?"
            wpn_to_be_sold=State.player.weapons[choice-1]
            print("\033[33m- - - - - - - Are you sure? - - - - - - -")
            print(f"1. Sell {wpn_to_be_sold.getWeaponString()} ({wpn_to_be_sold.sell_value})")
            print("2. Back\033[37m")

    return area, wpn_to_be_sold
print()

print("Accounts:")
save_files=load_files()
place_index=1
for i in save_files:
    print(f"{place_index}. {i.shortDescription()}")
    place_index+=1

current_save_file_index=mely(4)-1


State=load_game(current_save_file_index)
#State=GameState()


if State.name=="":
    State.name=input("New account detected, input account name (cant be changed (yet)): ")
    print("Choose difficulty:")
    for i in range(5):
        print(str(i+1)+".",State.gameDiffToString((i+1)*0.25+0.25))
    State.game_diff=mely(5)*0.25+0.25
    State.applyGameDiff()


welcome_message=f"Welcome, {State.name}!"
match State.name.lower():
    case "oroszi":
        welcome_message="Szopd ki a gecim"
    case "anyad" | "kurvaanyad" | "kurva anyad":
        welcome_message="Faszt tettem veled? Kurva anyád!"

input(welcome_message)

area="home"
choice=False
wpn_to_be_sold=False
info(area, choice, wpn_to_be_sold)

#print("\033[0;32;40mNormal text")

#State.player.weapons=makeWeapons(30,Enemy(100, 15, 10, name="Varga Gyula", loot=["club"], weapon_amount_max=3),True)

run=True
while run:
    choice=mely()

    State.money=round(State.money, 2)
    State.player.updateActuals()
    area, wpn_to_be_sold=info(area, choice, wpn_to_be_sold)

    if area=="quit":
        run=False
    
    if area=="adventure_start":

        places= ["\033[32mplains\033[37m","\033[32mforest\033[37m","\033[30mcave\033[37m","\033[36mriverside\033[37m"]
        place=random.choice(places)
        place_index=places.index(place)
        input(f"You walk into a {place}.")
        string=""
        match place_index:
            case 0:
                string="You feel the sun on your face, giving you strength! (1.5x damage, gain more focus when guarding)"
                State.player.actuals["dmg"]*=1.5
            case 1:
                string="The sounds of the forest harden your resolve! (1.5x defense, better weapons found)"
                State.player.actuals["df"]*=1.5
            case 2:
                string="The quiet of the cave makes it easier to focus! (1.5x accuracy, slower focus loss)"
                State.player.actuals["acc"]*=1.5
            case 3:
                string="The splashing of the river heals your soul! (1.3x max hp, more healing from potions)"
                State.player.actuals["hp"]*=1.3
        State.player.clampActuals()
        State.player.fullHeal()
        input(string)

        diff=0
        adventure=True
        
        while adventure and diff<=50:
            diff+=1

            enemies=[]
            boss=False
            if diff%10==0:
                boss=True
            
            else:
                for i in range(0,9): #9 max enemy, hogy az 1 garantáltal együtt legyen 10 max
                    if random.randint(0,6) == 0 or random.randint(0,6) == int((diff-1)/50*6):
                        enemies.append(makeEnemy(diff))

            enemies.append(makeEnemy(diff,boss))
            
            if not boss:
                enemies.append("Flee")

            while len(enemies)>1 or (len(enemies)>0 and boss):
                
                print()
                print(f"\033[37;41mHealth: {State.player.current_hp:.2f}\033[37;40m")
                print(f"\033[35m- - - - - - - Floor {diff} - - - - - - -")
                for i in enemies:
                    print(f"{enemies.index(i)+1}. {i.name if i !='Flee' else i}")
                print("\033[37m",end="")
                
                targeted_enemy=enemies[mely()-1]
                
                if targeted_enemy=="Flee":
                    adventure=False
                    area="home"
                    choice=False
                    area, wpn_to_be_sold=info(area, choice, wpn_to_be_sold)
                    break

                else:
                    targeted_enemy.fullHeal()
                    targeted_enemy.applyGameDiff(State.game_diff)
                    targeted_enemy.applyPlayerWeapon(State.player.getEquippedWeapon())

                    while targeted_enemy.current_hp>0: #fight
                        targeted_enemy.clampActuals()
                        print()
                        print(f"\033[37;41mHealth: {State.player.current_hp:.2f}\033[37;40m")
                        print(f"\033[37;45mfocus (accuracy): {State.player.actuals['acc']:.2f}\033[37;40m")
                        print(f"\033[31m- - - - - - - {targeted_enemy.name} (health: {targeted_enemy.current_hp}) - - - - - - -")
                        print("1. Attack")
                        print("2. Defend")
                        print(f"3. drink potion ({State.player.actuals['pot']} remaining)\033[37m")

                        atk_choice=mely(3)
                        
                        out_of_potions=State.player.actuals["pot"]==0
                        if out_of_potions and atk_choice==3:
                            print("You are out of potions.")
                            atk_choice=mely(2,"You are out of potions.")

                        State.player.is_guarding=False
                        print("\033[33m",end="")
                        match atk_choice:
                            case 1:
                                print(f"You whack the {targeted_enemy.name}, dealing {targeted_enemy.takeDamage(State.player.calcDamageOut())} damage!")

                            case 2:
                                print(f"You brace yourself for impact, negating some damage, and letting you focus!")
                                State.player.is_guarding=True
                                if State.player.actuals["acc"]+0.03 <= State.player.bases["acc"]*2:

                                    focus_gained=0.03
                                    match place_index:
                                        case 0:
                                            focus_gained*=1.25

                                    State.player.actuals["acc"]+=focus_gained
                                else:
                                    print("Max focus reached!")
                                    State.player.actuals["acc"] = State.player.bases["acc"]*2
                                State.player.actuals["acc"]+=0.02

                            case 3:
                                restored_hp=15 + (place_index==3) * 10 #if in river, +10 healing
                                print(f"You drink a potion, restoring {restored_hp} health!")
                                State.player.current_hp+=restored_hp
                                State.player.actuals["pot"]-=1
                        
                        if targeted_enemy.current_hp>0:
                            print(f"The {targeted_enemy.name} swings at you, dealing {State.player.takeDamage(targeted_enemy.calcDamageOut())}!")
                            if State.player.current_hp<=0:
                                input("\033[37mYou \033[37;41mdied...\033[37;40m")
                                adventure=False
                                run=False
                                break

                            print("you lose some focus.")
                            loss = 0.02
                            match State.player.equipped_wpn:
                                case "bow":
                                    loss *= 0.5
                                case "dagger":
                                    loss *= 1.5
                            
                            match place_index:
                                case 2:
                                    loss *= 0.75

                            State.player.actuals["acc"] -= loss

                            if State.player.actuals["acc"] <= 0:
                                State.player.actuals["acc"] = 0

                        print("\033[37m",end="")

                    if run: #checking if the player died
                        input("\033[36mEnemy defeated!")
                        weapons=makeWeapons(diff + (place_index==1)*5, targeted_enemy)
                        enemies.pop(enemies.index(targeted_enemy))

                        if len(weapons)==1:
                            print("You notice a weapon on the ground:")
                        if len(weapons)>1:
                            print("You notice some weapons on the ground:")

                        for i in weapons:
                            print(i.getWeaponString())
                            State.player.weapons.append(i)
                        print("\033[37m",end="")
                        
                        if weapons:
                            input()
                    else:
                        break

        if diff>50:
            print()
            input("Damn, you reached the last floor!\nHere, have a reward:")

            reward_enemy=Enemy(100, 15, 10, name="reward chest", loot=["sword","shield","dagger","bow","potion"], weapon_amount_max=1, diff=1)
            weapons=makeWeapons(200,reward_enemy,True)

            for i in weapons:
                print(i.getWeaponString())
                State.player.weapons.append(i)
