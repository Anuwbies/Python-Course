# Capstone Project 1.2: Text-Based Dungeon RPG

## 📌 Project Overview
Create an immersive, turn-based **Text Adventure Dungeon Crawler RPG**. The player navigates through interconnected rooms, discovers loot, equips weapons and armor, battles randomized monsters using dynamic combat mechanics, and manages health and inventory to defeat the Dungeon Boss.

---

## 🎯 Learning Objectives
- **State Management**: Managing active game state, character stats, and dynamic room graphs.
- **Randomization (`random` module)**: Generating randomized combat rolls, loot drops, and enemy encounters.
- **Object-Oriented Programming**: Building `Character`, `Player`, `Monster`, `Item`, and `Room` classes.
- **Game Loops**: Structuring non-crashing main game loops with command parsers (`go north`, `attack`, `use potion`, `inventory`, `stats`).
- **Persistence**: Saving and restoring saved game states to `savegame.json`.

---

## 🏗️ System Architecture

```text
               +-------------------+
               |     Game Engine   |
               +-------------------+
                         |
      +------------------+------------------+
      |                  |                  |
+------------+    +------------+    +---------------+
|   Player   |    |  Monster   |    |     Room      |
+------------+    +------------+    +---------------+
| - hp: int  |    | - hp: int  |    | - name: str   |
| - atk: int |    | - atk: int |    | - desc: str   |
| - inventory|    | - xp_val   |    | - items: list |
| + attack() |    +------------+    | - exits: dict |
| + heal()   |                      +---------------+
+------------+
```

---

## 📋 Functional Requirements

### 1. Room Navigation Map
Represent the dungeon using a dictionary of interconnected `Room` instances:
- Rooms have exits pointing to directions: `"north"`, `"south"`, `"east"`, `"west"`.
- Rooms may contain items (e.g. `Health Potion`, `Iron Sword`, `Boss Key`) or monsters.

### 2. Player and Monster Combat
- **Player Stats**: Health (HP), Attack Power, Defense, Inventory (max capacity 5 items).
- **Combat Mechanics**: Turn-based fight where damage dealt is calculated with random variance:
  $$\text{Damage} = \max(1, (\text{Attacker ATK} + \text{Random}(-2, 2)) - \text{Defender DEF})$$
- Critical hit chance (15% chance to deal $1.5\times$ damage).
- Defeating enemies grants Experience Points (XP) and gold loot.

### 3. Inventory & Items
- Consumables (`Health Potion`: restores +30 HP).
- Equipment (`Sword`: +5 ATK, `Shield`: +4 DEF).
- Players can type `inventory`, `use <item>`, or `drop <item>`.

### 4. Game Loop & Command Parser
Accept user commands:
- `look`: Re-examine the current room description, items, and visible exits.
- `go [direction]`: Move to an adjacent room.
- `take [item]`: Pick up an item.
- `attack`: Engage in combat if an enemy is in the room.
- `save`: Save current player stats, position, and dungeon state to JSON.
- `quit`: Exit game.

---

## 📐 Phased Implementation Guide

### Phase 1: Core Entity Models
```python
class Character:
    def __init__(self, name: str, hp: int, max_hp: int, attack_power: int, defense: int):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack_power = attack_power
        self.defense = defense

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        actual_damage = max(1, amount - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
```

### Phase 2: Room & World Graph
```python
class Room:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.exits = {}      # dict: {"north": room_obj, "east": room_obj}
        self.items = []      # list of items
        self.enemy = None    # optional Monster instance
```

### Phase 3: Turn-Based Combat Loop
Build the combat loop that alternates turns between player and enemy until one falls to 0 HP.

### Phase 4: Save & Load State
Serialize the dungeon graph and player state into a structured JSON file.

---

## 🧪 Verification Matrix & Edge Cases

| Scenario | Input / Action | Expected Behavior |
| :--- | :--- | :--- |
| **Invalid Direction** | Type `go up` or `go south` when no exit exists | Displays `"You cannot go that way!"` without crashing |
| **Inventory Overflow**| Pick up a 6th item when limit is 5 | Displays `"Inventory full! Drop an item first."` |
| **Zero HP** | Player health drops to 0 during combat | Displays Game Over message and prompts to restart or quit |
| **Save / Load** | Save game in Room 3 with 45 HP, restart and load | Accurately restores Room 3 position, items, and 45 HP |

---

## 🚀 Bonus Challenges
- **Multiple Classes**: Allow player selection at start: `Warrior` (high HP/DEF), `Mage` (mana spells), `Rogue` (high crit chance).
- **Procedural Dungeon Generation**: Dynamically generate random room layouts with random monsters.
