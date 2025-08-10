#!/usr/bin/env python3
"""
Launch script for Py_Card - The Mood Swing Card Game
"""

import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import pygame
        print(f"✓ Pygame {pygame.version.ver} is installed")
    except ImportError:
        print("❌ Pygame is not installed!")
        print("Please install it with: pip install pygame")
        return False
    
    return True

def check_assets():
    """Check if required game assets are present"""
    required_dirs = ['image_assets', 'image_assets/Moods', 'image_assets/Moods_Swings']
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"⚠️  Warning: {dir_path} directory not found")
            print("   Some card images may not display correctly")
    
    return True

def main():
    """Main launcher function"""
    print("🎴 Py_Card - The Mood Swing Card Game")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check assets
    check_assets()
    
    print("\n🚀 Launching game...")
    print("   Press ESC to quit")
    print("   Press SPACE to start tutorial")
    print("   Press I for instructions")
    print("   Press S for settings")
    
    try:
        # Import and run the game
        from main import FlipOutGame
        game = FlipOutGame()
        game.run()
    except Exception as e:
        print(f"\n❌ Error launching game: {e}")
        print("Please check that all files are present and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
