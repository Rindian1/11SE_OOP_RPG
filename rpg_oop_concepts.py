

"""
RPG OOP Concepts Demonstration
=============================

This file demonstrates core Object-Oriented Programming (OOP) concepts through a simple RPG game implementation.
Key OOP concepts demonstrated:
- Classes and Objects
- Inheritance (Character -> Boss)
- Composition (Character uses Weapon)
- Association (Game uses GameLogger)
- Encapsulation
- Polymorphism

File Structure:
--------------
1. Utility Functions (clear_screen, press_enter, print_border)
2. Core Classes (GameLogger, Weapon, Character, Boss)
3. Game Logic (main game loop)
4. Main Execution (entry point)

Each class and function includes detailed docstrings explaining their purpose and usage.
"""

import os
import datetime

# Clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Prompt the user to press Enter to continue
def press_enter():
    input("\nPress Enter to continue...\n")

# Print a border for visual separation
def print_border():
    print("-" * 80)

# GameLogger class to demonstrate association relationship with Game (solid line in UML)
class GameLogger:
    def __init__(self, log_to_console=True):
        self.log_to_console = log_to_console
        
    def log_combat(self, attacker, defender, damage):
        # Get current time for the log
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] COMBAT LOG: {attacker.name} attacked {defender.name} for {damage} damage"
        if self.log_to_console:
            print(log_message)
        # Future enhancement: could log to file, database, etc.

# Define a Weapon class to represent different weapons in the game
class Weapon:
    def __init__(self, name, damage_bonus):
        self.name = name
        self.damage_bonus = damage_bonus

# Define a Character class to represent a game character
class Character:
    def __init__(self, name, health, damage, weapon_name=None, weapon_damage=0):
        self.name = name
        # The underscore prefix (_) indicates that this attribute is intended to be "private" 
        # - meaning it should only be accessed through the getter and setter methods.
        # This is a convention in Python, not a strict rule enforced by the language.
        self._health = health  # Private attribute (by convention)
        self.damage = damage
        # Create the weapon inside the Character constructor (strong composition)
        self.weapon = Weapon(weapon_name, weapon_damage) if weapon_name else None

    # Getter for health - provides controlled access to the private attribute
    def get_health(self):
        return self._health
    
    # Setter for health with validation - ensures health is never negative
    def set_health(self, new_health):
        if new_health < 0:
            self._health = 0
        else:
            self._health = new_health

    # Method for the character to attack an enemy
    def attack(self, enemy, logger=None):
        total_damage = self.damage + (self.weapon.damage_bonus if self.weapon else 0) #if there is a weapon, add the dammage bonus
        # Use getter and setter instead of direct attribute access
        current_health = enemy.get_health()
        enemy.set_health(current_health - total_damage)
        # Use the logger if provided (dependency), otherwise fall back to static method
        if logger:
            logger.log_combat(self, enemy, total_damage)
        return total_damage

    # Method to display character information
    def display(self):
        weapon_name = self.weapon.name if self.weapon else 'No Weapon'
        weapon_damage = self.weapon.damage_bonus if self.weapon else 0
        # Use getter instead of direct attribute access
        print(f"Name: {self.name}\nHealth: {self.get_health()}\nDamage: {self.damage}\nWeapon: {weapon_name} (+{weapon_damage} Damage)")

# Define a Boss class that inherits from Character, representing a boss enemy
class Boss(Character):
    def __init__(self, name, health, damage):
        # Pass weapon details to parent constructor instead of creating a Weapon object here
        super().__init__(name, health, damage, "Boss Weapon", 5)

    # Boss's special attack with additional damage
    def attack(self, enemy, logger=None):
        additional_damage = 1 # Example of special attack causing additional damage
        total_damage = super().attack(enemy, logger) # Call Character's attack, then add bonus
        # Use getter and setter instead of direct attribute access
        current_health = enemy.get_health()
        enemy.set_health(current_health - additional_damage) # Apply additional damage
        print(f"{self.name} uses a special attack! (+{additional_damage} Damage)")
        # Use the logger if provided for the special attack
        if logger:
            logger.log_combat(self, enemy, additional_damage)
        return total_damage + additional_damage


