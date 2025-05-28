"""
Game logging functionality for the RPG game.

This module handles all game logging functionality including combat events,
character actions, and game state changes.
"""
import time
from typing import Optional

class GameLogger:
    """
    Handles all game logging functionality.
    
    This class demonstrates dependency relationship with the Game class.
    """
    def __init__(self, log_to_console: bool = True):
        """
        Initialize the game logger.
        
        Args:
            log_to_console (bool): Whether to print logs to console
        """
        self.logs = []
        self.log_to_console = log_to_console
    
    def log_event(self, message: str):
        """
        Log game events with timestamp.
        
        Args:
            message (str): The message to be logged
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        if self.log_to_console:
            print(log_entry)
    
    def log_combat(self, attacker, defender, damage: int):
        """
        Log combat actions between characters.
        
        Args:
            attacker: The attacking character
            defender: The defending character
            damage (int): Amount of damage dealt
        """
        message = f"{attacker.name} attacks {defender.name} for {damage} damage"
        self.log_event(message)
        
        # Log critical hits or special events
        if hasattr(attacker, 'critical_hit') and attacker.critical_hit:
            self.log_event(f"CRITICAL HIT! {attacker.name}'s attack was devastating!")
            
        if damage == 0:
            self.log_event(f"{defender.name} blocked the attack!")
            
        if not defender.is_alive():
            self.log_event(f"{defender.name} has been defeated!")
    
    def log_heal(self, healer, amount: int, target=None):
        """
        Log healing actions.
        
        Args:
            healer: The character performing the heal
            amount (int): Amount of health restored
            target: The target being healed (defaults to healer)
        """
        target_name = target.name if target else "themselves"
        self.log_event(f"{healer.name} heals {target_name} for {amount} health")
    
    def log_status_effect(self, character, effect: str, applied: bool = True):
        """
        Log status effect changes.
        
        Args:
            character: The affected character
            effect (str): Name of the status effect
            applied (bool): Whether the effect was applied or removed
        """
        action = "gains" if applied else "loses"
        self.log_event(f"{character.name} {action} {effect}!")
