import pygame
import os
import math
from constants import *
import random
from game_config import get_setting, update_setting, get_theme_colors, export_settings, import_settings

class SettingsMenu:
    """Settings menu for game configuration"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.visible = False
        self.current_category = 0
        self.current_option = 0
        self.categories = ['Game', 'AI', 'Visual', 'Audio', 'Performance']
        self.options = {
            'Game': ['Number of Players', 'Cards per Hand', 'Game Speed'],
            'AI': ['Difficulty', 'Thinking Delay', 'Strategy Aggression'],
            'Visual': ['Card Animations', 'Particle Effects', 'Theme'],
            'Audio': ['Master Volume', 'Music Volume', 'SFX Volume'],
            'Performance': ['Target FPS', 'VSync', 'Particle Limit']
        }
        self.values = {
            'Number of Players': [2, 3, 4, 5, 6],
            'Cards per Hand': [3, 4, 5, 6, 7],
            'Game Speed': ['Slow', 'Normal', 'Fast'],
            'Difficulty': ['Easy', 'Medium', 'Hard'],
            'Thinking Delay': [0.5, 1.0, 1.5, 2.0],
            'Strategy Aggression': [0.3, 0.5, 0.7, 0.9],
            'Card Animations': [True, False],
            'Particle Effects': [True, False],
            'Theme': ['Default', 'Dark', 'Pastel', 'Neon'],
            'Master Volume': [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            'Music Volume': [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            'SFX Volume': [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            'Target FPS': [30, 45, 60, 90, 120],
            'VSync': [True, False],
            'Particle Limit': [50, 100, 200, 300, 500]
        }
        self.current_values = {
            'Number of Players': 4,
            'Cards per Hand': 5,
            'Game Speed': 'Normal',
            'Difficulty': 'Medium',
            'Thinking Delay': 1.0,
            'Strategy Aggression': 0.7,
            'Card Animations': True,
            'Particle Effects': True,
            'Theme': 'Default',
            'Master Volume': 0.8,
            'Music Volume': 0.6,
            'SFX Volume': 0.8,
            'Target FPS': 60,
            'VSync': True,
            'Particle Limit': 100
        }
        self.load_current_settings()
    
    def load_current_settings(self):
        """Load current settings from game_config"""
        self.current_values['Number of Players'] = get_setting('GAME_SETTINGS', 'num_players', 4)
        self.current_values['Cards per Hand'] = get_setting('GAME_SETTINGS', 'cards_per_hand', 5)
        self.current_values['Difficulty'] = get_setting('AI_SETTINGS', 'difficulty', 'Medium').title()
        self.current_values['Thinking Delay'] = get_setting('AI_SETTINGS', 'thinking_delay', 1.0)
        self.current_values['Strategy Aggression'] = get_setting('AI_SETTINGS', 'strategy_aggression', 0.7)
        self.current_values['Card Animations'] = get_setting('VISUAL_SETTINGS', 'card_animations', True)
        self.current_values['Particle Effects'] = get_setting('VISUAL_SETTINGS', 'particle_effects', True)
        self.current_values['Theme'] = get_setting('THEME_SETTINGS', 'current_theme', 'Default').title()
        self.current_values['Master Volume'] = get_setting('AUDIO_SETTINGS', 'master_volume', 0.8)
        self.current_values['Music Volume'] = get_setting('AUDIO_SETTINGS', 'music_volume', 0.6)
        self.current_values['SFX Volume'] = get_setting('AUDIO_SETTINGS', 'sfx_volume', 0.8)
        self.current_values['Target FPS'] = get_setting('PERFORMANCE_SETTINGS', 'target_fps', 60)
        self.current_values['VSync'] = get_setting('PERFORMANCE_SETTINGS', 'vsync_enabled', True)
        self.current_values['Particle Limit'] = get_setting('PERFORMANCE_SETTINGS', 'particle_limit', 100)
    
    def handle_input(self, event):
        """Handle input for settings menu"""
        if not self.visible:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.visible = False
                return True
            elif event.key == pygame.K_UP:
                self.current_option = (self.current_option - 1) % len(self.options[self.categories[self.current_category]])
                return True
            elif event.key == pygame.K_DOWN:
                self.current_option = (self.current_option + 1) % len(self.options[self.categories[self.current_category]])
                return True
            elif event.key == pygame.K_LEFT:
                self.current_category = (self.current_category - 1) % len(self.categories)
                self.current_option = 0
                return True
            elif event.key == pygame.K_RIGHT:
                self.current_category = (self.current_category + 1) % len(self.categories)
                self.current_option = 0
                return True
            elif event.key == pygame.K_RETURN:
                self.change_current_value()
                return True
            elif event.key == pygame.K_s:
                self.save_settings()
                return True
        
        return False
    
    def change_current_value(self):
        """Change the value of the currently selected option"""
        category = self.categories[self.current_category]
        option = self.options[category][self.current_option]
        current_value = self.current_values[option]
        value_list = self.values[option]
        
        try:
            current_index = value_list.index(current_value)
            new_index = (current_index + 1) % len(value_list)
            self.current_values[option] = value_list[new_index]
        except ValueError:
            # If current value not in list, use first value
            self.current_values[option] = value_list[0]
    
    def save_settings(self):
        """Save current settings to game_config"""
        # Update game_config with new values
        update_setting('GAME_SETTINGS', 'num_players', self.current_values['Number of Players'])
        update_setting('GAME_SETTINGS', 'cards_per_hand', self.current_values['Cards per Hand'])
        update_setting('AI_SETTINGS', 'difficulty', self.current_values['Difficulty'].lower())
        update_setting('AI_SETTINGS', 'thinking_delay', self.current_values['Thinking Delay'])
        update_setting('AI_SETTINGS', 'strategy_aggression', self.current_values['Strategy Aggression'])
        update_setting('VISUAL_SETTINGS', 'card_animations', self.current_values['Card Animations'])
        update_setting('VISUAL_SETTINGS', 'particle_effects', self.current_values['Particle Effects'])
        update_setting('THEME_SETTINGS', 'current_theme', self.current_values['Theme'].lower())
        update_setting('AUDIO_SETTINGS', 'master_volume', self.current_values['Master Volume'])
        update_setting('AUDIO_SETTINGS', 'music_volume', self.current_values['Music Volume'])
        update_setting('AUDIO_SETTINGS', 'sfx_volume', self.current_values['SFX Volume'])
        update_setting('PERFORMANCE_SETTINGS', 'target_fps', self.current_values['Target FPS'])
        update_setting('PERFORMANCE_SETTINGS', 'vsync_enabled', self.current_values['VSync'])
        update_setting('PERFORMANCE_SETTINGS', 'particle_limit', self.current_values['Particle Limit'])
        
        # Export settings to file
        export_settings()
    
    def render(self):
        """Render the settings menu"""
        if not self.visible:
            return
        
        # Semi-transparent background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Settings panel
        panel_width = 800
        panel_height = 600
        panel_x = (WINDOW_WIDTH - panel_width) // 2
        panel_y = (WINDOW_HEIGHT - panel_height) // 2
        
        # Panel background
        pygame.draw.rect(self.screen, (50, 50, 50), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, (100, 100, 100), (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Title
        title_text = self.font_large.render("Settings", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, panel_y + 40))
        self.screen.blit(title_text, title_rect)
        
        # Categories (horizontal tabs)
        tab_width = 120
        tab_height = 40
        for i, category in enumerate(self.categories):
            tab_x = panel_x + 20 + i * (tab_width + 10)
            tab_y = panel_y + 80
            
            # Tab background
            tab_color = (100, 100, 100) if i == self.current_category else (70, 70, 70)
            pygame.draw.rect(self.screen, tab_color, (tab_x, tab_y, tab_width, tab_height))
            pygame.draw.rect(self.screen, (150, 150, 150), (tab_x, tab_y, tab_width, tab_height), 2)
            
            # Tab text
            tab_text = self.font_small.render(category, True, (255, 255, 255))
            tab_text_rect = tab_text.get_rect(center=(tab_x + tab_width // 2, tab_y + tab_height // 2))
            self.screen.blit(tab_text, tab_text_rect)
        
        # Options for current category
        options = self.options[self.categories[self.current_category]]
        option_y = panel_y + 140
        
        for i, option in enumerate(options):
            option_x = panel_x + 40
            option_color = (255, 255, 0) if i == self.current_option else (255, 255, 255)
            
            # Option name
            option_text = self.font_medium.render(option, True, option_color)
            self.screen.blit(option_text, (option_x, option_y + i * 50))
            
            # Current value
            current_value = self.current_values[option]
            value_text = self.font_small.render(str(current_value), True, (200, 200, 200))
            value_rect = value_text.get_rect(right=panel_x + panel_width - 40)
            value_rect.centery = option_y + i * 50 + 18
            self.screen.blit(value_text, value_rect)
            
            # Selection indicator
            if i == self.current_option:
                pygame.draw.rect(self.screen, (255, 255, 0), (option_x - 20, option_y + i * 50, 10, 30), 3)
        
        # Instructions
        instructions = [
            "Use ARROW KEYS to navigate",
            "ENTER to change values",
            "S to save settings",
            "ESC to close menu"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.font_small.render(instruction, True, (150, 150, 150))
            inst_rect = inst_text.get_rect(center=(WINDOW_WIDTH // 2, panel_y + panel_height - 80 + i * 25))
            self.screen.blit(inst_text, inst_rect)

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)
        
        # UI state
        self.instructions_visible = False
        self.settings_visible = False
        
        # Store players reference for card detection
        self.players = []
        
        # Load card images
        self.card_images = {}
        self.load_card_images()
        
        # Animation variables
        self.hover_animation = 0
        self.card_flip_animation = 0
        self.particle_effects = []
        
        # Settings menu
        self.settings_menu = SettingsMenu(screen)
        
    def load_card_images(self):
        """Load all card images from the image_assets directory"""
        try:
            # Load mood cards
            mood_dir = "image_assets/Moods"
            for mood in ['angry', 'happy', 'sad', 'scared', 'silly']:
                image_path = os.path.join(mood_dir, f"{mood.capitalize()}.png")
                if os.path.exists(image_path):
                    image = pygame.image.load(image_path)
                    # Scale to standard card size
                    image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
                    self.card_images[mood] = image
                    print(f"✓ Loaded {mood} card image")
                else:
                    print(f"⚠ Warning: {image_path} not found")
            
            # Load mood swing cards
            swing_dir = "image_assets/Moods_Swings"
            swing_mapping = {
                'wild_mood': 'Wild.png',
                'double_trouble': 'Double.png',
                'block_mood': 'Block.png',
                'steal_mood': 'Steal.png',
                'swap_hands': 'Swap.png'
            }
            
            for card_type, filename in swing_mapping.items():
                image_path = os.path.join(swing_dir, filename)
                if os.path.exists(image_path):
                    image = pygame.image.load(image_path)
                    # Scale to standard card size
                    image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
                    self.card_images[card_type] = image
                    print(f"✓ Loaded {card_type} card image")
                else:
                    print(f"⚠ Warning: {image_path} not found")
                    
        except Exception as e:
            print(f"Error loading card images: {e}")
            # Fallback to colored rectangles if images fail to load
            self.card_images = {}
    
    def draw_title_screen(self):
        """Draw the title screen"""
        # Draw background
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_background_pattern()
        
        # Draw title
        title_font = pygame.font.Font(None, 72)
        title_surface = title_font.render("🎴 Flip Out!", True, TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        self.screen.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_font = pygame.font.Font(None, 36)
        subtitle_surface = subtitle_font.render("The Mood Swing Card Game", True, SUBTITLE_COLOR)
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 60))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw floating cards animation
        self.draw_floating_cards()
        
        # Draw menu options
        menu_font = pygame.font.Font(None, 32)
        menu_options = [
            ("🎓 SPACE - Start Tutorial", TUTORIAL_COLOR),
            ("🎮 I - Instructions", MENU_COLOR),
            ("⚙️ S - Settings", MENU_COLOR),
            ("❌ ESC - Quit", MENU_COLOR)
        ]
        
        start_y = WINDOW_HEIGHT * 2 // 3
        for i, (text, color) in enumerate(menu_options):
            option_surface = menu_font.render(text, True, color)
            option_rect = option_surface.get_rect(center=(WINDOW_WIDTH // 2, start_y + i * 40))
            self.screen.blit(option_surface, option_rect)
        
        # Draw version info
        version_font = pygame.font.Font(None, 20)
        version_surface = version_font.render("v1.0 - Interactive Tutorial Available!", True, VERSION_COLOR)
        version_rect = version_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        self.screen.blit(version_surface, version_rect)
    
    def draw_game_instructions(self):
        """Draw the game instructions screen"""
        self.screen.fill(BACKGROUND_COLOR)
        
        # Title
        title_font = pygame.font.Font(None, 48)
        title_surface = title_font.render("📖 How to Play Flip Out!", True, TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.screen.blit(title_surface, title_rect)
        
        # Instructions content
        instructions = [
            "🎯 Objective: Collect one of each of the 5 moods to win!",
            "",
            "🎴 Card Types:",
            "  • Mood Cards: 😡 Angry, 😂 Happy, 😢 Sad, 😨 Scared, 🤪 Silly",
            "  • Mood Swing Cards: Special effects that help or hinder players",
            "",
            "🔄 Turn Structure:",
            "  1. Draw 1 card from the deck",
            "  2. Play up to 1 card (optional)",
            "  3. Discard 1 card (optional)",
            "",
            "🎮 Controls:",
            "  • Click deck to draw • Click and drag cards to play/discard",
            "  • SPACE to advance turn phases • ESC to quit",
            "",
            "💡 Tip: Use the Tutorial (SPACE on title screen) to learn step-by-step!"
        ]
        
        instruction_font = pygame.font.Font(None, 24)
        start_y = 120
        for i, instruction in enumerate(instructions):
            if instruction.strip():  # Only render non-empty lines
                color = TITLE_COLOR if instruction.startswith("🎯") else (
                    SUBTITLE_COLOR if instruction.startswith("🎴") or instruction.startswith("🔄") or instruction.startswith("🎮") or instruction.startswith("💡") else
                    (255, 255, 255) if instruction.startswith("  •") else
                    (200, 200, 200)
                )
                instruction_surface = instruction_font.render(instruction, True, color)
                instruction_rect = instruction_surface.get_rect(left=50, top=start_y + i * 25)
                self.screen.blit(instruction_surface, instruction_rect)
        
        # Back instruction
        back_font = pygame.font.Font(None, 28)
        back_surface = back_font.render("Press ESC to return to title screen", True, MENU_COLOR)
        back_rect = back_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        self.screen.blit(back_surface, back_rect)
    
    def draw_tutorial_screen(self, players, state, deck, discard_pile, tutorial_steps, drag_manager):
        """Draw the tutorial screen with new architecture"""
        # Draw the game screen first
        self.draw_game_screen(players, state, deck, discard_pile, drag_manager)
        
        # Draw tutorial overlay
        self.draw_tutorial_overlay(state.tutorial_step, tutorial_steps)
        
        # Draw dragging card if in dragging step
        if state.tutorial_step == 3 and drag_manager.dragging:
            mouse_pos = pygame.mouse.get_pos()
            card_x = mouse_pos[0] - CARD_WIDTH // 2
            card_y = mouse_pos[1] - CARD_HEIGHT // 2
            self.draw_card_image(drag_manager.dragged_card, card_x, card_y, highlight=True)
    
    def draw_tutorial_overlay(self, tutorial_step, tutorial_steps):
        """Draw the tutorial overlay with current step information"""
        if tutorial_step >= len(tutorial_steps):
            return
        
        current_step = tutorial_steps[tutorial_step]
        
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Tutorial box
        box_width = 600
        box_height = 200
        box_x = (WINDOW_WIDTH - box_width) // 2
        box_y = 50
        
        # Draw tutorial box with gradient
        tutorial_box = pygame.Surface((box_width, box_height))
        tutorial_box.fill((50, 50, 100))
        pygame.draw.rect(tutorial_box, (100, 100, 150), tutorial_box.get_rect(), 3)
        pygame.draw.rect(tutorial_box, (30, 30, 80), (5, 5, box_width - 10, box_height - 10), 2)
        self.screen.blit(tutorial_box, (box_x, box_y))
        
        # Step indicator
        step_font = pygame.font.Font(None, 20)
        step_text = f"Step {tutorial_step + 1} of {len(tutorial_steps)}"
        step_surface = step_font.render(step_text, True, (200, 200, 200))
        step_rect = step_surface.get_rect(topright=(box_x + box_width - 20, box_y + 15))
        self.screen.blit(step_surface, step_rect)
        
        # Title
        title_font = pygame.font.Font(None, 32)
        title_surface = title_font.render(current_step['title'], True, (255, 255, 0))
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, box_y + 40))
        self.screen.blit(title_surface, title_rect)
        
        # Description
        desc_font = pygame.font.Font(None, 24)
        desc_surface = desc_font.render(current_step['description'], True, (255, 255, 255))
        desc_rect = desc_surface.get_rect(center=(WINDOW_WIDTH // 2, box_y + 80))
        self.screen.blit(desc_surface, desc_rect)
        
        # Action required
        action_font = pygame.font.Font(None, 28)
        action_surface = action_font.render(current_step['action'], True, (100, 255, 100))
        action_rect = action_surface.get_rect(center=(WINDOW_WIDTH // 2, box_y + 120))
        self.screen.blit(action_surface, action_rect)
        
        # Special instruction for dragging step
        if tutorial_step == 3:  # Dragging step
            special_font = pygame.font.Font(None, 20)
            special_text = "💡 Tip: Hold down the mouse button and move the mouse to drag"
            special_surface = special_font.render(special_text, True, (255, 255, 100))
            special_rect = special_surface.get_rect(center=(WINDOW_WIDTH // 2, box_y + 150))
            self.screen.blit(special_surface, special_rect)
        
        # Progress bar
        progress_width = box_width - 40
        progress_height = 8
        progress_x = box_x + 20
        progress_y = box_y + 160 if tutorial_step != 3 else box_y + 180
        
        # Background bar
        pygame.draw.rect(self.screen, (100, 100, 100), (progress_x, progress_y, progress_width, progress_height))
        
        # Progress fill
        progress_fill = (tutorial_step + 1) / len(tutorial_steps)
        fill_width = int(progress_width * progress_fill)
        pygame.draw.rect(self.screen, (100, 255, 100), (progress_x, progress_y, fill_width, progress_height))
        
        # Highlight relevant game elements based on current step
        self.draw_tutorial_highlights(current_step['highlight'])
    
    def draw_tutorial_highlights(self, highlight_type):
        """Draw highlights around relevant game elements for the current tutorial step"""
        if not highlight_type:
            return
        
        highlight_color = (255, 255, 0, 128)  # Semi-transparent yellow
        highlight_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        
        if highlight_type == 'deck':
            # Highlight deck
            deck_rect = pygame.Rect(WINDOW_WIDTH // 2 - 40, WINDOW_HEIGHT // 2 - CARD_HEIGHT // 2,
                                   CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(highlight_surface, highlight_color, deck_rect, 5)
            # Add pulsing effect
            pulse_alpha = int(128 + 64 * (pygame.time.get_ticks() % 1000) / 1000)
            pulse_surface = pygame.Surface((CARD_WIDTH + 20, CARD_HEIGHT + 20), pygame.SRCALPHA)
            pygame.draw.rect(pulse_surface, (255, 255, 0, pulse_alpha), pulse_surface.get_rect(), 3)
            self.screen.blit(pulse_surface, (deck_rect.x - 10, deck_rect.y - 10))
        
        elif highlight_type == 'player_hand':
            # Highlight player's hand area
            hand_start_x = 50
            hand_y = WINDOW_HEIGHT - CARD_HEIGHT - 50
            for i in range(5):  # Assuming 5 cards
                card_x = hand_start_x + i * (CARD_WIDTH + 10)
                card_rect = pygame.Rect(card_x, hand_y, CARD_WIDTH, CARD_HEIGHT)
                pygame.draw.rect(highlight_surface, highlight_color, card_rect, 5)
        
        elif highlight_type == 'play_area':
            # Highlight opponents and discard pile
            for i in range(1, 4):  # AI players
                player_rect = self.get_player_rect(i)
                pygame.draw.rect(highlight_surface, highlight_color, player_rect, 5)
            
            # Highlight discard pile
            discard_rect = pygame.Rect(WINDOW_WIDTH // 2 + 40, WINDOW_HEIGHT // 2 - CARD_HEIGHT // 2,
                                     CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(highlight_surface, highlight_color, discard_rect, 5)
        
        elif highlight_type == 'controls':
            # Highlight the controls area
            controls_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 100, 200, 80)
            pygame.draw.rect(highlight_surface, highlight_color, controls_rect, 5)
        
        self.screen.blit(highlight_surface, (0, 0))
    
    def draw_floating_cards(self):
        """Draw animated floating cards in the background"""
        # Draw some floating cards for visual appeal
        for i in range(5):
            angle = (self.hover_animation * 0.5 + i * 1.2) % (2 * math.pi)
            x = int(WINDOW_WIDTH * 0.1 + i * 200)
            y = int(100 + 50 * math.sin(angle + i * 0.5))
            
            # Draw simple card shape
            card_rect = pygame.Rect(x, y, 40, 60)
            pygame.draw.rect(self.screen, CARD_COLOR, card_rect)
            pygame.draw.rect(self.screen, CARD_BORDER_COLOR, card_rect, 1)
            
            # Add some mood emojis
            emojis = ['😡', '😂', '😢', '😨', '🤪']
            emoji = emojis[i % len(emojis)]
            emoji_surface = self.font_small.render(emoji, True, (0, 0, 0))
            emoji_rect = emoji_surface.get_rect(center=(x + 20, y + 30))
            self.screen.blit(emoji_surface, emoji_rect)
    
    def draw_background_pattern(self):
        """Draw a subtle background pattern"""
        # Draw subtle grid pattern
        for x in range(0, WINDOW_WIDTH, 40):
            for y in range(0, WINDOW_HEIGHT, 40):
                if (x + y) % 80 == 0:
                    pygame.draw.circle(self.screen, (0, 100, 0), (x, y), 1)
    
    def draw_table_interface(self):
        """Draw the main table interface with central play area"""
        # Draw table surface
        table_rect = pygame.Rect(TABLE_MARGIN, TABLE_MARGIN, TABLE_WIDTH, TABLE_HEIGHT)
        pygame.draw.rect(self.screen, TABLE_COLOR, table_rect)
        pygame.draw.rect(self.screen, TABLE_BORDER_COLOR, table_rect, 3)
        
        # Draw central play area (like UNO's center)
        play_area_rect = pygame.Rect(PLAY_AREA_X, PLAY_AREA_Y, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT)
        pygame.draw.rect(self.screen, PLAY_AREA_COLOR, play_area_rect)
        pygame.draw.rect(self.screen, TABLE_BORDER_COLOR, play_area_rect, 2)
        
        # Add subtle texture to play area
        for i in range(0, PLAY_AREA_WIDTH, 20):
            for j in range(0, PLAY_AREA_HEIGHT, 20):
                if (i + j) % 40 == 0:
                    pygame.draw.circle(self.screen, (139, 69, 19), 
                                     (PLAY_AREA_X + i, PLAY_AREA_Y + j), 1)
    
    def draw_text_with_shadow(self, text, font, color, position, shadow_color=TEXT_SHADOW_COLOR):
        """Draw text with shadow for better readability"""
        # Draw shadow
        shadow_surface = font.render(text, TEXT_ANTIALIAS, shadow_color)
        shadow_rect = shadow_surface.get_rect(center=(position[0] + TEXT_SHADOW_OFFSET, 
                                                     position[1] + TEXT_SHADOW_OFFSET))
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Draw main text
        text_surface = font.render(text, TEXT_ANTIALIAS, color)
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect)
        
        return text_rect
    
    def add_particle_effect(self, x, y, effect_type='sparkle'):
        """Add a particle effect at the specified location"""
        if effect_type == 'sparkle':
            for _ in range(8):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 6)
                particle = {
                    'x': x,
                    'y': y,
                    'dx': math.cos(angle) * speed,
                    'dy': math.sin(angle) * speed,
                    'life': 30,
                    'color': (255, 255, 0),
                    'size': random.uniform(1, 3)
                }
                self.particle_effects.append(particle)
        elif effect_type == 'glow':
            for _ in range(5):
                particle = {
                    'x': x + random.uniform(-10, 10),
                    'y': y + random.uniform(-10, 10),
                    'dx': 0,
                    'dy': -1,
                    'life': 20,
                    'color': (255, 255, 255),
                    'size': random.uniform(2, 4)
                }
                self.particle_effects.append(particle)
    
    def draw_particle_effects(self):
        """Draw all active particle effects"""
        for particle in self.particle_effects:
            # Update particle position
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            
            # Draw particle
            if particle['life'] > 0:
                alpha = int(255 * (particle['life'] / 30))
                color = (*particle['color'][:3], alpha)
                
                particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, color, (particle['size'], particle['size']), particle['size'])
                self.screen.blit(particle_surface, (particle['x'] - particle['size'], particle['y'] - particle['size']))
    
    def draw_game_screen(self, players, state, deck, discard_pile, drag_manager):
        """Draw the main game screen with new architecture"""
        # Draw background
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_background_pattern()
        
        # Draw table interface
        self.draw_table_interface()
        
        # Draw players
        for i, player in enumerate(players):
            self.draw_player(player, i, state.current_player_index)
        
        # Draw deck
        if deck and deck.cards:
            deck_x = WINDOW_WIDTH // 2 - 40
            deck_y = WINDOW_HEIGHT // 2 - CARD_HEIGHT // 2
            self.draw_deck(deck_x, deck_y, len(deck.cards))
        
        # Draw discard pile
        if discard_pile:
            discard_x = WINDOW_WIDTH // 2 + 40
            discard_y = WINDOW_HEIGHT // 2 - CARD_HEIGHT // 2
            self.draw_discard_pile(discard_x, discard_y, discard_pile[-1], len(discard_pile))
        
        # Draw game message
        if state.game_message:
            self.draw_game_message(state.game_message)
        
        # Draw turn phase indicator
        self.draw_turn_phase_indicator(state.turn_phase)
        
        # Draw game controls
        self.draw_game_controls(state.turn_phase)
        
        # Draw dragging card
        if drag_manager.dragging and drag_manager.dragged_card:
            mouse_pos = pygame.mouse.get_pos()
            card_x = mouse_pos[0] - CARD_WIDTH // 2
            card_y = mouse_pos[1] - CARD_HEIGHT // 2
            self.draw_card_image(drag_manager.dragged_card, card_x, card_y, highlight=True)
    
    def draw_deck_and_discard(self, deck, discard_pile):
        """Draw the deck and discard pile in the central play area"""
        # Position deck and discard in the center play area
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        # Deck (left side of center)
        deck_x = center_x - 120
        deck_y = center_y - CARD_HEIGHT // 2
        
        # Draw deck with multiple card effect
        for i in range(min(3, len(deck))):
            offset = i * 2
            card_rect = pygame.Rect(deck_x + offset, deck_y + offset, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(self.screen, CARD_COLOR, card_rect)
            pygame.draw.rect(self.screen, CARD_BORDER_COLOR, card_rect, 2)
        
        # Deck count with simple text (no shadow)
        count_text = f"Deck: {len(deck)}"
        count_surface = self.font_small.render(count_text, True, (255, 255, 255))
        count_rect = count_surface.get_rect(center=(deck_x + CARD_WIDTH // 2, deck_y + CARD_HEIGHT + 20))
        self.screen.blit(count_surface, count_rect)
        
        # Discard pile (right side of center)
        discard_x = center_x + 40
        discard_y = center_y - CARD_HEIGHT // 2
        
        if discard_pile:
            # Draw top card of discard pile
            top_card = discard_pile[-1]
            self.draw_card_image(top_card, discard_x, discard_y, highlight=False)
        else:
            # Empty discard pile
            discard_rect = pygame.Rect(discard_x, discard_y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(self.screen, (100, 100, 100), discard_rect, 2)
            pygame.draw.rect(self.screen, (50, 50, 50), discard_rect)
        
        # Discard count with simple text (no shadow)
        discard_text = f"Discard: {len(discard_pile)}"
        discard_surface = self.font_small.render(discard_text, True, (255, 255, 255))
        discard_rect = discard_surface.get_rect(center=(discard_x + CARD_WIDTH // 2, discard_y + CARD_HEIGHT + 20))
        self.screen.blit(discard_surface, discard_rect)
    
    def draw_player(self, player, player_index, current_player_index, selected_card, target_player):
        """Draw a player area with simplified positioning to fix UI issues"""
        # Use simple grid positioning instead of complex circular math
        # Ensure all players are visible within screen bounds
        if player_index == 0:  # Top player
            player_x = WINDOW_WIDTH // 2
            player_y = 180  # Increased from 120 to give more space from top UI
        elif player_index == 1:  # Right player
            player_x = WINDOW_WIDTH - 200  # Moved left from 150 to give more space
            player_y = WINDOW_HEIGHT // 2
        elif player_index == 2:  # Bottom player
            player_x = WINDOW_WIDTH // 2
            player_y = WINDOW_HEIGHT - 200  # Increased from 100 to ensure visibility
        else:  # Left player (player_index == 3)
            player_x = 200  # Moved right from 150 to give more space
            player_y = WINDOW_HEIGHT // 2
        
        # Draw player background highlight if it's the current player
        if player_index == current_player_index:
            # Draw a highlighted background for current player
            highlight_rect = pygame.Rect(player_x - 200, player_y - 80, 400, 160)
            pygame.draw.rect(self.screen, (50, 100, 50, 100), highlight_rect)
            pygame.draw.rect(self.screen, (0, 255, 0), highlight_rect, 3)
        
        # Draw player background for better visibility (all players)
        player_bg_rect = pygame.Rect(player_x - 200, player_y - 80, 400, 160)
        pygame.draw.rect(self.screen, (0, 0, 0, 50), player_bg_rect)  # Semi-transparent black
        pygame.draw.rect(self.screen, (100, 100, 100), player_bg_rect, 2)  # Gray border
        
        # Draw player name and status with clear text
        name_color = (255, 255, 0) if player_index == current_player_index else (255, 255, 255)
        name_text = f"{player.name} ({len(player.hand)} cards)"
        
        # Draw name with simple positioning (no shadow for now to fix text issues)
        name_surface = self.font_small.render(name_text, True, name_color)
        name_rect = name_surface.get_rect(center=(player_x, player_y - 50))
        self.screen.blit(name_surface, name_rect)
        
        # Draw player's hand with simple horizontal layout
        if len(player.hand) > 0:
            # Calculate card spacing - ensure cards don't go off screen
            max_cards_visible = min(len(player.hand), 6)  # Show max 6 cards
            card_spacing = min(90, (400 // max_cards_visible))  # Max 400px width
            
            start_x = player_x - (max_cards_visible * card_spacing) // 2
            
            for i, card in enumerate(player.hand[:max_cards_visible]):
                card_x = start_x + i * card_spacing
                card_y = player_y
                
                # Ensure cards stay within screen bounds
                if card_x < 20:
                    card_x = 20
                elif card_x > WINDOW_WIDTH - CARD_WIDTH - 20:
                    card_x = WINDOW_WIDTH - CARD_WIDTH - 20
                
                # For AI players, only show card backs (hidden cards)
                if player.is_ai:
                    # Draw card back instead of actual card
                    self.draw_card_back(card_x, card_y)
                else:
                    # Human player - show actual cards
                    highlight = (selected_card == card)
                    target = (target_player == player and selected_card == card)
                    self.draw_card_image(card, card_x, card_y, highlight, target)
                    
                    # Draw card index for easier selection (simple text, no shadow)
                    index_text = str(i)
                    index_surface = self.font_small.render(index_text, True, (255, 255, 255))
                    index_rect = index_surface.get_rect(center=(card_x + CARD_WIDTH // 2, card_y + CARD_HEIGHT + 15))
                    self.screen.blit(index_surface, index_rect)
                
                # Show overflow indicator if there are more cards
                if i == max_cards_visible - 1 and len(player.hand) > max_cards_visible:
                    overflow_text = f"+{len(player.hand) - max_cards_visible}"
                    overflow_surface = self.font_small.render(overflow_text, True, (255, 255, 255))
                    overflow_rect = overflow_surface.get_rect(center=(card_x + CARD_WIDTH + 20, card_y + CARD_HEIGHT // 2))
                    self.screen.blit(overflow_surface, overflow_rect)
        else:
            # No cards - show empty hand indicator
            empty_text = "No cards"
            empty_surface = self.font_small.render(empty_text, True, (150, 150, 150))
            empty_rect = empty_surface.get_rect(center=(player_x, player_y))
            self.screen.blit(empty_surface, empty_rect)
        
        # Draw mood cards count if any (only for human player or if it's the current player)
        if hasattr(player, 'mood_cards') and player.mood_cards:
            mood_y = player_y + CARD_HEIGHT + 40
            if not player.is_ai or player_index == current_player_index:
                mood_text = f"Moods: {len(player.mood_cards)}"
                mood_surface = self.font_small.render(mood_text, True, (255, 255, 255))
                mood_rect = mood_surface.get_rect(center=(player_x, mood_y))
                self.screen.blit(mood_surface, mood_rect)
        
        # Draw targeting indicator if this player is targeted
        if target_player == player:
            target_text = "🎯 TARGETED"
            target_surface = self.font_small.render(target_text, True, (255, 0, 0))
            target_rect = target_surface.get_rect(center=(player_x, player_y + 80))
            self.screen.blit(target_surface, target_rect)
    
    def draw_card_image(self, card, x, y, highlight=False, target=False):
        """Draw a card using its actual image or fallback to colored rectangle"""
        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        
        # Check for hover effect
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = card_rect.collidepoint(mouse_pos)
        
        # Apply hover effect (slight lift and glow)
        if is_hovered and not highlight:
            y -= 5  # Lift the card slightly
            card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            
            # Draw hover shadow
            shadow_rect = pygame.Rect(x + 2, y + 2, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect)
        
        # Determine card image key
        if hasattr(card, 'mood'):
            image_key = card.mood
        elif hasattr(card, 'card_type'):
            image_key = card.card_type
        else:
            image_key = None
        
        # Draw card image if available
        if image_key and image_key in self.card_images:
            self.screen.blit(self.card_images[image_key], (x, y))
        else:
            # Fallback to colored rectangle
            color = card.color if hasattr(card, 'color') else (100, 100, 100)
            pygame.draw.rect(self.screen, color, card_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), card_rect, 2)
            
            # Draw card text
            if hasattr(card, 'emoji'):
                text = self.font_small.render(card.emoji, True, (0, 0, 0))
            elif hasattr(card, 'description'):
                text = self.font_small.render(card.description, True, (0, 0, 0))
            else:
                text = self.font_small.render(card.name, True, (0, 0, 0))
            
            text_rect = text.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
            self.screen.blit(text, text_rect)
        
        # Draw highlight effects
        if highlight:
            # Glowing border with animation
            glow_intensity = int(255 * (0.5 + 0.5 * abs(math.sin(self.hover_animation * 3))))
            for i in range(3):
                highlight_rect = pygame.Rect(x - i, y - i, CARD_WIDTH + i*2, CARD_HEIGHT + i*2)
                pygame.draw.rect(self.screen, (255, 255, 0, glow_intensity), highlight_rect, 2)
        
        if target:
            # Target indicator with pulsing effect
            pulse_intensity = int(255 * (0.3 + 0.7 * abs(math.sin(self.hover_animation * 4))))
            target_rect = pygame.Rect(x - 5, y - 5, CARD_WIDTH + 10, CARD_HEIGHT + 10)
            pygame.draw.rect(self.screen, (255, 0, 0, pulse_intensity), target_rect, 3)
        
        # Draw hover tooltip
        if is_hovered:
            self.draw_card_tooltip(card, x, y)
    
    def draw_card_tooltip(self, card, x, y):
        """Draw a tooltip showing card details when hovering"""
        # Determine tooltip text
        if hasattr(card, 'mood'):
            tooltip_text = f"Mood: {card.mood.capitalize()}"
            tooltip_color = (255, 255, 255)
        elif hasattr(card, 'card_type'):
            tooltip_text = f"Swing: {card.description}"
            tooltip_color = (255, 255, 0)
        else:
            tooltip_text = card.name
            tooltip_color = (255, 255, 255)
        
        # Render tooltip
        tooltip_surface = self.font_tiny.render(tooltip_text, True, (0, 0, 0))
        tooltip_bg = pygame.Surface((tooltip_surface.get_width() + 10, tooltip_surface.get_height() + 6))
        tooltip_bg.fill((255, 255, 255))
        tooltip_bg.set_alpha(230)
        
        # Position tooltip above the card
        tooltip_x = x + CARD_WIDTH // 2 - tooltip_bg.get_width() // 2
        tooltip_y = y - tooltip_bg.get_height() - 10
        
        # Draw tooltip background and text
        self.screen.blit(tooltip_bg, (tooltip_x, tooltip_y))
        self.screen.blit(tooltip_surface, (tooltip_x + 5, tooltip_y + 3))
        
        # Draw tooltip border
        pygame.draw.rect(self.screen, (100, 100, 100), tooltip_bg.get_rect(topleft=(tooltip_x, tooltip_y)), 1)
    
    def draw_game_controls(self, turn_phase):
        """Draw game controls with simple text rendering (no shadow)"""
        # Show different controls based on turn phase
        if turn_phase == 'draw':
            controls = [
                "🎯 Click the deck to draw a card",
                "🔄 Press SPACE to advance to play phase",
                "⚙️ Press S for settings"
            ]
        elif turn_phase == 'play':
            controls = [
                "🎴 Click a card to select it",
                "👤 Click a player to target them (for swing cards)",
                "🔄 Press SPACE to advance to discard phase",
                "⚙️ Press S for settings"
            ]
        elif turn_phase == 'discard':
            controls = [
                "🗑️ Click a card to select for discard",
                "🔄 Press SPACE to end turn",
                "⚙️ Press S for settings"
            ]
        else:
            controls = [
                "🎯 Click a card to select it",
                "👤 Click a player to target them",
                "🔄 Press SPACE to advance turn",
                "🗑️ Press D to discard selected card",
                "⚙️ Press S for settings"
            ]
        
        # Position controls at the bottom of the screen, but above the bottom player
        start_y = WINDOW_HEIGHT - 300  # Moved up from 250 to avoid overlap with bottom player
        
        for i, control in enumerate(controls):
            y_pos = start_y + i * 25
            control_surface = self.font_small.render(control, True, (255, 255, 255))
            control_rect = control_surface.get_rect(center=(WINDOW_WIDTH // 2, y_pos))
            self.screen.blit(control_surface, control_rect)
    
    def update_animations(self):
        """Update animation variables and particle effects"""
        self.hover_animation += 0.05
        self.card_flip_animation += 0.1
        
        # Update particle effects
        for particle in self.particle_effects[:]:
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particle_effects.remove(particle)
    
    def get_card_rect(self, card_index, player, player_index):
        """Get the rectangle for a specific card in a player's hand"""
        if len(player.hand) > 0:
            start_x = 200
            spacing = min((WINDOW_WIDTH - 400) // len(player.hand), 100)
        else:
            start_x = 200
            spacing = 100
        
        player_y = 150 + player_index * 120
        card_x = start_x + card_index * spacing
        card_y = player_y
        
        return pygame.Rect(card_x, card_y, CARD_WIDTH, CARD_HEIGHT)
    
    def get_player_rect(self, player_index):
        """Get the rectangle for a player area"""
        player_y = 150 + player_index * 120
        return pygame.Rect(50, player_y - 30, WINDOW_WIDTH - 100, 120)
    
    def show_settings_menu(self):
        """Show the settings menu"""
        self.settings_menu.visible = True
    
    def hide_settings_menu(self):
        """Hide the settings menu"""
        self.settings_menu.visible = False
    
    def is_settings_visible(self):
        """Check if settings menu is visible"""
        return self.settings_menu.visible
    
    def handle_settings_input(self, event):
        """Handle input for settings menu"""
        return self.settings_menu.handle_input(event)
    
    def render_settings(self):
        """Render the settings menu"""
        self.settings_menu.render()
    
    def show_instructions(self):
        """Show the game instructions screen"""
        self.instructions_visible = True
    
    def hide_instructions(self):
        """Hide the game instructions screen"""
        self.instructions_visible = False
    
    def is_instructions_visible(self):
        """Check if instructions screen is visible"""
        return getattr(self, 'instructions_visible', False)
    
    def render_instructions(self):
        """Render the game instructions screen"""
        if self.is_instructions_visible():
            self.draw_game_instructions()

    def draw_card_back(self, x, y):
        """Draw a card back (hidden card) for AI players"""
        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        
        # Draw card background
        pygame.draw.rect(self.screen, (50, 50, 100), card_rect)
        pygame.draw.rect(self.screen, (100, 100, 150), card_rect, 2)
        
        # Draw card back pattern
        pattern_rect = pygame.Rect(x + 5, y + 5, CARD_WIDTH - 10, CARD_HEIGHT - 10)
        pygame.draw.rect(self.screen, (30, 30, 80), pattern_rect)
        
        # Draw some decorative elements
        center_x = x + CARD_WIDTH // 2
        center_y = y + CARD_HEIGHT // 2
        
        # Draw a simple pattern
        for i in range(3):
            for j in range(2):
                dot_x = center_x - 20 + i * 20
                dot_y = center_y - 15 + j * 30
                pygame.draw.circle(self.screen, (100, 100, 150), (dot_x, dot_y), 3)
    
    def draw_game_over_screen(self, winner):
        """Draw the game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Game over box
        box_width = 500
        box_height = 300
        box_x = (WINDOW_WIDTH - box_width) // 2
        box_y = (WINDOW_HEIGHT - box_height) // 2
        
        # Draw box
        game_over_box = pygame.Surface((box_width, box_height))
        game_over_box.fill((50, 50, 100))
        pygame.draw.rect(game_over_box, (100, 100, 150), game_over_box.get_rect(), 3)
        pygame.draw.rect(game_over_box, (30, 30, 80), (5, 5, box_width - 10, box_height - 10), 2)
        self.screen.blit(game_over_box, (box_x, box_y))
        
        # Game over title
        title_font = pygame.font.Font(None, 48)
        title_surface = title_font.render("🎉 GAME OVER! 🎉", True, (255, 255, 0))
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, box_y + 60))
        self.screen.blit(title_surface, title_rect)
        
        # Winner announcement
        if winner:
            winner_font = pygame.font.Font(None, 36)
            winner_text = f"🏆 {winner.name} wins! 🏆"
            winner_surface = winner_font.render(winner_text, True, (100, 255, 100))
            winner_rect = winner_surface.get_rect(center=(WINDOW_WIDTH // 2, box_y + 120))
            self.screen.blit(winner_surface, winner_rect)
            
            # Win condition
            win_font = pygame.font.Font(None, 24)
            win_text = "They collected all 5 moods and FLIPPED OUT!"
            win_surface = win_font.render(win_text, True, (255, 255, 255))
            win_rect = win_surface.get_rect(center=(WINDOW_WIDTH // 2, box_y + 160))
            self.screen.blit(win_surface, win_rect)
        
        # Instructions
        instruction_font = pygame.font.Font(None, 28)
        instructions = [
            "Press SPACE to play again",
            "Press ESC to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            instruction_surface = instruction_font.render(instruction, True, (200, 200, 200))
            instruction_rect = instruction_surface.get_rect(center=(WINDOW_WIDTH // 2, box_y + 220 + i * 30))
            self.screen.blit(instruction_surface, instruction_rect)

    def is_tutorial_button_clicked(self, pos):
        """Check if tutorial button was clicked"""
        # Tutorial button area (around the tutorial text)
        tutorial_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT * 2 // 3, 300, 40)
        return tutorial_rect.collidepoint(pos)
    
    def is_deck_clicked(self, pos):
        """Check if deck was clicked"""
        deck_rect = pygame.Rect(WINDOW_WIDTH // 2 - 40, WINDOW_HEIGHT // 2 - CARD_HEIGHT // 2,
                               CARD_WIDTH, CARD_HEIGHT)
        return deck_rect.collidepoint(pos)
    
    def set_players(self, players):
        """Set the players reference for UI interactions"""
        self.players = players
    
    def get_clicked_card(self, pos, player):
        """Get the card that was clicked in a player's hand"""
        if not player.hand:
            return None
        
        # Calculate card positions for the player
        if player == self.players[0] if self.players else None:  # Human player (bottom)
            hand_start_x = 50
            hand_y = WINDOW_HEIGHT - CARD_HEIGHT - 50
            for i, card in enumerate(player.hand):
                card_x = hand_start_x + i * (CARD_WIDTH + 10)
                card_rect = pygame.Rect(card_x, hand_y, CARD_WIDTH, CARD_HEIGHT)
                if card_rect.collidepoint(pos):
                    return card
        
        return None
    
    def show_instructions(self):
        """Show instructions overlay"""
        self.instructions_visible = True
    
    def hide_instructions(self):
        """Hide instructions overlay"""
        self.instructions_visible = False
    
    def is_instructions_visible(self):
        """Check if instructions are visible"""
        return self.instructions_visible
    
    def show_settings(self):
        """Show settings overlay"""
        self.settings_visible = True
    
    def hide_settings(self):
        """Hide settings overlay"""
        self.settings_visible = False
    
    def is_settings_visible(self):
        """Check if settings are visible"""
        return self.settings_visible
    
    def render_instructions(self):
        """Render instructions overlay"""
        self.draw_game_instructions()
    
    def render_settings(self):
        """Render settings overlay"""
        # Simple settings display for now
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Settings box
        box_width = 400
        box_height = 300
        box_x = (WINDOW_WIDTH - box_width) // 2
        box_y = (WINDOW_HEIGHT - box_height) // 2
        
        settings_box = pygame.Surface((box_width, box_height))
        settings_box.fill((50, 50, 100))
        pygame.draw.rect(settings_box, (100, 100, 150), settings_box.get_rect(), 3)
        self.screen.blit(settings_box, (box_x, box_y))
        
        # Settings title
        title_font = pygame.font.Font(None, 36)
        title_surface = title_font.render("⚙️ Settings", True, (255, 255, 0))
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, box_y + 40))
        self.screen.blit(title_surface, title_rect)
        
        # Settings content
        settings_font = pygame.font.Font(None, 24)
        settings_text = [
            "Settings menu coming soon!",
            "",
            "Press ESC to return"
        ]
        
        for i, text in enumerate(settings_text):
            text_surface = settings_font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, box_y + 120 + i * 30))
            self.screen.blit(text_surface, text_rect)
    
    def draw_tutorial_screen(self, players, state, deck, discard_pile, tutorial_steps, drag_manager):
        """Draw the tutorial screen with new architecture"""
        # Draw the game screen first
        self.draw_game_screen(players, state, deck, discard_pile, drag_manager)
        
        # Draw tutorial overlay
        self.draw_tutorial_overlay(state.tutorial_step, tutorial_steps)
        
        # Draw dragging card if in dragging step
        if state.tutorial_step == 3 and drag_manager.dragging:
            mouse_pos = pygame.mouse.get_pos()
            card_x = mouse_pos[0] - CARD_WIDTH // 2
            card_y = mouse_pos[1] - CARD_HEIGHT // 2
            self.draw_card_image(drag_manager.dragged_card, card_x, card_y, highlight=True)
    
    def draw_game_screen(self, players, state, deck, discard_pile, drag_manager):
        """Draw the main game screen with new architecture"""
        # Draw background
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_background_pattern()
        
        # Draw table interface
        self.draw_table_interface()
        
        # Draw players
        for i, player in enumerate(players):
            self.draw_player(player, i, state.current_player_index)
        
        # Draw deck
        if deck and deck.cards:
            deck_x = WINDOW_WIDTH // 2 - 40
            deck_y = WINDOW_HEIGHT // 2 - CARD_HEIGHT // 2
            self.draw_deck(deck_x, deck_y, len(deck.cards))
        
        # Draw discard pile
        if discard_pile:
            discard_x = WINDOW_WIDTH // 2 + 40
            discard_y = WINDOW_HEIGHT // 2 - CARD_HEIGHT // 2
            self.draw_discard_pile(discard_x, discard_y, discard_pile[-1], len(discard_pile))
        
        # Draw game message
        if state.game_message:
            self.draw_game_message(state.game_message)
        
        # Draw turn phase indicator
        self.draw_turn_phase_indicator(state.turn_phase)
        
        # Draw game controls
        self.draw_game_controls(state.turn_phase)
        
        # Draw dragging card
        if drag_manager.dragging and drag_manager.dragged_card:
            mouse_pos = pygame.mouse.get_pos()
            card_x = mouse_pos[0] - CARD_WIDTH // 2
            card_y = mouse_pos[1] - CARD_HEIGHT // 2
            self.draw_card_image(drag_manager.dragged_card, card_x, card_y, highlight=True)
    
    def draw_turn_phase_indicator(self, turn_phase):
        """Draw the current turn phase indicator"""
        phase_text = f"Phase: {turn_phase.title()}"
        phase_font = pygame.font.Font(None, 28)
        phase_surface = phase_font.render(phase_text, True, (255, 255, 0))
        phase_rect = phase_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        self.screen.blit(phase_surface, phase_rect)
    
    def draw_deck(self, x, y, card_count):
        """Draw the deck with multiple card effect"""
        # Draw deck with multiple card effect
        for i in range(min(3, card_count)):
            offset = i * 2
            card_rect = pygame.Rect(x + offset, y + offset, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(self.screen, CARD_COLOR, card_rect)
            pygame.draw.rect(self.screen, CARD_BORDER_COLOR, card_rect, 2)
        
        # Deck count
        count_text = f"Deck: {card_count}"
        count_surface = self.font_small.render(count_text, True, (255, 255, 255))
        count_rect = count_surface.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT + 20))
        self.screen.blit(count_surface, count_rect)
    
    def draw_discard_pile(self, x, y, top_card, discard_count=0):
        """Draw the discard pile with the top card visible"""
        if top_card:
            # Draw top card of discard pile
            self.draw_card_image(top_card, x, y, highlight=False)
        else:
            # Empty discard pile
            discard_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(self.screen, (100, 100, 100), discard_rect, 2)
            pygame.draw.rect(self.screen, (50, 50, 50), discard_rect)
        
        # Discard count
        discard_text = f"Discard: {discard_count}"
        discard_surface = self.font_small.render(discard_text, True, (255, 255, 255))
        discard_rect = discard_surface.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT + 20))
        self.screen.blit(discard_surface, discard_rect)
    
    def draw_game_message(self, message):
        """Draw a game message at the top of the screen"""
        if not message:
            return
        
        # Message background
        message_font = pygame.font.Font(None, 32)
        message_surface = message_font.render(message, True, (255, 255, 255))
        message_bg = pygame.Surface((message_surface.get_width() + 20, message_surface.get_height() + 10))
        message_bg.fill((50, 50, 100))
        message_bg.set_alpha(200)
        
        # Position message at top center
        message_x = (WINDOW_WIDTH - message_bg.get_width()) // 2
        message_y = 20
        
        # Draw message background and text
        self.screen.blit(message_bg, (message_x, message_y))
        self.screen.blit(message_surface, (message_x + 10, message_y + 5))
        
        # Draw message border
        pygame.draw.rect(self.screen, (100, 100, 150), message_bg.get_rect(topleft=(message_x, message_y)), 2)
