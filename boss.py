"""
Boss class for the RPG game.

This module defines the Boss class which is a special type of Character
with additional abilities and mechanics.
"""
import random
from typing import Optional
from character import Character
from weapon import Weapon

class Boss(Character):
    """
    Special type of character that inherits from Character.
    
    This class demonstrates inheritance and method overriding.
    Bosses have special attacks and unique mechanics.
    """
    
    def __init__(self, name: str, max_health: int, weapon: Weapon, special_attack: str):
        """
        Initialize a new boss character.
        
        Args:
            name (str): Boss's name
            max_health (int): Maximum health points
            weapon (Weapon): The boss's weapon
            special_attack (str): Name of the boss's special attack
        """
        super().__init__(name, max_health, weapon)
        self.special_attack_name = special_attack
        self.special_attack_cooldown = 0
        self.turn_count = 0
        self.enraged = False
        
        # Boss stats are generally better than regular characters
        self.defense += 3
        self.weapon.base_damage = int(self.weapon.base_damage * 1.5)
    
    def __str__(self) -> str:
        """Return a string representation of the boss."""
        status = "ENRAGED" if self.enraged else ""
        return f"{super().__str__()} {status}"
    
    def start_turn(self):
        """Called at the start of the boss's turn."""
        self.turn_count += 1
        
        # Reduce cooldown on special attack
        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1
        
        # Check for enrage at 50% health
        if not self.enraged and self.health <= self.max_health // 2:
            self.enrage()
    
    def enrage(self):
        """Enhance the boss's abilities when enraged."""
        if self.enraged:
            return
            
        self.enraged = True
        self.weapon.base_damage = int(self.weapon.base_damage * 1.5)
        self.defense += 2
        
        # Heal slightly when enraging
        self.heal(self.max_health // 4)
    
    def attack(self, target) -> int:
        """
        Attack a target character with a chance to use special attack.
        
        Args:
            target (Character): The character to attack
            
        Returns:
            int: Damage dealt to the target
        """
        if not self.is_alive():
            return 0
        
        # Use special attack if available
        if (self.special_attack_cooldown == 0 and 
            (self.enraged or random.random() < 0.3)):  # 30% chance to use special when not enraged
            return self.special_attack(target)
            
        # Normal attack
        damage = super().attack(target)
        
        # Enraged bosses attack twice
        if self.enraged and random.random() < 0.5:  # 50% chance for double attack
            damage += super().attack(target)
            
        return damage
    
    def special_attack(self, target) -> int:
        """
        Perform a special boss attack.
        
        Args:
            target (Character): The target of the special attack
            
        Returns:
            int: Damage dealt by the special attack
        """
        if not self.is_alive():
            return 0
            
        # Set cooldown for special attack (2-4 turns)
        self.special_attack_cooldown = random.randint(2, 4)
        
        # Special attack deals 1.5x to 2.5x normal damage
        base_damage = self.weapon.base_damage
        special_multiplier = 1.5 + random.random()  # 1.5 to 2.5x
        damage = int(base_damage * special_multiplier)
        
        # Critical hit chance is doubled for special attacks
        if random.random() < self.weapon.critical_chance * 2:
            damage = int(damage * self.weapon.critical_multiplier)
            self.weapon.critical_hit = True
        else:
            self.weapon.critical_hit = False
        
        # Apply damage to target
        actual_damage = target.take_damage(damage, self)
        
        # Additional effects based on special attack type
        if "fire" in self.special_attack_name.lower() and hasattr(target, 'apply_burn'):
            target.apply_burn(damage // 4, 3)  # Burn for 25% of damage over 3 turns
        elif "freeze" in self.special_attack_name.lower() and hasattr(target, 'apply_stun'):
            target.apply_stun(1)  # Stun for 1 turn
            
        return actual_damage
    
    def take_damage(self, damage: int, attacker = None) -> int:
        """
        Take damage from an attack with boss-specific mechanics.
        
        Args:
            damage (int): Amount of damage to take
            attacker: The character dealing the damage
            
        Returns:
            int: Actual damage taken after defenses and boss mechanics
        """
        # Bosses take reduced damage when not enraged
        if not self.enraged:
            damage = max(1, damage // 2)  # Take at least 1 damage
            
        return super().take_damage(damage, attacker)
