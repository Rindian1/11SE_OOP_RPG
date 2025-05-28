"""
Weapon class for the RPG game.

This module defines the Weapon class which represents weapons that can be equipped by characters.
"""
from typing import Optional

class Weapon:
    """
    Represents a weapon that can be equipped by characters.
    
    Attributes:
        name (str): The name of the weapon
        base_damage (int): The base damage the weapon deals
        critical_chance (float): Chance to land a critical hit (0.0 to 1.0)
        critical_multiplier (float): Damage multiplier for critical hits
    """
    
    def __init__(self, name: str, base_damage: int, critical_chance: float = 0.1, critical_multiplier: float = 2.0):
        """
        Initialize a new weapon.
        
        Args:
            name (str): The name of the weapon
            base_damage (int): The base damage the weapon deals
            critical_chance (float, optional): Chance to land a critical hit (0.0 to 1.0)
            critical_multiplier (float, optional): Damage multiplier for critical hits
        """
        self.name = name
        self.base_damage = base_damage
        self.critical_chance = max(0.0, min(1.0, critical_chance))  # Clamp between 0 and 1
        self.critical_multiplier = max(1.0, critical_multiplier)  # Ensure at least 1.0x
        self.critical_hit = False
    
    def calculate_damage(self) -> int:
        """
        Calculate the damage dealt by this weapon.
        
        Returns:
            int: The calculated damage, including critical hits
        """
        import random
        
        # Reset critical hit flag
        self.critical_hit = False
        
        # Calculate base damage
        damage = self.base_damage
        
        # Check for critical hit
        if random.random() < self.critical_chance:
            damage = int(damage * self.critical_multiplier)
            self.critical_hit = True
        
        return damage
    
    def __str__(self) -> str:
        """
        Return a string representation of the weapon.
        
        Returns:
            str: A formatted string with weapon details
        """
        crit_info = f" (Crit: {self.critical_chance*100:.0f}% x{self.critical_multiplier})" if self.critical_chance > 0 else ""
        return f"{self.name} ({self.base_damage} damage{crit_info})"
    
    def upgrade(self, damage_increase: int = 1):
        """
        Upgrade the weapon's base damage.
        
        Args:
            damage_increase (int, optional): Amount to increase base damage by
        """
        self.base_damage += damage_increase
    
    def set_critical_chance(self, chance: float):
        """
        Set the weapon's critical hit chance.
        
        Args:
            chance (float): New critical hit chance (0.0 to 1.0)
        """
        self.critical_chance = max(0.0, min(1.0, chance))  # Clamp between 0 and 1
    
    def set_critical_multiplier(self, multiplier: float):
        """
        Set the weapon's critical hit multiplier.
        
        Args:
            multiplier (float): New critical hit multiplier (must be ≥ 1.0)
        """
        self.critical_multiplier = max(1.0, multiplier)  # Ensure at least 1.0x
