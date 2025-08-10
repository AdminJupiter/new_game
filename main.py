import pygame
import sys
import random
import time
from game_logic import Card, Deck, Player
from ui_manager import UIManager
from constants import *

class GameState:
    """Centralized game state management"""
    def __init__(self):
        self.phase = 'title'  # title, tutorial, playing, game_over
        self.turn_phase = 'draw'  # draw, play, discard
        self.current_player_index = 0
        self.selected_card = None
        self.target_player = None
        self.dragging_card = None
        self.drag_start_pos = None
        self.drag_offset = (0, 0)
        self.game_message = ""
        self.message_timer = 0
        self.winner = None
        
        # Tutorial state
        self.tutorial_mode = False
        self.tutorial_step = 0
        self.tutorial_completed = False

class DragManager:
    """Handles all card dragging operations"""
    def __init__(self):
        self.dragging = False
        self.dragged_card = None
        self.drag_start_pos = None
        self.drag_offset = (0, 0)
        self.original_pos = None
        self.drop_targets = []
    
    def start_drag(self, card, start_pos, original_pos):
        """Start dragging a card"""
        self.dragging = True
        self.dragged_card = card
        self.drag_start_pos = start_pos
        self.original_pos = original_pos
        self.drag_offset = (0, 0)
        print(f"🎴 Started dragging {card.name}")
    
    def update_drag(self, current_pos):
        """Update drag position"""
        if self.dragging and self.drag_start_pos:
            self.drag_offset = (current_pos[0] - self.drag_start_pos[0],
                               current_pos[1] - self.drag_start_pos[1])
    
    def end_drag(self, end_pos):
        """End dragging and return drop target info"""
        if not self.dragging:
            return None
        
        drop_info = self.find_drop_target(end_pos)
        self.dragging = False
        self.dragged_card = None
        self.drag_start_pos = None
        self.drag_offset = (0, 0)
        self.original_pos = None
        
        print(f"🎴 Ended drag at {end_pos}, target: {drop_info}")
        return drop_info
    
    def find_drop_target(self, pos):
        """Find what the card was dropped on"""
        # This will be implemented to detect opponents, discard pile, etc.
        return {'type': 'none', 'target': None, 'position': pos}

