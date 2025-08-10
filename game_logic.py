import random
from constants import *
from card import Card, MoodCard, MoodSwingCard
from player import Player

class Deck:
    """Represents a deck of cards"""
    
    def __init__(self):
        self.cards = []
        self.create_deck()
    
    def create_deck(self):
        """Create a standard deck with mood cards and mood swing cards"""
        # Create mood cards (5 of each mood)
        moods = ['angry', 'happy', 'sad', 'scared', 'silly']
        for mood in moods:
            for _ in range(5):
                self.cards.append(MoodCard(mood))
        
        # Create mood swing cards
        swing_types = ['steal_mood', 'swap_hands', 'block_mood', 'double_trouble', 'wild_mood']
        for swing_type in swing_types:
            for _ in range(3):  # 3 of each swing card
                self.cards.append(MoodSwingCard(swing_type))
        
        print(f"✓ Created deck with {len(self.cards)} cards")
    
    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)
        print("✓ Deck shuffled")
    
    def draw(self):
        """Draw a card from the top of the deck"""
        if self.cards:
            return self.cards.pop()
        return None
    
    def add_card(self, card):
        """Add a card to the deck"""
        self.cards.append(card)
    
    def add_cards(self, cards):
        """Add multiple cards to the deck"""
        self.cards.extend(cards)
    
    def get_card_count(self):
        """Get the number of cards in the deck"""
        return len(self.cards)
    
    def is_empty(self):
        """Check if the deck is empty"""
        return len(self.cards) == 0

class GameLogic:
    """Handles game rules and logic"""
    
    def __init__(self):
        self.game_phase = "setup"  # setup, playing, game_over
        self.current_turn = 0
        self.turn_order = []
        self.winner = None
    
    def start_game(self, players):
        """Initialize the game with players"""
        self.players = players
        self.turn_order = list(range(len(players)))
        self.current_turn = 0
        self.game_phase = "playing"
        self.winner = None
        
        # Initialize player mood collections
        for player in players:
            if not hasattr(player, 'mood_cards'):
                player.mood_cards = []
            if not hasattr(player, 'blocked_until'):
                player.blocked_until = 0
    
    def get_current_player(self):
        """Get the current player"""
        if self.turn_order:
            return self.players[self.turn_order[self.current_turn]]
        return None
    
    def next_turn(self):
        """Move to the next player's turn"""
        if self.game_phase == "playing":
            self.current_turn = (self.current_turn + 1) % len(self.turn_order)
            
            # Check if current player is blocked
            current_player = self.get_current_player()
            if hasattr(current_player, 'blocked_until') and current_player.blocked_until > 0:
                current_player.blocked_until -= 1
                if current_player.blocked_until <= 0:
                    print(f"🎉 {current_player.name} is no longer blocked!")
    
    def can_play_card(self, player, card_index):
        """Check if a player can play a specific card"""
        if card_index >= len(player.hand):
            return False
        
        card = player.hand[card_index]
        
        # Check if it's a mood card - blocked players can still collect moods
        if hasattr(card, 'mood'):
            return True
        
        # Check if it's a mood swing card
        if hasattr(card, 'card_type'):
            # Check if player is blocked from stealing/discarding
            if hasattr(player, 'blocked_until') and player.blocked_until > 0:
                if card.card_type in ['steal_mood', 'double_trouble']:
                    return False  # Blocked players can't steal or force discards
                # Blocked players can still use other swing cards
            return self.can_play_swing_card(card, player)
        
        return False
    
    def can_play_swing_card(self, card, player):
        """Check if a mood swing card can be played"""
        # Check if player is blocked from stealing/discarding
        if hasattr(player, 'blocked_until') and player.blocked_until > 0:
            if card.card_type in ['steal_mood', 'double_trouble']:
                return False  # Blocked players can't steal or force discards
        
        # All other swing cards can be played
        return True
    
    def play_mood_card(self, player, card_index):
        """Play a mood card"""
        if not self.can_play_card(player, card_index):
            return False, "Cannot play this card"
        
        card = player.hand.pop(card_index)
        
        if hasattr(card, 'mood'):
            player.mood_cards.append(card)
            return True, f"Played {card.mood} mood card"
        else:
            # Put the card back
            player.hand.insert(card_index, card)
            return False, "Not a mood card"
    
    def play_swing_card(self, player, card_index, target_player=None):
        """Play a mood swing card"""
        if not self.can_play_card(player, card_index):
            return False, "Cannot play this card"
        
        card = player.hand.pop(card_index)
        
        if hasattr(card, 'card_type'):
            result = self.execute_swing_card_effect(card, player, target_player)
            return True, result
        else:
            # Put the card back
            player.hand.insert(card_index, card)
            return False, "Not a swing card"
    
    def execute_swing_card_effect(self, card, player, target_player):
        """Execute the effect of a mood swing card according to the exact rules"""
        if card.card_type == 'steal_mood':
            if target_player and target_player.hand:
                # Steal a random card from opponent's hand (not just mood cards)
                stolen_card = random.choice(target_player.hand)
                target_player.hand.remove(stolen_card)
                player.hand.append(stolen_card)
                return f"Stole {stolen_card.name} from {target_player.name}!"
            else:
                return "No cards to steal!"
        
        elif card.card_type == 'swap_hands':
            if target_player:
                # Swap hands between players
                player.hand, target_player.hand = target_player.hand, player.hand
                return f"Swapped hands with {target_player.name}!"
            else:
                return "No target player selected!"
        
        elif card.card_type == 'block_mood':
            if target_player:
                # Block target player from stealing or discarding cards (not mood collection)
                target_player.blocked_until = 2
                return f"Blocked {target_player.name} from stealing/discarding for 2 turns!"
            else:
                return "No target player selected!"
        
        elif card.card_type == 'double_trouble':
            if target_player:
                # Force target player to discard a mood of choice (not draw 2 cards)
                # This will be handled in the main game loop with UI selection
                return f"Double trouble! {target_player.name} must discard a mood of your choice!"
            else:
                return "No target player selected!"
        
        elif card.card_type == 'wild_mood':
            # Player can choose any mood type to collect
            # This will be handled in the main game loop with UI selection
            return "Wild mood! Choose any mood type to collect!"
        
        return "Unknown swing card effect!"
    
    def check_win_condition(self, player):
        """Check if a player has won by collecting one of each of the 5 moods"""
        if not hasattr(player, 'mood_cards'):
            return False
        
        # Count unique moods collected
        unique_moods = set()
        for card in player.mood_cards:
            if hasattr(card, 'mood'):
                unique_moods.add(card.mood)
        
        # Check if player has all 5 moods
        required_moods = {'angry', 'happy', 'sad', 'scared', 'silly'}
        return unique_moods.issuperset(required_moods)
    
    def get_game_state(self):
        """Get the current game state"""
        return {
            'phase': self.game_phase,
            'current_turn': self.current_turn,
            'current_player': self.get_current_player().name if self.get_current_player() else None,
            'winner': self.winner.name if self.winner else None,
            'players': [{
                'name': p.name,
                'hand_size': len(p.hand),
                'mood_count': p.get_mood_count(),
                'mood_cards': [str(card) for card in p.mood_cards]
            } for p in self.players]
        }
    
    def is_game_over(self):
        """Check if the game is over"""
        return self.winner is not None
    
    def end_game(self, winner):
        """End the game with a winner"""
        self.winner = winner
        self.game_phase = "game_over"
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.game_phase = "setup"
        self.current_turn = 0
        self.turn_order = []
        self.winner = None
