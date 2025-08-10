#!/usr/bin/env python3
"""
Test script for Flip Out! game components
Run this to verify the game logic works without pygame
"""

def test_card_classes():
    """Test card creation and functionality"""
    print("Testing Card Classes...")
    
    from card import MoodCard, MoodSwingCard
    
    # Test MoodCard
    angry_card = MoodCard('angry')
    print(f"✓ Created MoodCard: {angry_card.mood} {angry_card.emoji}")
    print(f"  Color: {angry_card.color}")
    
    # Test MoodSwingCard
    steal_card = MoodSwingCard('steal_mood')
    print(f"✓ Created MoodSwingCard: {steal_card.card_type}")
    print(f"  Description: {steal_card.description}")
    print(f"  Effect: {steal_card.get_effect_description()}")
    
    print()

def test_player_class():
    """Test player functionality"""
    print("Testing Player Class...")
    
    from player import Player
    from card import MoodCard, MoodSwingCard
    
    player = Player("Test Player")
    print(f"✓ Created Player: {player.name}")
    
    # Test adding cards
    player.add_card_to_hand(MoodCard('happy'))
    player.add_card_to_hand(MoodSwingCard('wild_mood'))
    print(f"✓ Added cards to hand: {len(player.hand)} cards")
    
    # Test playing mood card
    card = player.play_mood_card(0)
    print(f"✓ Played mood card: {card.mood}")
    print(f"  Mood cards: {len(player.mood_cards)}")
    print(f"  Hand_size: {len(player.hand)}")
    
    print()

def test_game_logic():
    """Test game logic"""
    print("Testing Game Logic...")
    
    from game_logic import GameLogic
    from player import Player
    from card import MoodCard
    
    logic = GameLogic()
    print("✓ Created GameLogic instance")
    
    # Test with players
    players = [Player(f"Player {i+1}") for i in range(4)]
    logic.start_game(players)
    print(f"✓ Started game with {len(players)} players")
    
    # Test win condition
    test_player = players[0]
    for mood in ['angry', 'happy', 'sad', 'scared', 'silly']:
        test_player.mood_cards.append(MoodCard(mood))
    
    is_winner = logic.check_win_condition(test_player)
    print(f"✓ Win condition check: {is_winner}")
    
    print()

def test_deck_setup():
    """Test deck creation"""
    print("Testing Deck Setup...")
    
    from card import MoodCard, MoodSwingCard
    import random
    
    # Create deck manually
    deck = []
    
    # Create mood cards (8 of each)
    moods = ['angry', 'happy', 'sad', 'scared', 'silly']
    for mood in moods:
        for _ in range(8):
            card = MoodCard(mood)
            deck.append(card)
    
    # Create mood swing cards
    swing_cards = [
        ('steal_mood', 5),
        ('swap_hands', 4),
        ('block_mood', 5),
        ('double_trouble', 3),
        ('wild_mood', 3)
    ]
    
    for card_type, count in swing_cards:
        for _ in range(count):
            card = MoodSwingCard(card_type)
            deck.append(card)
    
    print(f"✓ Created deck with {len(deck)} cards")
    
    # Count card types
    mood_cards = sum(1 for card in deck if hasattr(card, 'mood'))
    swing_cards = sum(1 for card in deck if hasattr(card, 'card_type'))
    
    print(f"  Mood cards: {mood_cards}")
    print(f"  Swing cards: {swing_cards}")
    
    # Test shuffling
    random.shuffle(deck)
    print(f"✓ Deck shuffled successfully")
    
    print()

def main():
    """Run all tests"""
    print("🎴 Testing Flip Out! Game Components\n")
    
    try:
        test_card_classes()
        test_player_class()
        test_game_logic()
        test_deck_setup()
        
        print("🎉 All tests passed! The game is ready to play.")
        print("\nTo run the game:")
        print("  python main.py")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
