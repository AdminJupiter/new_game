"""
Game configuration file for Flip Out! - The Mood Swing Card Game
Modify these settings to customize your game experience
"""

# Game Settings
GAME_SETTINGS = {
    'num_players': 4, 'ai_players': 3, 'cards_per_hand': 5, 'game_speed': 'normal',
    'show_ai_thinking': True, 'sound_enabled': True, 'music_enabled': True,
}

# AI Difficulty Settings
AI_SETTINGS = {
    'difficulty': 'medium',  # 'easy', 'medium', 'hard'
    'thinking_delay': 1.0,  # seconds
    'strategy_aggression': 0.7,  # 0.0 to 1.0
    'card_priority': ['mood', 'steal_mood', 'wild_mood', 'swap_hands', 'block_mood', 'double_trouble']
}

# Visual Settings
VISUAL_SETTINGS = {
    'card_animations': True,
    'particle_effects': True,
    'hover_effects': True,
    'glow_effects': True,
    'background_animations': True,
    'card_shadows': True,
    'tooltips_enabled': True,
    'animation_speed': 1.0,  # multiplier
    'color_blind_mode': False,
    'high_contrast': False
}

# Audio Settings
AUDIO_SETTINGS = {
    'master_volume': 0.8,
    'music_volume': 0.6,
    'sfx_volume': 0.8,
    'voice_volume': 0.7,
    'ambient_sounds': True,
    'card_sounds': True,
    'victory_fanfare': True
}

# Balance Settings
BALANCE_SETTINGS = {
    'starting_cards': 5,
    'max_cards_in_hand': 10,
    'mood_cards_per_type': 8,
    'swing_card_counts': {
        'steal_mood': 5,
        'swap_hands': 4,
        'block_mood': 5,
        'double_trouble': 3,
        'wild_mood': 3
    },
    'win_condition_moods': 5
}

# Theme Settings
THEME_SETTINGS = {
    'current_theme': 'default',
    'available_themes': ['default', 'dark', 'pastel', 'neon'],
    'card_back_design': 'classic',
    'background_style': 'animated',
    'font_style': 'modern'
}

# Performance Settings
PERFORMANCE_SETTINGS = {
    'target_fps': 60,
    'vsync_enabled': True,
    'particle_limit': 100,
    'animation_smoothing': True,
    'reduce_animations': False,
    'low_power_mode': False
}

# Enhanced UI Settings
UI_ENHANCEMENTS = {
    'card_hover_lift': True,
    'card_hover_glow': True,
    'selection_animations': True,
    'turn_transitions': True,
    'victory_celebrations': True,
    'interactive_tutorial': False,
    'accessibility_features': True
}

def get_setting(category, key, default=None):
    """Get a setting value from the specified category"""
    if category in globals():
        category_dict = globals()[category]
        return category_dict.get(key, default)
    return default

def update_setting(category, key, value):
    """Update a setting value in the specified category"""
    if category in globals():
        category_dict = globals()[category]
        if key in category_dict:
            category_dict[key] = value
            return True
    return False

def validate_settings():
    """Validate all settings to ensure they are within acceptable ranges"""
    errors = []
    
    # Validate game settings
    if get_setting('GAME_SETTINGS', 'num_players') < 2 or get_setting('GAME_SETTINGS', 'num_players') > 6:
        errors.append("Number of players must be between 2 and 6")
    
    if get_setting('GAME_SETTINGS', 'cards_per_hand') < 1 or get_setting('GAME_SETTINGS', 'cards_per_hand') > 10:
        errors.append("Cards per hand must be between 1 and 10")
    
    # Validate audio settings
    for key in ['master_volume', 'music_volume', 'sfx_volume', 'voice_volume']:
        volume = get_setting('AUDIO_SETTINGS', key)
        if volume < 0.0 or volume > 1.0:
            errors.append(f"{key} must be between 0.0 and 1.0")
    
    # Validate performance settings
    if get_setting('PERFORMANCE_SETTINGS', 'target_fps') < 30 or get_setting('PERFORMANCE_SETTINGS', 'target_fps') > 144:
        errors.append("Target FPS must be between 30 and 144")
    
    if get_setting('PERFORMANCE_SETTINGS', 'particle_limit') < 10 or get_setting('PERFORMANCE_SETTINGS', 'particle_limit') > 500:
        errors.append("Particle limit must be between 10 and 500")
    
    return errors

def get_theme_colors(theme_name='default'):
    """Get color scheme for a specific theme"""
    themes = {
        'default': {
            'background': (34, 139, 34),
            'card_background': (255, 255, 255),
            'text_primary': (255, 255, 255),
            'text_secondary': (200, 200, 200),
            'accent': (255, 255, 0),
            'highlight': (255, 255, 0),
            'shadow': (0, 0, 0, 100)
        },
        'dark': {
            'background': (20, 20, 20),
            'card_background': (50, 50, 50),
            'text_primary': (255, 255, 255),
            'text_secondary': (150, 150, 150),
            'accent': (0, 255, 255),
            'highlight': (0, 255, 255),
            'shadow': (0, 0, 0, 150)
        },
        'pastel': {
            'background': (255, 230, 230),
            'card_background': (255, 255, 255),
            'text_primary': (100, 100, 100),
            'text_secondary': (150, 150, 150),
            'accent': (255, 182, 193),
            'highlight': (173, 216, 230),
            'shadow': (200, 200, 200, 100)
        },
        'neon': {
            'background': (0, 0, 0),
            'card_background': (30, 30, 30),
            'text_primary': (0, 255, 0),
            'text_secondary': (0, 200, 0),
            'accent': (255, 0, 255),
            'highlight': (0, 255, 255),
            'shadow': (0, 255, 0, 100)
        }
    }
    
    return themes.get(theme_name, themes['default'])

def export_settings():
    """Export current settings to a configuration file"""
    import json
    
    all_settings = {}
    for category in ['GAME_SETTINGS', 'AI_SETTINGS', 'VISUAL_SETTINGS', 'AUDIO_SETTINGS', 
                    'BALANCE_SETTINGS', 'THEME_SETTINGS', 'PERFORMANCE_SETTINGS', 'UI_ENHANCEMENTS']:
        all_settings[category] = globals()[category]
    
    try:
        with open('game_config.json', 'w') as f:
            json.dump(all_settings, f, indent=2)
        return True
    except Exception as e:
        print(f"Error exporting settings: {e}")
        return False

def import_settings():
    """Import settings from a configuration file"""
    import json
    import os
    
    if not os.path.exists('game_config.json'):
        return False
    
    try:
        with open('game_config.json', 'r') as f:
            all_settings = json.load(f)
        
        for category, settings in all_settings.items():
            if category in globals():
                globals()[category].update(settings)
        return True
    except Exception as e:
        print(f"Error importing settings: {e}")
        return False
