# Game Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Colors
BACKGROUND_COLOR = (20, 40, 80)
TEXT_COLOR = (255, 255, 255)
TITLE_COLOR = (255, 255, 0)
SUBTITLE_COLOR = (200, 200, 200)
MENU_COLOR = (255, 255, 255)
VERSION_COLOR = (150, 150, 150)
TUTORIAL_COLOR = (100, 255, 100)
TEXT_SHADOW_COLOR = (0, 0, 0)

# Additional colors for game elements
TABLE_COLOR = (139, 69, 19)       # Saddle Brown - Table surface
TABLE_BORDER_COLOR = (101, 67, 33) # Dark Brown - Table border
CARD_COLOR = (255, 255, 255)      # White
CARD_BORDER_COLOR = (0, 0, 0)     # Black
HIGHLIGHT_COLOR = (255, 255, 0)   # Yellow
SELECTED_COLOR = (255, 165, 0)    # Orange
TARGET_COLOR = (255, 0, 0)        # Red
PLAY_AREA_COLOR = (160, 82, 45)   # Sienna - Central play area

# Card dimensions
CARD_WIDTH = 80
CARD_HEIGHT = 120
CARD_SPACING = 10

# Table dimensions
TABLE_MARGIN = 50
TABLE_WIDTH = WINDOW_WIDTH - (TABLE_MARGIN * 2)
TABLE_HEIGHT = WINDOW_HEIGHT - (TABLE_MARGIN * 2)
PLAY_AREA_WIDTH = 400
PLAY_AREA_HEIGHT = 300
PLAY_AREA_X = (WINDOW_WIDTH - PLAY_AREA_WIDTH) // 2
PLAY_AREA_Y = (WINDOW_HEIGHT - PLAY_AREA_HEIGHT) // 2

# Player colors
PLAYER_COLORS = [
    (255, 0, 0),      # Red
    (0, 0, 255),      # Blue
    (0, 255, 0),      # Green
    (255, 255, 0),    # Yellow
    (255, 0, 255),    # Magenta
    (0, 255, 255),    # Cyan
]

# Mood emojis
MOOD_EMOJIS = {
    'angry': '😡',
    'happy': '😂',
    'sad': '😢',
    'scared': '😨',
    'silly': '🤪'
}

# Mood Swing card descriptions
SWING_CARD_DESCRIPTIONS = {
    'steal_mood': 'Steal Mood',
    'swap_hands': 'Swap Hands',
    'block_mood': 'Block Mood',
    'double_trouble': 'Double Trouble',
    'wild_mood': 'Wild Mood'
}

# Font sizes
TITLE_FONT_SIZE = 48
HEADER_FONT_SIZE = 24
CARD_FONT_SIZE = 16
SMALL_FONT_SIZE = 12

# Game settings
MAX_PLAYERS = 6
MIN_PLAYERS = 2
CARDS_PER_HAND = 5

# Text rendering improvements
TEXT_ANTIALIAS = True
TEXT_SHADOW_OFFSET = 2