# Define a Game class to manage the game flow
class Game:
    def __init__(self):
        self.player = None
        self.bosses = []
        # Create and manage a GameLogger instance (association)
        self.logger = GameLogger()

    # Show the introductory message and set up the game
    def show_intro(self):
        clear_screen()
        print("Welcome to the RPG Adventure!")
        print("In a world where darkness looms, you are the chosen hero destined to defeat the evil bosses and restore peace.")
        self.setup_game(input("Enter your character's name: ").capitalize())

    # Set up the game by creating the player character and bosses
    def setup_game(self, name):
        # Get weapon details instead of a Weapon object
        weapon_name, weapon_damage = self.choose_weapon()
        self.player = Character(name, 110, 10, weapon_name, weapon_damage)
        self.player.display()
        press_enter()
        self.bosses = [Boss("Goblin King", 50, 8), Boss("Dark Sorcerer", 60, 9)]

    # Allow the player to choose a weapon
    def choose_weapon(self):
        weapons = [
            {"name": "Rock", "damage_bonus": 2},
            {"name": "Paper", "damage_bonus": 3},
            {"name": "Scissors", "damage_bonus": 4}
        ]
        options = [weapon["name"] for weapon in weapons]
        choice_index = self.get_valid_input("\nChoose your weapon (Rock, Paper, Scissors): ", options)
        weapon_data = weapons[choice_index]
        # Return weapon name and damage instead of creating a Weapon object
        return weapon_data["name"], weapon_data["damage_bonus"]

    # Get valid user input for weapon choice
    def get_valid_input(self, prompt, options):
        while True:
            user_input = input(prompt).capitalize()
            if user_input in options:
                return options.index(user_input)
            print("Invalid input, please try again.")

    # Handle the combat between player and enemy
    def combat(self, player, enemy):
        while player.get_health() > 0 and enemy.get_health() > 0:
            self.display_combat_status(player, enemy)
            # Pass the logger to the attack methods
            damage_dealt = player.attack(enemy, self.logger)
            print(f"You dealt {damage_dealt} damage to {enemy.name}.")
            if enemy.get_health() <= 0:
                self.print_victory_message(enemy)
                return True

            # Pass the logger to the attack methods
            damage_received = enemy.attack(player, self.logger)
            print(f"{enemy.name} dealt {damage_received} damage to you.")
            if player.get_health() <= 0:
                self.print_defeat_message(enemy)
                return False
            press_enter()

    # Display the current status of the combat
    def display_combat_status(self, player, enemy):
        clear_screen()
        level = "LEVEL 1" if enemy.name == "Goblin King" else "LEVEL 2"
        print(f"\n=============> {level}: {enemy.name} <=============")
        player.display()
        print("-" * 30)
        enemy.display()
        print("-" * 30)
        # press_enter() # Removed from here to avoid double enter after enemy attack

    # Handle battles with bosses
    def handle_boss_battles(self):
        for boss in self.bosses:
            self.introduce_boss(boss)
            if not self.combat(self.player, boss):
                self.end_game(False)
                return
        self.end_game(True)

    # Introduce each boss before the battle
    def introduce_boss(self, boss):
        clear_screen()
        intro_messages = {
            "Goblin King": f"Level 1 - You have entered the lair of the Goblin King. He is known for his strength and brutality. Prepare for battle, {self.player.name}!",
            "Dark Sorcerer": f"Level 2 - You have defeated the Goblin King! Now, you face the Dark Sorcerer, a master of dark magic. Good luck, {self.player.name}!"
        }
        print(intro_messages.get(boss.name, "A new boss appears!"))
        press_enter()

    # Print victory message after defeating an enemy
    def print_victory_message(self, enemy):
        print_border()
        print(f"Victory! You defeated {enemy.name}.")
        press_enter()

    # Print defeat message after being defeated by an enemy
    def print_defeat_message(self, enemy):
        print_border()
        print(f"Defeat! You were defeated by {enemy.name}.")
        press_enter()

    # End the game and show final message
    def end_game(self, player_won):
        print_border()
        if player_won:
            print(f"Congratulations, {self.player.name}! You defeated all the bosses and restored peace to the land!")
        else:
            print(f"Game Over. The darkness prevails, but heroes never give up. Try again, {self.player.name}!")
        print_border()

    # Run the game
    def run(self):
        self.show_intro()
        self.handle_boss_battles()

# Start the game if this file is executed
if __name__ == "__main__":
    game = Game()
    game.run()
