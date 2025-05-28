"""
Main entry point for the RPG Game.

This module initializes and starts the game.
"""

def main():
    """Initialize and start the game."""
    from game import Game
    
    print("Starting RPG Game...")
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
