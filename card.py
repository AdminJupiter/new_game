from constants import *

class Card:
    """Base class for all cards in the game"""
    def __init__(self, name):
        self.name = name
        self.width = CARD_WIDTH
        self.height = CARD_HEIGHT
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Card({self.name})"

class MoodCard(Card):
    """Represents a mood card (angry, happy, sad, scared, silly)"""
    def __init__(self, mood):
        super().__init__(mood)
        self.mood = mood
        self.emoji = MOOD_EMOJIS.get(mood, '❓')
        self.color = self.get_mood_color()
    
    def get_mood_color(self):
        """Get the color associated with each mood"""
        mood_colors = {
            'angry': (255, 0, 0),      # Red
            'happy': (255, 255, 0),    # Yellow
            'sad': (0, 0, 255),        # Blue
            'scared': (128, 0, 128),   # Purple
            'silly': (255, 165, 0)     # Orange
        }
        return mood_colors.get(self.mood, (128, 128, 128))
    
    def __str__(self):
        return f"MoodCard({self.mood})"
    
    def __repr__(self):
        return f"MoodCard({self.mood})"

class MoodSwingCard(Card):
    """Represents a mood swing card (special action cards)"""
    def __init__(self, card_type):
        super().__init__(card_type)
        self.card_type = card_type
        self.description = SWING_CARD_DESCRIPTIONS.get(card_type, card_type)
        self.color = self.get_swing_card_color()
    
    def get_swing_card_color(self):
        """Get the color associated with each swing card type"""
        swing_colors = {
            'steal_mood': (255, 0, 255),    # Magenta
            'swap_hands': (0, 255, 255),    # Cyan
            'block_mood': (128, 128, 128),  # Gray
            'double_trouble': (255, 69, 0), # Red-Orange
            'wild_mood': (255, 215, 0)      # Gold
        }
        return swing_colors.get(self.card_type, (128, 128, 128))
    
    def get_effect_description(self):
        """Get a detailed description of what the card does"""
        effects = {
            'steal_mood': 'Take a random mood card from an opponent',
            'swap_hands': 'Swap your entire hand with another player',
            'block_mood': 'Block a steal or discard action',
            'double_trouble': 'Force a player to discard a mood of your choice',
            'wild_mood': 'Acts as any one mood to complete your set'
        }
        return effects.get(self.card_type, 'Unknown effect')
    
    def __str__(self):
        return f"MoodSwingCard({self.card_type})"
    
    def __repr__(self):
        return f"MoodSwingCard({self.card_type})"
