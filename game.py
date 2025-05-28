"""
Game class for the RPG game.

This module contains the main Game class that manages the game state and flow.
It demonstrates the use of other classes and handles the game loop.
"""
import random
from typing import Dict, List, Optional, Any

# Import other game components
from character import Character
from boss import Boss
from weapon import Weapon
from game_logger import GameLogger
from console_utils import clear_screen, print_header, press_enter, print_border

class Game:
    """
    Manages the game state and controls the game flow.
    
    This class demonstrates:
    - Game loop pattern
    - Dependency on GameLogger
    - Composition of game elements
    - State management
    """
    
    def __init__(self):
        """Initialize the game with default settings."""
        self.logger = GameLogger()
        self.player: Optional[Character] = None
        self.current_enemy: Optional[Character] = None
        self.game_active: bool = False
        self.turn_count: int = 0
        self.defending: bool = False
        
        # Game balance settings
        self.encounters: List[Dict[str, Any]] = [
            {
                "name": "Goblin",
                "health": 30,
                "weapon": Weapon("Rusty Dagger", 5),
                "is_boss": False
            },
            {
                "name": "Orc",
                "health": 50,
                "weapon": Weapon("Battle Axe", 8),
                "is_boss": False
            },
            {
                "name": "Dragon",
                "health": 100,
                "weapon": Weapon("Fire Breath", 12, 0.2),
                "special_attack": "Inferno Breath",
                "is_boss": True
            },
        ]
    
    def clear_screen(self):
        """Clear the console screen."""
        clear_screen()
    
    def print_header(self, title: str):
        """
        Print a formatted header.
        
        Args:
            title (str): The title to display in the header
        """
        print_header(title)
    
    def setup_game(self):
        """Initialize the game state and create the player character."""
        self.clear_screen()
        self.print_header("RPG Game - Character Creation")
        
        # Get player name
        player_name = input("Enter your character's name: ").strip() or "Hero"
        
        # Create player with starting weapon
        starting_weapon = Weapon("Iron Sword", 6, 0.15, 2.0)
        self.player = Character(player_name, 50, starting_weapon)
        
        self.game_active = True
        self.turn_count = 0
        
        print(f"\nWelcome, {player_name}! Your adventure begins...")
        press_enter()
    
    def create_enemy(self, enemy_data: Dict[str, Any]) -> Character:
        """
        Create an enemy character based on the given data.
        
        Args:
            enemy_data (dict): Dictionary containing enemy properties
            
        Returns:
            Character: The created enemy character
        """
        if enemy_data.get("is_boss", False):
            return Boss(
                name=enemy_data["name"],
                max_health=enemy_data["health"],
                weapon=enemy_data["weapon"],
                special_attack=enemy_data.get("special_attack", "Special Attack")
            )
        else:
            return Character(
                name=enemy_data["name"],
                max_health=enemy_data["health"],
                weapon=enemy_data["weapon"]
            )
    
    def player_turn(self):
        """Handle the player's turn in combat."""
        if not self.player or not self.current_enemy:
            return
            
        self.clear_screen()
        self.print_header(f"Combat - Turn {self.turn_count}")
        
        # Show combat status
        print(f"\n{self.player}")
        print(f"{self.current_enemy}\n")
        
        # Show item usage status
        health_item_status = "(Used)" if self.player.health_bonus_used else "(Available)"
        attack_item_status = "(Used)" if self.player.attack_bonus_used else "(Available)"
        
        # Player actions
        print("1. Attack")
        print("2. Defend")
        print("3. Use Health Potion", health_item_status)
        print("4. Use Strength Potion", attack_item_status)
        print("5. Run Away")
        
        while True:
            try:
                choice = input("\nChoose an action (1-5): ")
                if choice == "1":
                    # Attack
                    damage = self.player.attack(self.current_enemy)
                    self.logger.log_combat(self.player, self.current_enemy, damage)
                    if self.player.attack_bonus > 0:
                        self.logger.log_event(f"{self.player.name}'s attack is empowered! (+{self.player.attack_bonus} damage)")
                    break
                elif choice == "2":
                    # Defend
                    self.player.defend()
                    self.logger.log_event(f"{self.player.name} prepares to defend! (+{self.player.defense_bonus} defense)")
                    break
                elif choice == "3":
                    # Use health potion
                    heal_amount = self.player.use_health_item()
                    if heal_amount > 0:
                        self.logger.log_heal(self.player, heal_amount)
                    else:
                        self.logger.log_event("You've already used your health potion for this battle!")
                    break
                elif choice == "4":
                    # Use strength potion
                    bonus = self.player.use_attack_item()
                    if bonus > 0:
                        self.logger.log_event(f"{self.player.name} drinks a strength potion! Next attack will deal +{bonus} damage!")
                    else:
                        self.logger.log_event("You've already used your strength potion for this battle!")
                    break
                elif choice == "5":
                    # Run away
                    if isinstance(self.current_enemy, Boss):
                        self.logger.log_event("You can't run from a boss battle!")
                        break
                        
                    if random.random() < 0.5:  # 50% chance to escape
                        self.logger.log_event("You successfully ran away!")
                        self.game_active = False
                        return
                    else:
                        self.logger.log_event("You failed to escape!")
                        break
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")
        
        press_enter()
    
    def enemy_turn(self):
        """Handle the enemy's turn in combat."""
        if not self.player or not self.current_enemy:
            return
            
        # Skip turn if enemy is dead
        if not self.current_enemy.is_alive():
            return
            
        # Special handling for bosses
        if isinstance(self.current_enemy, Boss):
            self.current_enemy.start_turn()
        
        # Simple AI: 70% chance to attack, 30% chance to defend
        action = random.choices(
            ["attack", "defend"],
            weights=[0.7, 0.3],
            k=1
        )[0]
        
        if action == "attack":
            damage = self.current_enemy.attack(self.player)
            self.logger.log_combat(self.current_enemy, self.player, damage)
        else:
            self.current_enemy.defend()
            self.logger.log_event(f"{self.current_enemy.name} prepares to defend!")
        
        press_enter()
    
    def check_victory(self):
        """Check if the player has defeated all enemies."""
        if not self.current_enemy or not self.current_enemy.is_alive():
            # Player defeated the current enemy
            self.logger.log_event(f"You defeated {self.current_enemy.name}!")
            
            # Grant experience
            xp_reward = 50 * self.turn_count  # More XP for longer fights
            self.player.gain_experience(xp_reward)
            
            # Reset item usage for the next enemy
            self.player.reset_item_usage()
            
            # Check if there are more enemies
            if self.encounters:
                # Get next enemy
                next_enemy_data = self.encounters.pop(0)
                self.current_enemy = self.create_enemy(next_enemy_data)
                self.logger.log_event(f"A wild {self.current_enemy.name} appears!")
                
                # Reset turn counter for the new enemy
                self.turn_count = 0
            else:
                # Player won the game
                self.logger.log_event("Congratulations! You've defeated all enemies!")
                self.game_active = False
    
    def game_over(self):
        """Handle game over scenario."""
        self.clear_screen()
        self.print_header("Game Over")
        
        if self.player and not self.player.is_alive():
            print("You were defeated in battle...")
        else:
            print("Thanks for playing!")
        
        print(f"\nYou reached level {self.player.level if self.player else 1}.")
        press_enter()
    
    def run(self):
        """Main game loop."""
        try:
            # Setup game
            self.setup_game()
            
            # Create first enemy
            if self.encounters:
                first_enemy_data = self.encounters.pop(0)
                self.current_enemy = self.create_enemy(first_enemy_data)
                self.logger.log_event(f"A wild {self.current_enemy.name} appears!")
            
            # Main game loop
            while self.game_active and self.player and self.player.is_alive():
                self.turn_count += 1
                
                # Player's turn
                self.player_turn()
                
                # Check if enemy was defeated
                if not self.current_enemy.is_alive():
                    self.check_victory()
                    if not self.game_active:
                        break
                    press_enter()
                    continue
                
                # Enemy's turn
                self.enemy_turn()
                
                # Check if player was defeated
                if not self.player.is_alive():
                    self.game_active = False
                    break
            
            # Game over
            self.game_over()
            
        except KeyboardInterrupt:
            print("\nGame interrupted. Thanks for playing!")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("The game will now exit.")
