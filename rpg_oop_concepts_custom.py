"""RPG_OOP_CONCEPTS CUSTOM"""
import random
import time
from typing import List, Optional

class GameLogger:
    def __init__(self, log_to_console=True):
        self.log_to_console = log_to_console
        
    def log_combat(self, attacker, defender, damage):
        if self.log_to_console:
            print(f"{attacker.name} attacked {defender.name} for {damage} damage!")
            print(f"{defender.name}'s health: {defender.health}")

class Weapon:
    def __init__(self, name: str, damage_bonus: int, description: str):
        self.name = name
        self.damage_bonus = damage_bonus
        self.description = description
        self.equipped = False

    def __str__(self):
        return f"{self.name} (+{self.damage_bonus} damage)\n{self.description}"

class Character:
    def __init__(self, name, health, damage, weapon=None):
        self.name = name
        self.health = health
        self.damage = damage
        self.weapon = weapon
        
    def is_alive(self):
        return self.health > 0
        
    def attack(self, target, logger=None):
        total_damage = self.damage + (self.weapon.damage_bonus if self.weapon else 0)
        target.health -= total_damage
        if logger:
            logger.log_combat(self, target, total_damage)

class Boss(Character):
    def __init__(self, name, health, damage, weapon=None, special_attack=10):
        super().__init__(name, health, damage, weapon)
        self.special_attack = special_attack
        
    def special_attack(self, target, logger=None):
        damage = self.damage * 1.5 + self.special_attack
        target.health -= damage
        if logger:
            logger.log_combat(self, target, damage)
            print(f"{self.name} used special attack!")

class Enemy(Character):
    def __init__(self, name, health, damage, weapon=None):
        super().__init__(name, health, damage, weapon)

class Person(Character):
    def __init__(self, name: str, health: int, damage: int, weapon: Optional[Weapon] = None):
        super().__init__(name, health, damage, weapon)
        self.level = 1
        self.xp = 0
        self.inventory: List[Weapon] = []
        self.gold = 0
        
    def add_weapon(self, weapon: Weapon):
        print(f"\nYou found a {weapon.name}!")
        print(f"{weapon.description}")
        self.inventory.append(weapon)
        
    def equip_weapon(self, weapon_index: int) -> bool:
        if 0 <= weapon_index < len(self.inventory):
            weapon = self.inventory[weapon_index]
            if self.weapon:
                self.weapon.equipped = False
            self.weapon = weapon
            weapon.equipped = True
            print(f"\nEquipped {weapon.name}!")
            print(f"New damage: {self.damage + weapon.damage_bonus}")
            return True
        return False
        
    def show_inventory(self):
        print("\nYour Inventory:")
        print("1. Weapons:")
        for i, weapon in enumerate(self.inventory):
            status = "(Equipped)" if weapon.equipped else ""
            print(f"{i + 1}. {weapon} {status}")
        print(f"\nGold: {self.gold}g")
        
    def level_up(self):
        self.level += 1
        self.health += 10
        self.damage += 5
        print(f"\nCongratulations! You leveled up to level {self.level}!")
        print(f"Health increased to {self.health}")
        print(f"Damage increased to {self.damage}")

class Game:
    def __init__(self):
        self.logger = GameLogger()
        self.player = Person("Hero", 100, 20)
        self.story = [
            "You are a brave adventurer in the land of Eldoria, where darkness threatens the realm.",
            "Your journey begins in the small village of Thundertop, where rumors of a growing evil have been spreading.",
            "The village elder has tasked you with investigating the nearby Goblin Caves.",
            "The goblins have been raiding the village and must be stopped."
        ]
        
        self.weapons = [
            Weapon("Iron Sword", 10, "A sturdy sword forged in the mountains of Eldoria."),
            Weapon("Dagger of Shadows", 8, "A quick and deadly weapon, perfect for surprise attacks."),
            Weapon("Mighty Axe", 15, "A heavy weapon that deals devastating damage."),
            Weapon("Flame Sword", 20, "A legendary weapon said to have been crafted by the fire elementals.")
        ]
        
        self.enemies = [
            Enemy("Goblin", 30, 10),
            Enemy("Orc", 50, 15),
            Boss("Dragon", 200, 30, special_attack=20)
        ]
        
    def start(self):
        print("Welcome to the RPG Adventure!")
        print("\nYou are a brave hero facing dangerous enemies. Good luck!")
        print("\nPress Enter to begin your journey...")
        input()
        
        while self.player.is_alive() and any(enemy.is_alive() for enemy in self.enemies):
            
            # Combat phase
            print("\nEnemies remaining:")
            for i, enemy in enumerate(self.enemies):
                if enemy.is_alive():
                    print(f"{i + 1}. {enemy.name} (Health: {enemy.health})")
            
            print("\nWhat would you like to do?")
            print("1. Attack an enemy")
            print("2. Check inventory")
            print("3. Rest and heal")
            
            choice = input("\nChoose an action (1-3): ")
            
            try:
                if choice == "1":
                    enemy_index = int(input("Choose an enemy to attack (1-3): ")) - 1
                    if 0 <= enemy_index < len(self.enemies):
                        enemy = self.enemies[enemy_index]
                        if enemy.is_alive():
                            self.player.attack(enemy, self.logger)
                            
                            if enemy.is_alive():
                                enemy.attack(self.player, self.logger)
                            
                            if not enemy.is_alive():
                                print(f"\nYou defeated {enemy.name}!")
                                xp_gain = random.randint(10, 20)
                                gold_gain = random.randint(5, 15)
                                self.player.xp += xp_gain
                enemy_index = int(choice) - 1
                
                if 0 <= enemy_index < len(self.enemies):
                    enemy = self.enemies[enemy_index]
                    if enemy.is_alive():
                        self.player.attack(enemy, self.logger)
                        
                        if enemy.is_alive():
                            enemy.attack(self.player, self.logger)
                        
                        if not enemy.is_alive():
                            print(f"\nYou defeated {enemy.name}!")
                            xp_gain = random.randint(10, 20)
                            self.player.xp += xp_gain
                            print(f"You gained {xp_gain} XP!")
                            
                            if self.player.xp >= 100 * self.player.level:
                                self.player.level_up()
                                self.player.xp = 0
                    else:
                        print("That enemy is already defeated!")
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a number!")
            except IndexError:
                print("Please enter a number between 1 and 3!")
            
            if not self.player.is_alive():
                print("\nGame Over! You have been defeated!")
                break
            
            if all(not enemy.is_alive() for enemy in self.enemies):
                print("\nCongratulations! You have defeated all enemies!")
                print(f"Final Level: {self.player.level}")
                print(f"Final Health: {self.player.health}")
                print(f"Final Damage: {self.player.damage}")
                break

if __name__ == "__main__":
    game = Game()
    game.start()
