
def choiceToArea(State, area, choice, wpn_to_be_sold):
    match area:
        case "home":
            match choice:
                case 1:
                    return "shop"
                case 2:
                    return "char_weapons"
                case 3:
                    return "char_stats"
                case 4:
                    return "adventure_start"
                case 5:
                    return "quit"
        
        case "shop":
            match choice:
                case 1:
                    return "upgrade_dmg"
                case 2:
                    return "upgrade_def"
                case 3:
                    return "upgrade_acc"
                case 4:
                    return "upgrade_pot"
                case 5:
                    return "sell_wpn"
                case 6:
                    return "home"
        
        case "upgrade_dmg" | "upgrade_def" | "upgrade_acc" | "upgrade_pot":
            match area:
                case "upgrade_dmg":
                    upgrade_index=0
                case "upgrade_def":
                    upgrade_index=1
                case "upgrade_acc":
                    upgrade_index=2
                case "upgrade_pot":
                    upgrade_index=3
                    
            if choice==1:
                if State.upgrade_prices[upgrade_index]<=State.money:
                    State.money-=State.upgrade_prices[upgrade_index]

                    State.player.bases[list(State.player.bases.keys())[upgrade_index+1]] += State.player.upgrade_amounts[list(State.player.upgrade_amounts.keys())[upgrade_index]] #az első choice-1 lenne, de hp az első így hozzá kell adni egyet, így csak simán choice
                    State.upgrade_prices[upgrade_index] *= State.player.upgrade_price_scaling[list(State.player.upgrade_price_scaling.keys())[upgrade_index]]
                    State.clampUpgradePrices()
                else:
                    input("Not enough money.")
            return "shop"
        
        case "sell_wpn":
            if choice<=len(State.player.weapons):
                return "q_sell_wpn"
            return "shop"
        
        case "q_sell_wpn":
            if choice==2:
                return "sell_wpn"
            State.money+=wpn_to_be_sold.sell_value
            State.player.weapons.pop(State.player.weapons.index(wpn_to_be_sold))
            return "sell_wpn"

        case "char_weapons":
            if choice<=len(State.player.weapons) and choice>=0:
                for i in State.player.weapons:
                    i.equipped=False
                State.player.weapons[choice-1].equipped=True
                print(State.player.getEquippedWeapon().getWeaponString()+" equipped!")
                State.player.calcDamageOut()
            return "home"
        
        case "char_stats":
            return "home"

    return area