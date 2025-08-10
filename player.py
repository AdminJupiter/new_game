from constants import *

class Player:
    """Represents a player in the game"""
    def __init__(self, name, is_ai=False):
        self.name = name
        self.hand = []  # Cards in hand
        self.mood_cards = []  # Mood cards played face up
        self.color = None  # Player color for UI
        self.is_ai = is_ai  # Whether this is an AI player
        self.blocked_until = 0  # Turns blocked from certain actions
    
    def add_card_to_hand(self, card):
        """Add a card to the player's hand"""
        self.hand.append(card)
    
    def remove_card_from_hand(self, card_index):
        """Remove a card from hand by index"""
        if 0 <= card_index < len(self.hand):
            return self.hand.pop(card_index)
        return None
    
    def play_mood_card(self, card_index):
        """Play a mood card from hand to the table"""
        if 0 <= card_index < len(self.hand):
            card = self.hand[card_index]
            if hasattr(card, 'mood'):  # Check if it's a mood card
                self.hand.pop(card_index)
                self.mood_cards.append(card)
                return card
        return None
    
    def play_swing_card(self, card_index):
        """Play a mood swing card from hand"""
        if 0 <= card_index < len(self.hand):
            card = self.hand[card_index]
            if hasattr(card, 'card_type'):  # Check if it's a swing card
                self.hand.pop(card_index)
                return card
        return None
    
    def add_mood_card(self, card):
        """Add a mood card to the player's collection"""
        if hasattr(card, 'mood'):
            self.mood_cards.append(card)
            return True
        return False
    
    def remove_mood_card(self, card):
        """Remove a mood card from the player's collection"""
        if card in self.mood_cards:
            self.mood_cards.remove(card)
            return True
        return False
    
    def get_mood_count(self):
        """Get the count of unique moods the player has"""
        unique_moods = set()
        for card in self.mood_cards:
            if hasattr(card, 'mood'):
                unique_moods.add(card.mood)
            elif hasattr(card, 'card_type') and card.card_type == 'wild_mood':
                # Wild mood can represent any mood
                return 5  # Maximum possible
        return len(unique_moods)
    
    def has_mood(self, mood):
        """Check if player has a specific mood"""
        for card in self.mood_cards:
            if hasattr(card, 'mood') and card.mood == mood:
                return True
            elif hasattr(card, 'card_type') and card.card_type == 'wild_mood':
                return True  # Wild mood can represent any mood
        return False
    
    def get_hand_size(self):
        """Get the number of cards in hand"""
        return len(self.hand)
    
    def get_mood_cards_count(self):
        """Get the number of mood cards played"""
        return len(self.mood_cards)
    
    def is_winner(self):
        """Check if player has won (all 5 moods)"""
        return self.get_mood_count() >= 5
    
    def is_blocked(self):
        """Check if player is currently blocked from certain actions"""
        return self.blocked_until > 0
    
    def block_player(self, turns):
        """Block the player for a specified number of turns"""
        self.blocked_until = turns
    
    def unblock_player(self):
        """Remove the block from the player"""
        self.blocked_until = 0
    
    def __str__(self):
        return f"Player({self.name}, Hand: {len(self.hand)}, Moods: {len(self.mood_cards)})"
    
    def __repr__(self):
        return self.__str__()
