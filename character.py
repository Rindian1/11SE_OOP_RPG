"""
Character class for the RPG game.

This module defines the base Character class that represents game characters.
It demonstrates core OOP concepts like encapsulation, composition, and polymorphism.
"""
from typing import Optional
from weapon import Weapon

class Character:
    """
    Base class for all game characters.
    
    This class demonstrates:
    - Encapsulation (with private health attribute)
    - Composition (with Weapon)
    - Polymorphism (through overridden methods)
    """
    
    def __init__(self, name: str, max_health: int, weapon: Weapon):
        """
        Initialize a new character.
        
        Args:
            name (str): Character's name
            max_health (int): Maximum health points
            weapon (Weapon): The weapon equipped by this character
        """
        self.name = name
        self._max_health = max_health
        self._health = max_health
        self.weapon = weapon
        self.defense = 5  # Base defense value
        self.base_defense = 5  # Store base defense separately
        self.level = 1
        self.experience = 0
        self.is_defending = False
        self.defense_bonus = 0
        self.attack_bonus = 0
        self.health_bonus_used = False
        self.attack_bonus_used = False
    
    def __str__(self) -> str:
        """Return a string representation of the character."""
        return (f"{self.name} (Lvl {self.level}) - "
                f"HP: {self._health}/{self._max_health} | "
                f"Weapon: {self.weapon}")
    
    @property
    def health(self) -> int:
        """
        Get the current health of the character.
        
        Returns:
            int: Current health points
        """
        return self._health
    
    @health.setter
    def health(self, value: int):
        """
        Set the character's health with validation.
        
        Args:
            value (int): New health value
        """
        self._health = max(0, min(value, self._max_health))
    
    @property
    def max_health(self) -> int:
        """
        Get the maximum health of the character.
        
        Returns:
            int: Maximum health points
        """
        return self._max_health
    
    def is_alive(self) -> bool:
        """
        Check if the character is still alive.
        
        Returns:
            bool: True if alive, False otherwise
        """
        return self._health > 0
    
    def attack(self, target) -> int:
        """
        Attack a target character.
        
        Args:
            target (Character): The character to attack
            
        Returns:
            int: Damage dealt to the target
        """
        if not self.is_alive():
            return 0
            
        # Calculate base damage from weapon + attack bonus
        damage = self.weapon.calculate_damage() + self.attack_bonus
        
        # Reset attack bonus after use
        if self.attack_bonus > 0:
            self.attack_bonus = 0
            self.attack_bonus_used = True
        
        # Apply damage to target
        return target.take_damage(damage, self)
    
    def take_damage(self, damage: int, attacker = None) -> int:
        """
        Take damage from an attack.
        
        Args:
            damage (int): Amount of damage to take
            attacker (Character, optional): The character dealing the damage
            
        Returns:
            int: Actual damage taken after defenses
        """
        if not self.is_alive():
            return 0
            
        # Calculate total defense (base + bonus)
        total_defense = self.defense + self.defense_bonus
        
        # Apply defense if defending (double the defense value when defending)
        defense_value = total_defense * 2 if self.is_defending else total_defense
        
        # Ensure at least 1 damage is taken
        damage_taken = max(1, damage - defense_value)
        
        # Reduce health
        self.health -= damage_taken
        
        # Reset defense after taking damage
        if self.is_defending:
            self.is_defending = False
            self.defense_bonus = 0  # Reset defense bonus after being hit
            
        return damage_taken
    
    def defend(self):
        """
        Prepare to defend against the next attack.
        Reduces damage taken from the next attack.
        """
        self.is_defending = True
        self.defense_bonus = 2  # Small defense bonus for defending
        
    def use_health_item(self) -> int:
        """
        Use a health bonus item.
        
        Returns:
            int: Amount of health restored, or 0 if already used
        """
        if self.health_bonus_used:
            return 0
            
        heal_amount = 20  # Fixed amount or could be based on level
        old_health = self.health
        self.health += heal_amount
        self.health_bonus_used = True
        return self.health - old_health
        
    def use_attack_item(self) -> int:
        """
        Use an attack bonus item.
        
        Returns:
            int: Attack bonus amount, or 0 if already used
        """
        if self.attack_bonus_used:
            return 0
            
        self.attack_bonus = 5  # Fixed bonus or could be based on level
        self.attack_bonus_used = True
        return self.attack_bonus
        
    def reset_item_usage(self):
        """Reset item usage flags for a new enemy."""
        self.health_bonus_used = False
        self.attack_bonus_used = False
        self.defense_bonus = 0
    
    def heal(self, amount: int) -> int:
        """
        Heal the character.
        
        Args:
            amount (int): Amount to heal
            
        Returns:
            int: Actual amount healed
        """
        if not self.is_alive():
            return 0
            
        old_health = self.health
        self.health += amount
        return self.health - old_health
    
    def level_up(self):
        """Increase the character's level and improve stats."""
        self.level += 1
        self._max_health += 10
        self._health = self._max_health  # Fully heal on level up
        self.defense += 1
        
        # Improve weapon on level up
        if hasattr(self, 'weapon') and self.weapon:
            self.weapon.upgrade()
    
    def gain_experience(self, amount: int):
        """
        Gain experience points and level up if enough XP is accumulated.
        
        Args:
            amount (int): Amount of experience to gain
        """
        self.experience += amount
        xp_for_next_level = self.level * 100
        
        while self.experience >= xp_for_next_level:
            self.experience -= xp_for_next_level
            self.level_up()
            xp_for_next_level = self.level * 100
            print(f"{self.name} leveled up to level {self.level}!")
