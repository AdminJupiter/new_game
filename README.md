# 🎴 Flip Out! - The Mood Swing Card Game

A fun and chaotic card game built with Python and Pygame where players race to collect all 5 moods while dealing with wild mood swings!

## 🎯 Game Objective

Be the first player to collect one of each of the 5 moods:
- 😡 **Angry**
- 😂 **Happy** 
- 😢 **Sad**
- 😨 **Scared**
- 🤪 **Silly**

When you collect all 5, shout **"I FLIPPED OUT!"** and you win!

## 🎭 Card Types

### Mood Cards (40 total)
- 8 copies of each mood
- Play these face up to build your collection

### Mood Swing Cards (20 total)
- **😈 Steal Mood (x5)**: Take a random card from an opponent's hand
- **🤝 Swap Hands (x4)**: Swap your entire hand with another player  
- **🙅 Block Mood (x5)**: Block a steal or discard action
- **🔥 Double Trouble (x3)**: Force a player to discard a mood of your choice
- **🎲 Wild Mood (x3)**: Acts as any one mood to help complete your set

## 🕹️ How to Play

### Setup
- 2-6 players (default: 4)
- Each player starts with 5 cards
- Deck contains 60 cards total

### Turn Structure
1. **Draw 1 card** from the deck
2. **Play up to 1 card** from your hand (Mood or Mood Swing)
3. **Discard 1 card** (optional)

### Gameplay
- **Mood Cards**: Play face up in front of you to build your set
- **Mood Swing Cards**: Use for their special effects, then discard
- **Wild Mood**: Can represent any mood to complete your collection
- **Steal/Swap**: Target other players to mess with their strategy!

## 🚀 Installation & Running

### Prerequisites
- Python 3.7 or higher
- Pygame library

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Game
```bash
python main.py
```

## 🎮 Controls

- **SPACE**: Start the game
- **Mouse Click**: Select cards, target players, interact with deck/discard
- **ENTER**: Play selected card
- **ESC**: Quit game

## 🎨 Game Features

- **Beautiful UI**: Clean, colorful interface with emoji representations
- **Player Targeting**: Click on other players to target them for swing cards
- **Visual Feedback**: Cards highlight when selected, players highlight when targeted
- **Real-time Updates**: See all players' progress and current game state
- **Smooth Gameplay**: 60 FPS smooth animations and interactions

## 🏗️ Project Structure

```
Py_Card/
├── main.py              # Main game loop and initialization
├── constants.py         # Game constants and configuration
├── card.py             # Card classes (MoodCard, MoodSwingCard)
├── player.py            # Player class and game state
├── ui_manager.py        # UI rendering and interaction
├── game_logic.py        # Game rules and logic
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🎯 Strategy Tips

- **Early Game**: Focus on collecting different moods quickly
- **Mid Game**: Use swing cards to disrupt opponents' progress
- **Late Game**: Protect your collection with Block Mood cards
- **Wild Cards**: Save Wild Mood cards for when you're close to winning
- **Targeting**: Focus on players who are ahead in mood collection

## 🐛 Troubleshooting

- **Game won't start**: Make sure Pygame is installed (`pip install pygame`)
- **Display issues**: Check your screen resolution supports 1200x800
- **Performance issues**: Close other applications to free up system resources

## 🎉 Have Fun!

Flip Out! is designed to be chaotic, fun, and full of surprises. Don't get too attached to your mood collection - it might just get stolen or swapped away! 

**Remember**: The best strategy is to stay flexible and embrace the chaos! 🎴✨

---

*Built with ❤️ and Python + Pygame*
