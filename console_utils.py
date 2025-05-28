"""
Console utility functions for the RPG game.

This module contains utility functions for console operations like clearing the screen,
handling user input, and displaying formatted output.
"""
import os

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def press_enter():
    """Prompt the user to press Enter to continue."""
    input("\nPress Enter to continue...\n")

def print_border():
    """Print a border for visual separation."""
    print("-" * 80)

def print_header(title: str):
    """
    Print a formatted header.
    
    Args:
        title (str): The title to display in the header
    """
    clear_screen()
    print_border()
    print(f"{title:^80}")
    print_border()
    print()