class FlipOutGame:
    """Main game class with robust architecture"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flip Out! - The Mood Swing Card Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize core systems
        self.state = GameState()
        self.drag_manager = DragManager()
        self.ui_manager = UIManager(self.screen)
        
        # Game objects
        self.players = []
        self.deck = None
        self.discard_pile = []
        
        # Initialize game
        self.setup_game()
        
        # Tutorial steps
        self.setup_tutorial()
    
    def setup_game(self):
        """Initialize all game components"""
        self.setup_players()
        self.setup_deck()
        self.deal_initial_cards()
        print("✓ Game setup complete")
    
    def setup_players(self):
        """Create players"""
        self.players = [
            Player("You", is_ai=False),
            Player("AI Player 1", is_ai=True),
            Player("AI Player 2", is_ai=True),
            Player("AI Player 3", is_ai=True)
        ]
    
    def setup_deck(self):
        """Create and shuffle the deck"""
        self.deck = Deck()
        self.deck.shuffle()
        print(f"✓ Created deck with {len(self.deck.cards)} cards")
    
    def deal_initial_cards(self):
        """Deal initial cards to all players"""
        for player in self.players:
            for _ in range(5):
                if self.deck.cards:
                    card = self.deck.draw()
                    player.add_card_to_hand(card)
        print("✓ Dealt initial cards to all players")
    
    def setup_tutorial(self):
        """Setup tutorial system"""
        self.tutorial_steps = [
            {
                'title': 'Welcome to Flip Out!',
                'description': 'Let\'s learn how to play step by step!',
                'highlight': None,
                'action': 'Click anywhere to continue'
            },
            {
                'title': 'Drawing Cards',
                'description': 'Click on the deck to draw a card',
                'highlight': 'deck',
                'action': 'Click the deck to draw a card'
            },
            {
                'title': 'Selecting Cards',
                'description': 'Click on a card in your hand to select it',
                'highlight': 'player_hand',
                'action': 'Click on one of your cards'
            },
            {
                'title': 'Dragging Cards',
                'description': 'Click and drag a card from your hand',
                'highlight': 'player_hand',
                'action': 'Click and drag a card, then release'
            },
            {
                'title': 'Playing Cards',
                'description': 'Drag cards to opponents or discard pile',
                'highlight': 'play_area',
                'action': 'Drag a card to an opponent or discard pile'
            },
            {
                'title': 'You\'re Ready!',
                'description': 'You now know how to play!',
                'highlight': None,
                'action': 'Click to start playing!'
            }
        ]
    
    def handle_events(self):
        """Main event handling system"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            # Handle events based on game phase
            if self.state.phase == 'title':
                self.handle_title_events(event)
            elif self.state.phase == 'tutorial':
                self.handle_tutorial_events(event)
            elif self.state.phase == 'playing':
                self.handle_game_events(event)
            elif self.state.phase == 'game_over':
                self.handle_game_over_events(event)
    
    def handle_title_events(self, event):
        """Handle title screen events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.start_tutorial()
            elif event.key == pygame.K_i:
                self.ui_manager.show_instructions()
            elif event.key == pygame.K_s:
                self.ui_manager.show_settings()
            elif event.key == pygame.K_ESCAPE:
                self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if tutorial button was clicked
            if self.ui_manager.is_tutorial_button_clicked(event.pos):
                self.start_tutorial()
    
    def handle_tutorial_events(self, event):
        """Handle tutorial events with proper dragging"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_tutorial_click(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_tutorial_release(event)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_tutorial_motion(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.start_game()
    
    def handle_tutorial_click(self, event):
        """Handle mouse clicks during tutorial"""
        current_step = self.tutorial_steps[self.state.tutorial_step]
        
        if self.state.tutorial_step == 1:  # Drawing cards
            if self.ui_manager.is_deck_clicked(event.pos):
                self.tutorial_draw_card()
        elif self.state.tutorial_step == 2:  # Selecting cards
            card = self.ui_manager.get_clicked_card(event.pos, self.players[0])
            if card:
                self.state.selected_card = card
                self.next_tutorial_step()
        elif self.state.tutorial_step == 3:  # Dragging cards
            card = self.ui_manager.get_clicked_card(event.pos, self.players[0])
            if card:
                # Start dragging
                self.drag_manager.start_drag(card, event.pos, event.pos)
                self.state.dragging_card = card
        elif self.state.tutorial_step == 4:  # Playing cards
            if self.drag_manager.dragging:
                # Continue dragging
                pass
        elif self.state.tutorial_step == 5:  # Final step
            self.start_game()
    
    def handle_tutorial_release(self, event):
        """Handle mouse release during tutorial"""
        if self.drag_manager.dragging:
            drop_info = self.drag_manager.end_drag(event.pos)
            if self.state.tutorial_step == 3:  # Dragging step
                self.next_tutorial_step()
            elif self.state.tutorial_step == 4:  # Playing step
                if drop_info['type'] in ['opponent', 'discard']:
                    self.next_tutorial_step()
    
    def handle_tutorial_motion(self, event):
        """Handle mouse motion during tutorial"""
        if self.drag_manager.dragging:
            self.drag_manager.update_drag(event.pos)
    
    def handle_game_events(self, event):
        """Handle events during actual gameplay"""
        if event.type == pygame.KEYDOWN:
            self.handle_game_keydown(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_game_click(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_game_release(event)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_game_motion(event)
    
    def handle_game_keydown(self, event):
        """Handle keyboard input during gameplay"""
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_SPACE:
            self.advance_turn_phase()
        elif event.key == pygame.K_r:
            self.reset_game()
    
    def handle_game_click(self, event):
        """Handle mouse clicks during gameplay"""
        if self.state.turn_phase == 'draw':
            if self.ui_manager.is_deck_clicked(event.pos):
                self.draw_card()
        elif self.state.turn_phase == 'play':
            # Check if clicked on a card in hand
            card = self.ui_manager.get_clicked_card(event.pos, self.players[0])
            if card:
                self.state.selected_card = card
                # Start dragging for playing
                self.drag_manager.start_drag(card, event.pos, event.pos)
        elif self.state.turn_phase == 'discard':
            # Check if clicked on a card in hand
            card = self.ui_manager.get_clicked_card(event.pos, self.players[0])
            if card:
                self.discard_card(card)
    
    def handle_game_release(self, event):
        """Handle mouse release during gameplay"""
        if self.drag_manager.dragging:
            drop_info = self.drag_manager.end_drag(event.pos)
            if self.state.turn_phase == 'play' and self.state.selected_card:
                self.handle_card_play(drop_info)
    
    def handle_game_motion(self, event):
        """Handle mouse motion during gameplay"""
        if self.drag_manager.dragging:
            self.drag_manager.update_drag(event.pos)
    
    def handle_card_play(self, drop_info):
        """Handle playing a card based on drop target"""
        if drop_info['type'] == 'opponent':
            self.play_card_on_opponent(self.state.selected_card, drop_info['target'])
        elif drop_info['type'] == 'discard':
            self.discard_card(self.state.selected_card)
        
        self.state.selected_card = None
    
    def start_tutorial(self):
        """Start the tutorial mode"""
        self.state.phase = 'tutorial'
        self.state.tutorial_step = 0
        self.state.tutorial_mode = True
        print("🎓 Tutorial started!")
    
    def next_tutorial_step(self):
        """Advance to next tutorial step"""
        self.state.tutorial_step += 1
        if self.state.tutorial_step >= len(self.tutorial_steps):
            self.state.tutorial_completed = True
            print("🎓 Tutorial completed!")
        else:
            current_step = self.tutorial_steps[self.state.tutorial_step]
            print(f"🎓 Tutorial Step {self.state.tutorial_step + 1}: {current_step['title']}")
    
    def start_game(self):
        """Start the actual game"""
        self.state.phase = 'playing'
        self.state.tutorial_mode = False
        self.state.current_player_index = 0
        self.state.turn_phase = 'draw'
        print("🎮 Game started!")
    
    def draw_card(self):
        """Draw a card from the deck"""
        if self.deck.cards:
            card = self.deck.draw()
            self.players[0].add_card_to_hand(card)
            self.show_message(f"🎴 Drew: {card.name}")
            self.advance_turn_phase()
        else:
            self.show_message("⚠️ No cards left in deck!")
    
    def advance_turn_phase(self):
        """Move to next turn phase"""
        if self.state.turn_phase == 'draw':
            self.state.turn_phase = 'play'
            self.show_message("🎯 Your turn: Play a card (optional)")
        elif self.state.turn_phase == 'play':
            self.state.turn_phase = 'discard'
            self.show_message("🗑️ Your turn: Discard a card (optional)")
        elif self.state.turn_phase == 'discard':
            self.end_turn()
    
    def end_turn(self):
        """End current player's turn"""
        self.state.current_player_index = (self.state.current_player_index + 1) % len(self.players)
        self.state.turn_phase = 'draw'
        self.state.selected_card = None
        
        if self.players[self.state.current_player_index].is_ai:
            self.handle_ai_turn()
        else:
            self.show_message("🎴 Your turn! Click deck to draw")
    
    def handle_ai_turn(self):
        """Handle AI player turns"""
        ai_player = self.players[self.state.current_player_index]
        self.show_message(f"🤖 {ai_player.name}'s turn")
        
        # Simple AI: draw, play random card, discard random card
        time.sleep(1)
        if self.deck.cards:
            card = self.deck.draw()
            ai_player.add_card_to_hand(card)
        
        time.sleep(0.5)
        if ai_player.hand:
            # Play a random card
            card = random.choice(ai_player.hand)
            ai_player.hand.remove(card)
            self.discard_pile.append(card)
        
        time.sleep(0.5)
        if ai_player.hand:
            # Discard a random card
            card = random.choice(ai_player.hand)
            ai_player.hand.remove(card)
            self.discard_pile.append(card)
        
        self.end_turn()
    
    def play_card_on_opponent(self, card, target_player):
        """Play a card on an opponent"""
        if card.card_type == 'mood_swing':
            self.handle_mood_swing_card(card, target_player)
        else:
            # Regular mood card
            target_player.add_mood_card(card)
            self.players[0].hand.remove(card)
            self.show_message(f"🎴 Played {card.name} on {target_player.name}")
        
        self.advance_turn_phase()
    
    def handle_mood_swing_card(self, card, target_player):
        """Handle mood swing card effects"""
        if card.name == 'steal_mood':
            if target_player.mood_cards:
                stolen_card = random.choice(target_player.mood_cards)
                target_player.mood_cards.remove(stolen_card)
                self.players[0].add_mood_card(stolen_card)
                self.show_message(f"🎴 Stole {stolen_card.name} from {target_player.name}")
        
        # Add card to discard pile
        self.discard_pile.append(card)
        self.players[0].hand.remove(card)
        self.show_message(f"🎴 Used {card.name} on {target_player.name}")
    
    def discard_card(self, card):
        """Discard a card"""
        self.players[0].hand.remove(card)
        self.discard_pile.append(card)
        self.show_message(f"🗑️ Discarded: {card.name}")
        self.advance_turn_phase()
    
    def show_message(self, message):
        """Show a game message"""
        self.state.game_message = message
        self.state.message_timer = 120  # 2 seconds at 60 FPS
        print(f"💬 {message}")
    
    def update_message_timer(self):
        """Update message display timer"""
        if self.state.message_timer > 0:
            self.state.message_timer -= 1
            if self.state.message_timer == 0:
                self.state.game_message = ""
    
    def check_win_condition(self):
        """Check if any player has won"""
        for player in self.players:
            if len(player.mood_cards) >= 5:  # Need one of each mood
                return player
        return None
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.state = GameState()
        self.drag_manager = DragManager()
        self.setup_game()
        print("🔄 Game reset!")
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update game state
            if self.state.phase == 'playing':
                self.update_message_timer()
                
                # Check win condition
                winner = self.check_win_condition()
                if winner:
                    self.state.winner = winner
                    self.state.phase = 'game_over'
            
            # Render appropriate screen
            if self.state.phase == 'title':
                self.ui_manager.draw_title_screen()
            elif self.state.phase == 'tutorial':
                self.ui_manager.draw_tutorial_screen(
                    self.players, self.state, self.deck, self.discard_pile,
                    self.tutorial_steps, self.drag_manager
                )
            elif self.state.phase == 'playing':
                self.ui_manager.draw_game_screen(
                    self.players, self.state, self.deck, self.discard_pile,
                    self.drag_manager
                )
            elif self.state.phase == 'game_over':
                self.ui_manager.draw_game_over_screen(self.state.winner)
            
            # Render overlays
            if self.ui_manager.is_instructions_visible():
                self.ui_manager.render_instructions()
            if self.ui_manager.is_settings_visible():
                self.ui_manager.render_settings()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = FlipOutGame()
    game.run()
