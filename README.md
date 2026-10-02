# Town n shit 2 electric boogaloo

A CLI roguelite dungeon crawler made in Python.

## How to play

Download `Town.exe` and run it. I recommend putting it in its own folder, since it creates save files in its directory.

## The game

This section is a guide to the interface and mechanics. If you're not sure what's happening, start here.

When asked to make a choice, pressing Enter without typing a number counts as choosing 1.

### Objective

The main objective of the game is to advance. There are 50 floors and 5 enemy types, with a boss of the matching type every 10 floors.

## Areas

### Town

The main menu of the game. Entering the Town saves your progress and restores your health. From here you have 6 options:

- **Shop**: spend money on upgrades, or sell weapons you no longer use
- **Weapons**: view and equip the weapons you own
- **Stats**: view your character's stats
- **Adventure**: go on an adventure
- **Settings**: change game settings
- **Quit**: close the game

### Shop

The place you can spend your money. Also, the place where you can get money by selling the weapons you aren't using anymore.

Money buys permanent upgrades that boost your base stats: damage, defense, accuracy and potions.

You start with 10 money, which (on default difficulty) is enough for exactly one potion upgrade, so visit the shop before your first adventure.

### Settings

Currently there is only one setting:

- **Combat QoL** (off by default): skips the "press Enter" pauses in combat, namely after enemy attacks, after defeating an enemy, and after weapons drop.

## Combat

Before entering the first floor, you are taken to a random location, each with its own bonuses:

- **Plains**: 1.5x damage, and you gain more focus when defending
- **Forest**: 1.5x defense, and enemies drop better weapons
- **Cave**: 1.5x accuracy, and you lose focus more slowly
- **Riverside**: 1.3x max health, and potions heal more

### Floors

Each floor has one or more enemies, and you pick which one to fight. You can choose **Flee** at any time to return to town, but every 10th floor is a boss fight with no escape. If you clear floor 50, you get a special reward.

If you die, the run ends and the game closes. Keep in mind that progress is only saved when entering the Town, so if you die, you also lose all weapons you got during that run.

### Fighting

Each turn you can:

1. **Attack**: deal damage to the enemy
2. **Defend**: take less damage and build up focus
3. **Drink potion**: restore health (uses one potion)
4. **Auto focus**: picks Defend every turn until your focus reaches its maximum, then returns control to you

Focus is the same as your accuracy, and it multiplies the damage you deal. It drops a little every time an enemy hits you, and defending brings it back up, so it's worth stopping to build focus before a big fight. Your maximum focus is twice your base accuracy, or higher if you have a bow equipped. The amount it drops by when hit is less with a bow equipped, and more with a dagger.

### Weapons and loot

Defeated enemies may drop weapons, and bosses always drop some. Every weapon has a **value** (shown in its name, like "good sword, 1.65x") and a quality prefix based on it: dogshit, decent, good, great, or legendary. Higher floors drop higher-value weapons.

Only one weapon can be equipped at a time. Its value is multiplied with your base stat, and each type has its own extra modifier on top:

| Type | Effect |
| --- | --- |
| Sword | Damage = base damage × value |
| Shield | Defense = base defense × value |
| Dagger | Damage = base damage × value × 1.2, but defense = base defense × 0.8 (the penalty doesn't depend on value). You also lose focus faster |
| Bow | Accuracy = base accuracy × value × 0.9. Your max focus becomes base accuracy × value × 2, and you lose focus slower |
| Potion | Extra potions = (value − 1) × 5, rounded |
| Club | Damage = base damage × value × 0.7, and the enemy's defense is ignored |

For example, with 10 base damage, a 1.8x sword gives 18 damage, while a 1.8x dagger gives 10 × 1.8 × 1.2 = 21.6 damage but cuts your defense to 80%.