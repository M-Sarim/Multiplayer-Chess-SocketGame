"""
Chess Game Lobby System
This file handles the lobby menu, game creation, and joining games
"""
import pygame
import sys
import os
import json
import time
import uuid
import math
from ..utils.chess_assets import (
    draw_chess_button,
    draw_chess_panel,
    draw_chess_input,
    draw_chess_game_item,
    draw_chess_icon,
    draw_chess_board_pattern
)

# Initialize pygame
pygame.init()

# Set window size
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Chess Game Lobby")
# Create a chess icon with our new color scheme
icon = pygame.Surface((32, 32), pygame.SRCALPHA)
# We'll still use the king icon but with our new color scheme
# The draw_chess_icon function will use the updated colors
draw_chess_icon(icon, "king", "white", (16, 16), 30)
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
FPS = 60

# Colors - Classic black-and-white chess theme
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (255, 255, 255)  # White for light squares
DARK_SQUARE = (0, 0, 0)         # Black for dark squares
HIGHLIGHT = (150, 150, 150, 150)  # Gray highlight
GRAY = (80, 80, 80)
DARK_GRAY = (40, 40, 40)        # Dark gray
LIGHT_GRAY = (220, 220, 220)
RED = (220, 60, 60)             # Softer red
GREEN = (60, 200, 60)           # Softer green
BLUE = (60, 120, 255)           # Brighter blue
GOLD = (150, 150, 150)          # Changed to gray for classic theme

# Updated colors for a classic black-and-white chess theme
BACKGROUND_COLOR = (50, 50, 50)  # Dark gray background
BUTTON_COLOR = (30, 30, 30)      # Dark button color
BUTTON_HOVER_COLOR = (70, 70, 70)  # Lighter gray for hover
PANEL_COLOR = (40, 40, 40)       # Slightly lighter panel background
TITLE_COLOR = (200, 200, 200)    # Light gray for titles
ACCENT_COLOR = (150, 150, 150)   # Gray accent

# Fonts - Try to use nicer fonts if available
try:
    title_font = pygame.font.Font(None, 64)  # Default font, larger size
    header_font = pygame.font.Font(None, 48)
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 24)
except:
    # Fallback to SysFont if custom font fails
    title_font = pygame.font.SysFont('Arial', 48, bold=True)
    header_font = pygame.font.SysFont('Arial', 32, bold=True)
    font = pygame.font.SysFont('Arial', 24)
    small_font = pygame.font.SysFont('Arial', 18)

# No video background - using static background instead

# File for storing game list
GAMES_LIST_FILE = "../../data/chess_games_list.json"

# Enhanced Button class with beautiful animations and effects
class Button:
    def __init__(self, x, y, width, height, text, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, text_color=WHITE, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.original_rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action
        self.is_hovered = False
        self.animation_state = 0  # For hover animation
        self.pulse_direction = 1  # For pulsing effect
        self.hover_scale = 1.0  # Scale factor for hover effect
        self.glow_intensity = 0  # Glow effect intensity
        self.click_animation = 0  # Click animation state
        self.shadow_offset = 3  # Shadow depth

    def draw(self, screen):
        # Calculate animated properties
        current_time = pygame.time.get_ticks() / 1000.0

        # Smooth hover scaling animation
        target_scale = 1.05 if self.is_hovered else 1.0
        self.hover_scale += (target_scale - self.hover_scale) * 0.15

        # Glow intensity animation
        target_glow = 0.8 if self.is_hovered else 0.0
        self.glow_intensity += (target_glow - self.glow_intensity) * 0.1

        # Calculate scaled rect
        scale_offset = int((self.original_rect.width * (self.hover_scale - 1)) / 2)
        scaled_rect = pygame.Rect(
            self.original_rect.x - scale_offset,
            self.original_rect.y - scale_offset,
            int(self.original_rect.width * self.hover_scale),
            int(self.original_rect.height * self.hover_scale)
        )
        self.rect = scaled_rect

        # Draw glow effect
        if self.glow_intensity > 0:
            glow_surface = pygame.Surface((scaled_rect.width + 20, scaled_rect.height + 20), pygame.SRCALPHA)
            glow_color = (*self.hover_color, int(30 * self.glow_intensity))
            for i in range(5):
                glow_rect = pygame.Rect(10-i*2, 10-i*2, scaled_rect.width + i*4, scaled_rect.height + i*4)
                pygame.draw.rect(glow_surface, glow_color, glow_rect, border_radius=8)
            screen.blit(glow_surface, (scaled_rect.x - 10, scaled_rect.y - 10))

        # Draw shadow with depth
        shadow_rect = pygame.Rect(
            scaled_rect.x + self.shadow_offset,
            scaled_rect.y + self.shadow_offset,
            scaled_rect.width,
            scaled_rect.height
        )
        shadow_surface = pygame.Surface((scaled_rect.width, scaled_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 80), (0, 0, scaled_rect.width, scaled_rect.height), border_radius=8)
        screen.blit(shadow_surface, shadow_rect)

        # Draw gradient background
        color = self.hover_color if self.is_hovered else self.color
        gradient_surface = pygame.Surface((scaled_rect.width, scaled_rect.height), pygame.SRCALPHA)

        # Create vertical gradient
        for y in range(scaled_rect.height):
            gradient_factor = y / scaled_rect.height
            r = int(color[0] * (1 + gradient_factor * 0.3))
            g = int(color[1] * (1 + gradient_factor * 0.3))
            b = int(color[2] * (1 + gradient_factor * 0.3))
            gradient_color = (min(255, r), min(255, g), min(255, b))
            pygame.draw.line(gradient_surface, gradient_color, (0, y), (scaled_rect.width, y))

        # Apply gradient with rounded corners
        pygame.draw.rect(screen, color, scaled_rect, border_radius=8)
        screen.blit(gradient_surface, scaled_rect)

        # Draw elegant border with subtle animation
        border_color = (100 + int(50 * self.glow_intensity), 100 + int(50 * self.glow_intensity), 100 + int(50 * self.glow_intensity))
        pygame.draw.rect(screen, border_color, scaled_rect, 2, border_radius=8)

        # Draw inner highlight
        highlight_rect = pygame.Rect(scaled_rect.x + 2, scaled_rect.y + 2, scaled_rect.width - 4, scaled_rect.height - 4)
        pygame.draw.rect(screen, (255, 255, 255, 20), highlight_rect, 1, border_radius=6)

        # Draw text with shadow and scaling
        text_font = pygame.font.SysFont('Arial', int(22 * self.hover_scale), bold=True)

        # Text shadow
        text_shadow = text_font.render(self.text, True, (0, 0, 0))
        shadow_rect = text_shadow.get_rect(center=(scaled_rect.centerx + 1, scaled_rect.centery + 1))
        screen.blit(text_shadow, shadow_rect)

        # Main text with subtle glow
        text_color = self.text_color
        if self.is_hovered:
            text_color = (min(255, text_color[0] + 30), min(255, text_color[1] + 30), min(255, text_color[2] + 30))

        text_surf = text_font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        screen.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        # Update hover state
        prev_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Smooth animation updates
        if prev_hovered != self.is_hovered:
            self.animation_state = 0

    def check_click(self, mouse_pos):
        # Check if button was clicked with click animation
        if self.rect.collidepoint(mouse_pos) and self.action:
            self.click_animation = 1.0  # Start click animation
            return self.action
        return None

class InputBox:
    def __init__(self, x, y, width, height, text='', placeholder='Enter text...'):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = LIGHT_GRAY
        self.color_active = BLUE
        self.color = self.color_inactive
        self.text = text
        self.placeholder = placeholder
        self.active = False
        self.rendered_text = font.render(text, True, BLACK)
        self.cursor_visible = True
        self.cursor_timer = 0
        self.focus_animation = 0.0  # Focus animation state
        self.glow_intensity = 0.0  # Glow effect for focus
        self.typing_animation = 0.0  # Animation for typing effect

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked
            was_active = self.active
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive

            # Start focus animation
            if self.active and not was_active:
                self.focus_animation = 0.0

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.typing_animation = 1.0  # Start typing animation
                else:
                    self.text += event.unicode
                    self.typing_animation = 1.0  # Start typing animation
                # Re-render the text
                self.rendered_text = font.render(self.text, True, BLACK)
        return None

    def draw(self, screen):
        # Update animations
        target_focus = 1.0 if self.active else 0.0
        self.focus_animation += (target_focus - self.focus_animation) * 0.15

        target_glow = 0.8 if self.active else 0.0
        self.glow_intensity += (target_glow - self.glow_intensity) * 0.1

        # Decay typing animation
        self.typing_animation *= 0.95

        # Draw glow effect when focused
        if self.glow_intensity > 0:
            glow_surface = pygame.Surface((self.rect.width + 16, self.rect.height + 16), pygame.SRCALPHA)
            glow_color = (100, 150, 255, int(40 * self.glow_intensity))
            for i in range(4):
                glow_rect = pygame.Rect(8-i*2, 8-i*2, self.rect.width + i*4, self.rect.height + i*4)
                pygame.draw.rect(glow_surface, glow_color, glow_rect, border_radius=8)
            screen.blit(glow_surface, (self.rect.x - 8, self.rect.y - 8))

        # Draw shadow
        shadow_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width, self.rect.height)
        shadow_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 60), (0, 0, self.rect.width, self.rect.height), border_radius=8)
        screen.blit(shadow_surface, shadow_rect)

        # Draw main background with gradient
        bg_color = (220 + int(20 * self.focus_animation), 220 + int(20 * self.focus_animation), 220 + int(20 * self.focus_animation))
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=8)

        # Draw border with focus animation
        border_color = (100 + int(100 * self.focus_animation), 120 + int(100 * self.focus_animation), 200 + int(55 * self.focus_animation))
        border_width = 1 + int(2 * self.focus_animation)
        pygame.draw.rect(screen, border_color, self.rect, border_width, border_radius=8)

        # Draw enhanced chess icon with animation
        icon_size = 32
        icon_x = self.rect.left + 12
        icon_y = self.rect.centery - icon_size // 2

        # Icon background with subtle animation
        icon_bg_color = (255, 255, 255) if not self.active else (250, 250, 255)
        pygame.draw.rect(screen, icon_bg_color, (icon_x, icon_y, icon_size, icon_size), border_radius=4)
        pygame.draw.rect(screen, (180, 180, 180), (icon_x, icon_y, icon_size, icon_size), 1, border_radius=4)

        # Draw enhanced checkerboard pattern
        square_size = icon_size // 8
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:  # Black squares
                    square_rect = (icon_x + col * square_size, icon_y + row * square_size, square_size, square_size)
                    pygame.draw.rect(screen, (40, 40, 40), square_rect)

        # Draw text or placeholder with enhanced styling
        padding = 55  # Space for the chess icon
        if self.text:
            # Text with subtle animation
            text_color = (40, 40, 40)
            if self.typing_animation > 0:
                text_color = (20 + int(20 * self.typing_animation), 20 + int(20 * self.typing_animation), 20 + int(20 * self.typing_animation))

            text_surf = font.render(self.text, True, text_color)
            text_rect = text_surf.get_rect(x=self.rect.x + padding, centery=self.rect.centery)
            screen.blit(text_surf, text_rect)

            # Enhanced cursor with pulsing animation
            if self.active and self.cursor_visible:
                cursor_x = self.rect.x + padding + font.size(self.text)[0] + 3
                cursor_alpha = int(200 + 55 * math.sin(pygame.time.get_ticks() * 0.008))
                cursor_color = (50, 50, 50, cursor_alpha)

                # Draw cursor with glow
                cursor_surface = pygame.Surface((3, self.rect.height - 16), pygame.SRCALPHA)
                pygame.draw.rect(cursor_surface, cursor_color, (0, 0, 3, self.rect.height - 16))
                screen.blit(cursor_surface, (cursor_x, self.rect.y + 8))
        else:
            # Enhanced placeholder with fade animation
            placeholder_alpha = 120 - int(40 * self.focus_animation)
            placeholder_font = pygame.font.SysFont('Arial', 20, italic=True)
            placeholder_surf = placeholder_font.render(self.placeholder, True, (placeholder_alpha, placeholder_alpha, placeholder_alpha))
            placeholder_rect = placeholder_surf.get_rect(x=self.rect.x + padding, centery=self.rect.centery)
            screen.blit(placeholder_surf, placeholder_rect)

        # Blink cursor with smoother timing
        self.cursor_timer += 0.03
        if self.cursor_timer > 1:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

class GameListItem:
    def __init__(self, game_id, game_name, host_name, guest_name=None, status="waiting", x=0, y=0, width=600, height=80):
        self.game_id = game_id
        self.game_name = game_name
        self.host_name = host_name
        self.guest_name = guest_name
        self.status = status
        self.rect = pygame.Rect(x, y, width, height)
        self.hover_animation = 0
        self.hover_direction = 1

        # Create appropriate buttons based on game status with dark theme styling
        button_y = y + height//2 - 20
        if status == "waiting":
            self.primary_button = Button(
                x + width - 90,  # Position to match screenshot and avoid overlap
                button_y,
                80,  # Width to match screenshot
                40,  # Height to match screenshot
                "Join",
                (40, 40, 40),  # Darker gray background
                (60, 60, 60),  # Slightly lighter on hover
                WHITE,
                f"join_{game_id}"
            )
            self.secondary_button = None
        else:  # in_progress
            # Position the spectate button to match screenshot exactly
            self.primary_button = Button(
                x + width - 110,  # Position on the right side to match screenshot
                button_y,
                100,  # Width to match screenshot
                40,   # Height to match screenshot
                "Spectate",
                (40, 40, 40),  # Darker gray background
                (60, 60, 60),  # Slightly lighter on hover
                WHITE,
                f"spectate_{game_id}"
            )
            self.secondary_button = None

        self.is_hovered = False

    def draw(self, screen):
        # Update hover animation
        target_hover = 1.0 if self.is_hovered else 0.0
        self.hover_animation += (target_hover - self.hover_animation) * 0.12

        # Draw shadow with depth
        shadow_offset = 2 + int(2 * self.hover_animation)
        shadow_rect = pygame.Rect(
            self.rect.x + shadow_offset,
            self.rect.y + shadow_offset,
            self.rect.width,
            self.rect.height
        )
        shadow_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        shadow_alpha = 40 + int(20 * self.hover_animation)
        pygame.draw.rect(shadow_surface, (0, 0, 0, shadow_alpha), (0, 0, self.rect.width, self.rect.height), border_radius=8)
        screen.blit(shadow_surface, shadow_rect)

        # Draw background with subtle gradient and hover effect
        bg_color = (30 + int(10 * self.hover_animation), 30 + int(10 * self.hover_animation), 30 + int(10 * self.hover_animation))

        # Create gradient background
        gradient_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        for y in range(self.rect.height):
            gradient_factor = y / self.rect.height
            r = int(bg_color[0] * (1 + gradient_factor * 0.2))
            g = int(bg_color[1] * (1 + gradient_factor * 0.2))
            b = int(bg_color[2] * (1 + gradient_factor * 0.2))
            gradient_color = (min(255, r), min(255, g), min(255, b))
            pygame.draw.line(gradient_surface, gradient_color, (0, y), (self.rect.width, y))

        pygame.draw.rect(screen, bg_color, self.rect, border_radius=8)
        screen.blit(gradient_surface, self.rect)

        # Draw elegant border
        border_color = (60 + int(40 * self.hover_animation), 60 + int(40 * self.hover_animation), 60 + int(40 * self.hover_animation))
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=8)

        # Draw animated highlight line at the bottom
        highlight_intensity = 0.7 + 0.3 * math.sin(pygame.time.get_ticks() * 0.003)
        highlight_color = (int(100 * highlight_intensity), int(150 * highlight_intensity), int(255 * highlight_intensity))
        pygame.draw.line(screen, highlight_color,
                        (self.rect.left + 8, self.rect.bottom - 3),
                        (self.rect.right - 8, self.rect.bottom - 3), 3)

        # Draw enhanced chess board icon with animation
        board_size = 68
        board_x = self.rect.left + 25
        board_y = self.rect.top + (self.rect.height - board_size) // 2

        # Icon hover effect
        icon_scale = 1.0 + 0.05 * self.hover_animation
        scaled_board_size = int(board_size * icon_scale)
        scaled_board_x = board_x - (scaled_board_size - board_size) // 2
        scaled_board_y = board_y - (scaled_board_size - board_size) // 2

        # Draw icon shadow
        icon_shadow_rect = (scaled_board_x + 2, scaled_board_y + 2, scaled_board_size, scaled_board_size)
        pygame.draw.rect(screen, (0, 0, 0, 60), icon_shadow_rect, border_radius=4)

        # Draw white background for the chess icon with subtle glow
        icon_bg_color = (255, 255, 255) if not self.is_hovered else (255, 255, 250)
        pygame.draw.rect(screen, icon_bg_color, (scaled_board_x, scaled_board_y, scaled_board_size, scaled_board_size), border_radius=4)
        pygame.draw.rect(screen, (200, 200, 200), (scaled_board_x, scaled_board_y, scaled_board_size, scaled_board_size), 2, border_radius=4)

        # Draw enhanced checkerboard pattern
        square_size = scaled_board_size // 8
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:  # Black squares
                    square_rect = (scaled_board_x + col * square_size, scaled_board_y + row * square_size, square_size, square_size)
                    pygame.draw.rect(screen, (40, 40, 40), square_rect)

        # Draw game name with enhanced typography and shadow
        font_large = pygame.font.SysFont('Arial', 30, bold=True)
        text_x = board_x + board_size + 25

        # Text shadow
        name_shadow = font_large.render(self.game_name, True, (10, 10, 10))
        screen.blit(name_shadow, (text_x + 1, self.rect.top + 16))

        # Main text with hover glow
        text_color = (255, 255, 255) if not self.is_hovered else (255, 255, 240)
        name_text = font_large.render(self.game_name, True, text_color)
        screen.blit(name_text, (text_x, self.rect.top + 15))

        # Draw host name with enhanced styling
        font_small = pygame.font.SysFont('Arial', 22)
        host_shadow = font_small.render(f"White: {self.host_name}", True, (10, 10, 10))
        screen.blit(host_shadow, (text_x + 1, self.rect.top + 56))

        host_color = (180, 180, 180) if not self.is_hovered else (200, 200, 200)
        host_text = font_small.render(f"White: {self.host_name}", True, host_color)
        screen.blit(host_text, (text_x, self.rect.top + 55))

        # Draw enhanced waiting badge with animation
        if self.status == "waiting":
            badge_width = 95
            badge_height = 38
            badge_x = self.rect.right - 210
            badge_y = self.rect.centery - badge_height // 2

            # Badge pulse animation
            pulse = 0.9 + 0.1 * math.sin(pygame.time.get_ticks() * 0.005)
            badge_color = (int(120 * pulse), int(120 * pulse), int(120 * pulse))

            # Badge shadow
            pygame.draw.ellipse(screen, (0, 0, 0, 80), (badge_x + 2, badge_y + 2, badge_width, badge_height))

            # Badge background with gradient
            pygame.draw.ellipse(screen, badge_color, (badge_x, badge_y, badge_width, badge_height))
            pygame.draw.ellipse(screen, (160, 160, 160), (badge_x, badge_y, badge_width, badge_height), 2)

            # Badge text with glow
            badge_font = pygame.font.SysFont('Arial', 18, bold=True)
            badge_text = badge_font.render("Waiting", True, (250, 250, 250))
            badge_rect = badge_text.get_rect(center=(badge_x + badge_width // 2, badge_y + badge_height // 2))
            screen.blit(badge_text, badge_rect)

        # Draw buttons
        self.primary_button.draw(screen)
        if self.secondary_button:
            self.secondary_button.draw(screen)

    def update(self, mouse_pos):
        prev_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Reset animation when hover state changes
        if prev_hovered != self.is_hovered and not self.is_hovered:
            self.hover_animation = 0
            self.hover_direction = 1

        self.primary_button.update(mouse_pos)
        if self.secondary_button:
            self.secondary_button.update(mouse_pos)

    def check_click(self, mouse_pos):
        primary_action = self.primary_button.check_click(mouse_pos)
        if primary_action:
            return primary_action

        if self.secondary_button:
            return self.secondary_button.check_click(mouse_pos)

        return None

class LobbySystem:
    def __init__(self):
        self.games = []
        self.load_games()

    def load_games(self):
        """Load games from file"""
        try:
            if os.path.exists(GAMES_LIST_FILE):
                with open(GAMES_LIST_FILE, 'r') as f:
                    data = json.load(f)
                    self.games = data.get('games', [])
        except Exception as e:
            print(f"Error loading games: {e}")
            self.games = []

    def save_games(self):
        """Save games to file"""
        try:
            with open(GAMES_LIST_FILE, 'w') as f:
                json.dump({'games': self.games}, f)
        except Exception as e:
            print(f"Error saving games: {e}")

    def create_game(self, game_name, host_name):
        """Create a new game"""
        game_id = str(uuid.uuid4())
        game = {
            'game_id': game_id,
            'game_name': game_name,
            'host_name': host_name,
            'guest_name': None,
            'spectators': [],
            'created_at': time.time(),
            'status': 'waiting'
        }
        self.games.append(game)
        self.save_games()
        return game_id

    def get_game(self, game_id):
        """Get a game by ID"""
        for game in self.games:
            if game['game_id'] == game_id:
                return game
        return None

    def join_game(self, game_id, player_name):
        """Join an existing game"""
        game = self.get_game(game_id)
        if game and game['status'] == 'waiting':
            game['guest_name'] = player_name
            game['status'] = 'in_progress'
            self.save_games()
            return True
        return False

    def spectate_game(self, game_id, spectator_name):
        """Spectate an existing game"""
        game = self.get_game(game_id)
        if game:
            if 'spectators' not in game:
                game['spectators'] = []

            # Add spectator if not already in the list
            if spectator_name not in game['spectators']:
                game['spectators'].append(spectator_name)
                self.save_games()
            return True
        return False

    def get_active_games(self):
        """Get all active games (both waiting and in progress)"""
        return [game for game in self.games if game['status'] in ['waiting', 'in_progress']]

    def get_waiting_games(self):
        """Get games waiting for players"""
        return [game for game in self.games if game['status'] == 'waiting']

    def get_in_progress_games(self):
        """Get games that are in progress"""
        return [game for game in self.games if game['status'] == 'in_progress']

def draw_background(screen):
    """Draw an enhanced animated background with chess pattern"""
    current_time = pygame.time.get_ticks() / 1000.0

    # Draw enhanced gradient background with subtle animation
    for y in range(WINDOW_HEIGHT):
        # Create a more sophisticated gradient with subtle wave animation
        wave_offset = math.sin(current_time * 0.5 + y * 0.01) * 5
        color_value = 25 + (y / WINDOW_HEIGHT * 25) + wave_offset
        color_value = max(20, min(60, color_value))  # Clamp values
        color = (color_value, color_value, color_value)
        pygame.draw.line(screen, color, (0, y), (WINDOW_WIDTH, y))

    # Draw floating chess pieces in background
    piece_positions = [
        (100, 150, "pawn", "white", 0.3),
        (WINDOW_WIDTH - 150, 200, "knight", "black", 0.25),
        (200, WINDOW_HEIGHT - 200, "bishop", "white", 0.2),
        (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 250, "rook", "black", 0.35),
    ]

    for x, y, piece, color, speed in piece_positions:
        # Floating animation
        float_y = y + math.sin(current_time * speed) * 15
        float_x = x + math.cos(current_time * speed * 0.7) * 8

        # Create semi-transparent piece
        piece_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
        draw_chess_icon(piece_surface, piece, color, (30, 30), 50)
        piece_surface.set_alpha(30)  # Very subtle
        screen.blit(piece_surface, (float_x, float_y))

    # Draw enhanced chess board pattern at the bottom
    board_rect = (0, WINDOW_HEIGHT - 120, WINDOW_WIDTH, 120)
    pattern_surface = pygame.Surface((WINDOW_WIDTH, 120), pygame.SRCALPHA)

    # Animated chess pattern with wave effect
    square_size = 30
    for x in range(0, WINDOW_WIDTH, square_size):
        for y in range(0, 120, square_size):
            # Wave animation for the pattern
            wave = math.sin(current_time * 2 + x * 0.02) * 0.3
            if ((x // square_size) + (y // square_size)) % 2 == 1:
                alpha = int(80 + 40 * wave)
                color = (0, 0, 0, alpha)
            else:
                alpha = int(120 + 30 * wave)
                color = (255, 255, 255, alpha)

            square_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
            pygame.draw.rect(square_surface, color, (0, 0, square_size, square_size))
            pattern_surface.blit(square_surface, (x, y))

    # Add subtle glow effect to the pattern
    glow_surface = pygame.Surface((WINDOW_WIDTH, 120), pygame.SRCALPHA)
    glow_intensity = 0.5 + 0.3 * math.sin(current_time * 1.5)
    for i in range(5):
        glow_color = (100, 100, 150, int(20 * glow_intensity / (i + 1)))
        pygame.draw.rect(glow_surface, glow_color, (0, i * 2, WINDOW_WIDTH, 120 - i * 4))

    screen.blit(pattern_surface, board_rect)
    screen.blit(glow_surface, board_rect)

    # Draw subtle vignette effect
    vignette_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
    max_distance = math.sqrt(center_x**2 + center_y**2)

    for y in range(0, WINDOW_HEIGHT, 4):  # Sample every 4 pixels for performance
        for x in range(0, WINDOW_WIDTH, 4):
            distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            vignette_strength = min(1.0, distance / max_distance)
            alpha = int(vignette_strength * 40)
            if alpha > 0:
                pygame.draw.rect(vignette_surface, (0, 0, 0, alpha), (x, y, 4, 4))

    screen.blit(vignette_surface, (0, 0))

def main_menu():
    """Main menu screen"""
    # Create buttons with better positioning and sizing
    button_width = 300
    button_height = 60
    button_spacing = 15
    start_y = WINDOW_HEIGHT // 2 - 150  # Moved up to accommodate the new button

    # Create a panel for the buttons with a more elegant design
    panel_width = button_width + 80
    panel_height = button_height * 6 + button_spacing * 5 + 80
    panel_rect = pygame.Rect(
        WINDOW_WIDTH // 2 - panel_width // 2,
        start_y - 50,
        panel_width,
        panel_height
    )

    # Inner panel for a layered effect
    inner_panel_rect = pygame.Rect(
        WINDOW_WIDTH // 2 - (panel_width - 20) // 2,
        start_y - 40,
        panel_width - 20,
        panel_height - 20
    )

    # Create buttons with walnut-inspired colors
    button_color = BUTTON_COLOR  # Walnut-inspired from our color scheme
    hover_color = BUTTON_HOVER_COLOR  # Lighter walnut for hover

    # Local two-player game button (new)
    local_game_button = Button(
        WINDOW_WIDTH // 2 - button_width // 2,
        start_y,
        button_width,
        button_height,
        "Local Two-Player Game",
        button_color,
        hover_color,
        WHITE,
        "local_game"
    )

    quick_match_button = Button(
        WINDOW_WIDTH // 2 - button_width // 2,
        start_y + button_height + button_spacing,
        button_width,
        button_height,
        "Online Quick Match",
        button_color,
        hover_color,
        WHITE,
        "quick_match"
    )

    create_game_button = Button(
        WINDOW_WIDTH // 2 - button_width // 2,
        start_y + (button_height + button_spacing) * 2,
        button_width,
        button_height,
        "Create Online Game",
        button_color,
        hover_color,
        WHITE,
        "create_game"
    )

    join_game_button = Button(
        WINDOW_WIDTH // 2 - button_width // 2,
        start_y + (button_height + button_spacing) * 3,
        button_width,
        button_height,
        "Join Online Game",
        button_color,
        hover_color,
        WHITE,
        "join_game"
    )

    spectate_button = Button(
        WINDOW_WIDTH // 2 - button_width // 2,
        start_y + (button_height + button_spacing) * 4,
        button_width,
        button_height,
        "Spectate Online Game",
        button_color,
        hover_color,
        WHITE,
        "spectate_games"
    )

    exit_button = Button(
        WINDOW_WIDTH // 2 - button_width // 2,
        start_y + (button_height + button_spacing) * 5,
        button_width,
        button_height,
        "Exit Game",
        button_color,
        hover_color,
        WHITE,
        "exit"
    )

    # Animation variables
    title_bounce = 0
    title_direction = 1
    time_passed = 0

    running = True
    while running:
        time_passed += 1/FPS

        # Get mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        local_game_button.update(mouse_pos)
        quick_match_button.update(mouse_pos)
        create_game_button.update(mouse_pos)
        join_game_button.update(mouse_pos)
        spectate_button.update(mouse_pos)
        exit_button.update(mouse_pos)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    action = local_game_button.check_click(mouse_pos)
                    if action == "local_game":
                        return "local_game"

                    action = quick_match_button.check_click(mouse_pos)
                    if action == "quick_match":
                        return "quick_match"

                    action = create_game_button.check_click(mouse_pos)
                    if action == "create_game":
                        return "create_game"

                    action = join_game_button.check_click(mouse_pos)
                    if action == "join_game":
                        return "join_game"

                    action = spectate_button.check_click(mouse_pos)
                    if action == "spectate_games":
                        return "spectate_games"

                    action = exit_button.check_click(mouse_pos)
                    if action == "exit":
                        pygame.quit()
                        sys.exit()

        # Draw everything
        draw_background(screen)

        # Draw enhanced panel with multiple layers and glow effects
        # Outer glow
        glow_surface = pygame.Surface((panel_width + 40, panel_height + 40), pygame.SRCALPHA)
        for i in range(10):
            glow_alpha = int(20 / (i + 1))
            glow_rect = pygame.Rect(20 - i*2, 20 - i*2, panel_width + i*4, panel_height + i*4)
            pygame.draw.rect(glow_surface, (150, 150, 150, glow_alpha), glow_rect, border_radius=20)
        screen.blit(glow_surface, (panel_rect.x - 20, panel_rect.y - 20))

        # Panel shadow
        shadow_rect = pygame.Rect(panel_rect.x + 5, panel_rect.y + 5, panel_width, panel_height)
        shadow_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 100), (0, 0, panel_width, panel_height), border_radius=15)
        screen.blit(shadow_surface, shadow_rect)

        # Main panel with gradient
        gradient_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        for y in range(panel_height):
            gradient_factor = y / panel_height
            base_color = 45
            color_value = int(base_color * (1 + gradient_factor * 0.3))
            color = (color_value, color_value, color_value)
            pygame.draw.line(gradient_surface, color, (0, y), (panel_width, y))

        pygame.draw.rect(screen, DARK_GRAY, panel_rect, border_radius=15)
        screen.blit(gradient_surface, panel_rect)

        # Elegant border with animation
        border_intensity = 0.8 + 0.2 * math.sin(time_passed * 2)
        border_color = (int(150 * border_intensity), int(150 * border_intensity), int(150 * border_intensity))
        pygame.draw.rect(screen, border_color, panel_rect, 3, border_radius=15)

        # Inner highlight
        highlight_rect = pygame.Rect(panel_rect.x + 3, panel_rect.y + 3, panel_width - 6, panel_height - 6)
        pygame.draw.rect(screen, (255, 255, 255, 30), highlight_rect, 2, border_radius=12)

        # Enhanced chess pattern overlay
        pattern_size = 25
        pattern_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pattern_time = time_passed * 0.5

        for row in range(panel_height // pattern_size):
            for col in range(panel_width // pattern_size):
                # Animated pattern with wave effect
                wave = math.sin(pattern_time + row * 0.3 + col * 0.3) * 0.5 + 0.5
                if (row + col) % 2 == 0:
                    alpha = int(15 * wave)
                    pygame.draw.rect(pattern_surface, (255, 255, 255, alpha),
                                   (col * pattern_size, row * pattern_size, pattern_size, pattern_size))
        screen.blit(pattern_surface, panel_rect)

        # Enhanced title animation
        title_bounce += 0.02 * title_direction
        if title_bounce > 1:
            title_bounce = 1
            title_direction = -1
        elif title_bounce < 0:
            title_bounce = 0
            title_direction = 1

        # Multi-layered title with glow effect
        title_offset = int(math.sin(time_passed * 2) * 4)
        title_scale = 1.0 + 0.05 * math.sin(time_passed * 1.5)

        # Title glow layers
        for i in range(3):
            glow_font = pygame.font.SysFont('Arial', int(48 * title_scale) + i*2, bold=True)
            glow_text = glow_font.render("CHESS GAME LOBBY", True, (100, 100, 100, 80 - i*20))
            glow_rect = glow_text.get_rect(center=(WINDOW_WIDTH // 2 + i, 80 + title_offset + i))
            screen.blit(glow_text, glow_rect)

        # Main title with enhanced styling
        title_font_scaled = pygame.font.SysFont('Arial', int(48 * title_scale), bold=True)

        # Title shadow
        title_shadow = title_font_scaled.render("CHESS GAME LOBBY", True, (20, 20, 20))
        shadow_rect = title_shadow.get_rect(center=(WINDOW_WIDTH // 2 + 3, 80 + 3 + title_offset))
        screen.blit(title_shadow, shadow_rect)

        # Main title text with subtle color animation
        title_brightness = 150 + int(50 * math.sin(time_passed * 1.2))
        title_color = (title_brightness, title_brightness, title_brightness)
        title_text = title_font_scaled.render("CHESS GAME LOBBY", True, title_color)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80 + title_offset))
        screen.blit(title_text, title_rect)

        # Enhanced chess icons with complex animations
        icon_size = 45
        icon_y = 80 + title_offset
        icon_bounce = math.sin(time_passed * 3) * 8
        icon_rotation = time_passed * 20  # Slow rotation

        # Animated chess pieces with glow
        pieces_data = [
            ("king", "white", WINDOW_WIDTH // 2 - title_rect.width // 2 - 60, icon_bounce),
            ("queen", "black", WINDOW_WIDTH // 2 + title_rect.width // 2 + 60, -icon_bounce)
        ]

        for piece, color, x, bounce in pieces_data:
            # Piece glow
            glow_surface = pygame.Surface((icon_size + 20, icon_size + 20), pygame.SRCALPHA)
            for i in range(5):
                glow_alpha = int(40 / (i + 1))
                glow_pos = (10 - i, 10 - i)
                glow_size = icon_size + i*2
                draw_chess_icon(glow_surface, piece, color, (glow_pos[0] + glow_size//2, glow_pos[1] + glow_size//2), glow_size)
                glow_surface.set_alpha(glow_alpha)
            screen.blit(glow_surface, (x - 10, icon_y + bounce - 10))

            # Main piece
            draw_chess_icon(screen, piece, color, (x, icon_y + bounce), icon_size)

        # Draw buttons
        local_game_button.draw(screen)
        quick_match_button.draw(screen)
        create_game_button.draw(screen)
        join_game_button.draw(screen)
        spectate_button.draw(screen)
        exit_button.draw(screen)

        # Removed "RECOMMENDED" label as requested

        # Draw enhanced version info with animation
        version_rect = pygame.Rect(WINDOW_WIDTH - 90, WINDOW_HEIGHT - 40, 80, 30)

        # Version badge glow
        version_glow = pygame.Surface((90, 40), pygame.SRCALPHA)
        glow_intensity = 0.6 + 0.4 * math.sin(time_passed * 3)
        for i in range(3):
            glow_alpha = int(30 * glow_intensity / (i + 1))
            glow_rect = pygame.Rect(5 - i, 5 - i, 80 + i*2, 30 + i*2)
            pygame.draw.rect(version_glow, (100, 100, 150, glow_alpha), glow_rect, border_radius=8)
        screen.blit(version_glow, (WINDOW_WIDTH - 95, WINDOW_HEIGHT - 45))

        # Version badge background with gradient
        gradient_surface = pygame.Surface((80, 30), pygame.SRCALPHA)
        for y in range(30):
            gradient_factor = y / 30
            color_value = int(50 * (1 + gradient_factor * 0.4))
            color = (color_value, color_value, color_value + 10)
            pygame.draw.line(gradient_surface, color, (0, y), (80, y))

        pygame.draw.rect(screen, (45, 45, 55), version_rect, border_radius=8)
        screen.blit(gradient_surface, version_rect)

        # Animated border
        border_brightness = 120 + int(40 * math.sin(time_passed * 2.5))
        border_color = (border_brightness, border_brightness, border_brightness + 20)
        pygame.draw.rect(screen, border_color, version_rect, 2, border_radius=8)

        # Version text with subtle animation
        version_font = pygame.font.SysFont('Arial', 16, bold=True)
        text_brightness = 180 + int(30 * math.sin(time_passed * 1.8))
        version_color = (text_brightness, text_brightness, text_brightness + 20)
        version_text = version_font.render("v2.0.0", True, version_color)
        version_text_rect = version_text.get_rect(center=version_rect.center)
        screen.blit(version_text, version_text_rect)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

def create_game_screen():
    """Create game screen"""
    # Create panel for form
    panel_width = 500
    panel_height = 400
    panel_rect = pygame.Rect(
        WINDOW_WIDTH // 2 - panel_width // 2,
        WINDOW_HEIGHT // 2 - panel_height // 2,
        panel_width,
        panel_height
    )

    # Create input boxes
    input_width = 400
    game_name_input = InputBox(
        WINDOW_WIDTH // 2 - input_width // 2,
        WINDOW_HEIGHT // 2 - 80,
        input_width,
        50,
        "",
        "Enter game name..."
    )

    player_name_input = InputBox(
        WINDOW_WIDTH // 2 - input_width // 2,
        WINDOW_HEIGHT // 2 + 20,
        input_width,
        50,
        "",
        "Enter your name..."
    )

    create_button = Button(
        WINDOW_WIDTH // 2 - 100,
        WINDOW_HEIGHT // 2 + 120,
        200,
        50,
        "Create",
        BUTTON_COLOR,
        BUTTON_HOVER_COLOR,
        WHITE,
        "create"
    )

    back_button = Button(
        50,
        50,
        120,
        50,
        "Back",
        GRAY,
        LIGHT_GRAY,
        WHITE,
        "back"
    )

    error_message = ""
    time_passed = 0

    # Chess piece animation
    piece_rotation = 0

    running = True
    while running:
        time_passed += 1/FPS
        piece_rotation += 0.5  # Rotate chess piece

        # Get mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        create_button.update(mouse_pos)
        back_button.update(mouse_pos)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle input box events
            game_name_input.handle_event(event)
            player_name_input.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    action = create_button.check_click(mouse_pos)
                    if action == "create":
                        if not game_name_input.text:
                            error_message = "Please enter a game name"
                        elif not player_name_input.text:
                            error_message = "Please enter your name"
                        else:
                            # Create the game
                            lobby = LobbySystem()
                            game_id = lobby.create_game(game_name_input.text, player_name_input.text)

                            # Start the game as white player
                            import subprocess
                            subprocess.Popen(["python", "two_player_chess.py", "white", game_id, player_name_input.text])
                            return

                    action = back_button.check_click(mouse_pos)
                    if action == "back":
                        return

        # Draw everything
        draw_background(screen)

        # Draw form panel
        draw_chess_panel(screen, panel_rect, border_color=TITLE_COLOR)

        # Draw decorative chess board on the side with classic black-and-white color scheme
        board_size = 120
        board_rect = (WINDOW_WIDTH // 2 - panel_width // 2 - board_size - 30, WINDOW_HEIGHT // 2 - board_size // 2, board_size, board_size)
        draw_chess_board_pattern(screen, board_rect, light_color=(255, 255, 255), dark_color=(0, 0, 0))
        pygame.draw.rect(screen, TITLE_COLOR, board_rect, 2)

        # Draw animated chess piece
        piece_x = board_rect[0] + board_size // 2
        piece_y = board_rect[1] + board_size // 2
        piece_size = 60

        # Create a temporary surface for rotation
        piece_surface = pygame.Surface((piece_size*2, piece_size*2), pygame.SRCALPHA)
        draw_chess_icon(piece_surface, "king", "white", (piece_size, piece_size), piece_size)

        # Rotate the piece
        rotated_piece = pygame.transform.rotate(piece_surface, piece_rotation)
        piece_rect = rotated_piece.get_rect(center=(piece_x, piece_y))
        screen.blit(rotated_piece, piece_rect)

        # Draw title with animation
        title_offset = int(math.sin(time_passed * 2) * 3)
        title_shadow = header_font.render("Create New Game", True, (30, 30, 30))
        title_text = header_font.render("Create New Game", True, TITLE_COLOR)

        # Shadow
        shadow_rect = title_shadow.get_rect(center=(WINDOW_WIDTH // 2 + 2, panel_rect.y - 50 + 2 + title_offset))
        screen.blit(title_shadow, shadow_rect)

        # Main text
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, panel_rect.y - 50 + title_offset))
        screen.blit(title_text, title_rect)

        # Draw labels with icons
        draw_chess_icon(screen, "rook", "white", (WINDOW_WIDTH // 2 - input_width // 2 - 30, WINDOW_HEIGHT // 2 - 80 + 25), 20)
        game_name_label = font.render("Game Name:", True, WHITE)
        screen.blit(game_name_label, (WINDOW_WIDTH // 2 - input_width // 2, WINDOW_HEIGHT // 2 - 110))

        draw_chess_icon(screen, "pawn", "white", (WINDOW_WIDTH // 2 - input_width // 2 - 30, WINDOW_HEIGHT // 2 + 20 + 25), 20)
        player_name_label = font.render("Your Name:", True, WHITE)
        screen.blit(player_name_label, (WINDOW_WIDTH // 2 - input_width // 2, WINDOW_HEIGHT // 2 - 10))

        # Draw input boxes
        game_name_input.draw(screen)
        player_name_input.draw(screen)

        # Draw buttons
        create_button.draw(screen)
        back_button.draw(screen)

        # Draw error message if any
        if error_message:
            # Create error panel
            error_panel = pygame.Rect(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 + 180, 400, 40)
            pygame.draw.rect(screen, (80, 0, 0), error_panel, border_radius=10)
            pygame.draw.rect(screen, RED, error_panel, 2, border_radius=10)

            error_text = font.render(error_message, True, WHITE)
            error_rect = error_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 200))
            screen.blit(error_text, error_rect)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

def join_game_screen():
    """Join game screen"""
    lobby = LobbySystem()

    # Create back button with dark theme styling
    back_button = Button(
        50,
        50,
        100,
        40,
        "Back",
        (50, 50, 50),  # Dark gray background
        (80, 80, 80),  # Lighter gray on hover
        WHITE,
        "back"
    )

    # Create refresh button with dark theme styling
    refresh_button = Button(
        WINDOW_WIDTH - 150,
        50,
        100,
        40,
        "Refresh",
        (50, 50, 50),  # Dark gray background
        (80, 80, 80),  # Lighter gray on hover
        WHITE,
        "refresh"
    )

    # Create search input box with dark theme styling - centered on screen
    search_input = InputBox(
        WINDOW_WIDTH // 2 - 275,  # Centered horizontally
        100,  # Adjusted position to match screenshot
        550,  # Wider to match screenshot
        50,   # Taller to match screenshot
        "",
        "Search games..."
    )

    # Create player name input with dark theme styling
    player_name_input = InputBox(
        WINDOW_WIDTH // 2 - 275,  # Centered to match search box
        WINDOW_HEIGHT - 80,
        550,  # Same width as search box
        50,
        "",
        "Enter your name to join..."
    )

    error_message = ""
    scroll_offset = 0
    max_visible_games = 2  # Reduced to match the screenshot

    # Scroll buttons with dark theme styling
    scroll_up_button = Button(
        WINDOW_WIDTH - 80,
        160,
        60,
        40,
        "▲",
        (50, 50, 50),  # Dark gray background
        (80, 80, 80),  # Lighter gray on hover
        WHITE,
        "scroll_up"
    )

    scroll_down_button = Button(
        WINDOW_WIDTH - 80,
        WINDOW_HEIGHT - 160,
        60,
        40,
        "▼",
        (50, 50, 50),  # Dark gray background
        (80, 80, 80),  # Lighter gray on hover
        WHITE,
        "scroll_down"
    )

    running = True
    while running:
        # Get mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        back_button.update(mouse_pos)
        refresh_button.update(mouse_pos)
        scroll_up_button.update(mouse_pos)
        scroll_down_button.update(mouse_pos)

        # Get waiting games
        waiting_games = lobby.get_waiting_games()

        # Filter games based on search input
        filtered_games = waiting_games
        if search_input.text:
            search_term = search_input.text.lower()
            filtered_games = [
                game for game in waiting_games
                if search_term in game['game_name'].lower() or
                   search_term in game['host_name'].lower()
            ]

        # Adjust scroll offset if needed
        max_scroll = max(0, len(filtered_games) - max_visible_games)
        scroll_offset = min(max_scroll, max(0, scroll_offset))

        # Create game list items for visible games
        game_items = []
        visible_games = filtered_games[scroll_offset:scroll_offset + max_visible_games]

        # Game list area
        list_area_top = 180
        list_area_height = WINDOW_HEIGHT - 300  # Space for list between header and input

        # Calculate y positions for visible games with more spacing to match screenshot
        for i, game in enumerate(visible_games):
            y_pos = list_area_top + i * 140  # Increased spacing between items to prevent overlap
            item = GameListItem(
                game_id=game['game_id'],
                game_name=game['game_name'],
                host_name=game['host_name'],
                x=WINDOW_WIDTH // 2 - 425,  # Centered to align with search box
                y=y_pos,
                width=850,  # Wider to match screenshot
                height=120  # Taller items to match screenshot
            )
            game_items.append(item)
            item.update(mouse_pos)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle input box events
            player_name_input.handle_event(event)
            search_input.handle_event(event)

            # Handle mouse wheel for scrolling
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset -= event.y  # Scroll up/down
                scroll_offset = max(0, min(max_scroll, scroll_offset))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    action = back_button.check_click(mouse_pos)
                    if action == "back":
                        return

                    action = refresh_button.check_click(mouse_pos)
                    if action == "refresh":
                        lobby.load_games()

                    # Handle scroll buttons
                    action = scroll_up_button.check_click(mouse_pos)
                    if action == "scroll_up" and scroll_offset > 0:
                        scroll_offset -= 1

                    action = scroll_down_button.check_click(mouse_pos)
                    if action == "scroll_down" and scroll_offset < max_scroll:
                        scroll_offset += 1

                    # Check game item clicks
                    for item in game_items:
                        action = item.check_click(mouse_pos)
                        if action and action.startswith("join_"):
                            game_id = action.split("_")[1]
                            if not player_name_input.text:
                                error_message = "Please enter your name to join"
                            else:
                                # Join the game
                                if lobby.join_game(game_id, player_name_input.text):
                                    # Start the game as black player
                                    import subprocess
                                    subprocess.Popen(["python", "two_player_chess.py", "black", game_id, player_name_input.text])
                                    return
                                else:
                                    error_message = "Failed to join game"

        # Draw everything
        # Draw a solid dark background instead of the gradient
        screen.fill((20, 20, 20))  # Very dark gray background

        # Draw a chess board pattern at the bottom with classic black-and-white color scheme
        board_rect = (0, WINDOW_HEIGHT - 100, WINDOW_WIDTH, 100)
        pattern_surface = pygame.Surface((WINDOW_WIDTH, 100), pygame.SRCALPHA)
        # Use the classic black-and-white color scheme
        draw_chess_board_pattern(pattern_surface, (0, 0, WINDOW_WIDTH, 100), light_color=(255, 255, 255), dark_color=(0, 0, 0), square_size=25)
        pattern_surface.set_alpha(150)  # Make it visible
        screen.blit(pattern_surface, board_rect)

        # Draw title - larger and centered
        title_font = pygame.font.SysFont('Arial', 40, bold=True)
        title_text = title_font.render("Available Games", True, WHITE)  # White text
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 60))
        screen.blit(title_text, title_rect)

        # Draw buttons
        back_button.draw(screen)
        refresh_button.draw(screen)

        # Draw search box
        search_label = font.render("Search:", True, WHITE)
        # Position the label to align with the centered search box
        search_label_x = WINDOW_WIDTH // 2 - 275 - search_label.get_width() - 10
        screen.blit(search_label, (search_label_x, 110))  # Aligned with search box
        search_input.draw(screen)

        # Draw scroll buttons if needed
        if len(filtered_games) > max_visible_games:
            scroll_up_button.draw(screen)
            scroll_down_button.draw(screen)

            # Draw scroll indicator
            if filtered_games:
                total_height = WINDOW_HEIGHT - 320
                indicator_height = max(40, total_height * max_visible_games / len(filtered_games))
                indicator_pos = 200 + (total_height - indicator_height) * (scroll_offset / max_scroll) if max_scroll > 0 else 200

                indicator_rect = pygame.Rect(WINDOW_WIDTH - 80, indicator_pos, 60, indicator_height)
                pygame.draw.rect(screen, LIGHT_GRAY, indicator_rect, border_radius=5)
                pygame.draw.rect(screen, GRAY, indicator_rect, 2, border_radius=5)

        # Draw game list area background with dark theme styling
        list_bg_rect = pygame.Rect(WINDOW_WIDTH // 2 - 450, list_area_top - 10, 900, list_area_height)  # Centered to match search box
        pygame.draw.rect(screen, (30, 30, 30), list_bg_rect, border_radius=5)  # Darker background

        # Draw game list
        if not filtered_games:
            no_games_text = font.render("No games available. Try refreshing or create your own game.", True, WHITE)
            no_games_rect = no_games_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(no_games_text, no_games_rect)
        else:
            # Show how many games are available
            games_count_text = small_font.render(f"Showing {len(visible_games)} of {len(filtered_games)} games", True, LIGHT_GRAY)
            # Position to align with the centered game list
            screen.blit(games_count_text, (WINDOW_WIDTH // 2 - 425, list_area_top - 30))  # Aligned with game list

            # Draw visible games
            for item in game_items:
                item.draw(screen)

        # Draw player name input with better positioning
        player_name_label = font.render("Your Name:", True, WHITE)
        # Position the label to align with the centered player name input
        name_label_x = WINDOW_WIDTH // 2 - 275 - player_name_label.get_width() - 10
        screen.blit(player_name_label, (name_label_x, WINDOW_HEIGHT - 110))  # Aligned with input box
        player_name_input.draw(screen)

        # Draw error message if any
        if error_message:
            error_text = font.render(error_message, True, RED)
            error_rect = error_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
            screen.blit(error_text, error_rect)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

def spectate_game_screen():
    """Spectate game screen - shows in-progress games"""
    lobby = LobbySystem()

    # Create back button
    back_button = Button(
        50,
        50,
        100,
        40,
        "Back",
        GRAY,
        LIGHT_GRAY,
        WHITE,
        "back"
    )

    # Create refresh button
    refresh_button = Button(
        WINDOW_WIDTH - 150,
        50,
        100,
        40,
        "Refresh",
        BUTTON_COLOR,
        BUTTON_HOVER_COLOR,
        WHITE,
        "refresh"
    )

    # No spectator name input needed

    error_message = ""
    scroll_offset = 0
    max_visible_games = 3  # Show exactly 3 games as in the screenshot

    # Scroll buttons
    scroll_up_button = Button(
        WINDOW_WIDTH - 80,
        160,
        60,
        40,
        "▲",
        GRAY,
        LIGHT_GRAY,
        WHITE,
        "scroll_up"
    )

    scroll_down_button = Button(
        WINDOW_WIDTH - 80,
        WINDOW_HEIGHT - 160,
        60,
        40,
        "▼",
        GRAY,
        LIGHT_GRAY,
        WHITE,
        "scroll_down"
    )

    running = True
    while running:
        # Get mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        back_button.update(mouse_pos)
        refresh_button.update(mouse_pos)
        scroll_up_button.update(mouse_pos)
        scroll_down_button.update(mouse_pos)

        # Get in-progress games
        in_progress_games = lobby.get_in_progress_games()

        # No search filtering in spectator mode as per new design
        filtered_games = in_progress_games

        # Adjust scroll offset if needed
        max_scroll = max(0, len(filtered_games) - max_visible_games)
        scroll_offset = min(max_scroll, max(0, scroll_offset))

        # Create game list items for visible games
        game_items = []
        visible_games = filtered_games[scroll_offset:scroll_offset + max_visible_games]

        # Game list area
        list_area_top = 180
        list_area_height = WINDOW_HEIGHT - 350  # Increased space between list and input field

        # Draw a container panel for the game list
        list_panel_rect = pygame.Rect(
            WINDOW_WIDTH // 2 - 320,
            list_area_top - 10,
            640,
            list_area_height
        )
        draw_chess_panel(screen, list_panel_rect, border_color=TITLE_COLOR)

        # Calculate y positions for visible games with exact spacing to match screenshot
        for i, game in enumerate(visible_games):
            # No spacing between items as shown in screenshot
            y_pos = list_area_top + i * 90  # Exact spacing to match screenshot
            item = GameListItem(
                game_id=game['game_id'],
                game_name=game['game_name'],
                host_name=game['host_name'],
                guest_name=game.get('guest_name', "Unknown"),
                status=game['status'],
                x=WINDOW_WIDTH // 2 - 310,  # Adjusted to center better
                y=y_pos,
                width=620,  # Slightly wider to match screenshot
                height=90   # Height to match screenshot
            )
            game_items.append(item)
            item.update(mouse_pos)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # No input box events to handle

            # Handle mouse wheel for scrolling
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset -= event.y  # Scroll up/down
                scroll_offset = max(0, min(max_scroll, scroll_offset))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    action = back_button.check_click(mouse_pos)
                    if action == "back":
                        return

                    action = refresh_button.check_click(mouse_pos)
                    if action == "refresh":
                        lobby.load_games()

                    # Handle scroll buttons
                    action = scroll_up_button.check_click(mouse_pos)
                    if action == "scroll_up" and scroll_offset > 0:
                        scroll_offset -= 1

                    action = scroll_down_button.check_click(mouse_pos)
                    if action == "scroll_down" and scroll_offset < max_scroll:
                        scroll_offset += 1

                    # Check game item clicks
                    for item in game_items:
                        action = item.check_click(mouse_pos)
                        if action and action.startswith("spectate_"):
                            game_id = action.split("_")[1]

                            # Use "Spectator" as the default name
                            spectator_name = "Spectator"

                            # Spectate the game
                            if lobby.spectate_game(game_id, spectator_name):
                                # Start the game as spectator
                                import subprocess
                                subprocess.Popen(["python", "two_player_chess.py", "spectator", game_id, spectator_name])
                                return
                            else:
                                error_message = "Failed to spectate game"

        # Draw everything
        draw_background(screen)

        # Draw title at the top center of the screen
        title_text = header_font.render("Spectate Games", True, TITLE_COLOR)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 25))
        screen.blit(title_text, title_rect)

        # Draw buttons
        back_button.draw(screen)
        refresh_button.draw(screen)

        # No search box in spectator mode as per new design

        # Draw scroll buttons if needed
        if len(filtered_games) > max_visible_games:
            scroll_up_button.draw(screen)
            scroll_down_button.draw(screen)

            # Draw scroll indicator
            if filtered_games:
                total_height = WINDOW_HEIGHT - 320
                indicator_height = max(40, total_height * max_visible_games / len(filtered_games))
                indicator_pos = 200 + (total_height - indicator_height) * (scroll_offset / max_scroll) if max_scroll > 0 else 200

                indicator_rect = pygame.Rect(WINDOW_WIDTH - 80, indicator_pos, 60, indicator_height)
                pygame.draw.rect(screen, LIGHT_GRAY, indicator_rect, border_radius=5)
                pygame.draw.rect(screen, GRAY, indicator_rect, 2, border_radius=5)

        # Draw game list area background - match the screenshot exactly
        list_bg_rect = pygame.Rect(WINDOW_WIDTH // 2 - 320, list_area_top - 10, 640, list_area_height)
        pygame.draw.rect(screen, (25, 25, 25), list_bg_rect, border_radius=5)  # Darker background
        pygame.draw.rect(screen, (50, 50, 50), list_bg_rect, 1, border_radius=5)  # Subtle border

        # Draw game list
        if not filtered_games:
            no_games_text = font.render("No games in progress. Try refreshing or check back later.", True, WHITE)
            no_games_rect = no_games_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(no_games_text, no_games_rect)
        else:
            # Show how many games are available
            games_count_text = small_font.render(f"Showing {len(visible_games)} of {len(filtered_games)} games", True, LIGHT_GRAY)
            # Position to align with the game list as shown in screenshot
            screen.blit(games_count_text, (WINDOW_WIDTH // 2 - 80, list_area_top - 30))

            # Draw visible games
            for item in game_items:
                item.draw(screen)

        # Draw a panel for the name input section - styled to match project's color scheme
        name_panel_rect = pygame.Rect(
            0,  # Full width panel
            WINDOW_HEIGHT - 100,
            WINDOW_WIDTH,  # Full width panel
            100  # Taller panel to match screenshot
        )
        # Use the project's dark gray theme
        pygame.draw.rect(screen, (30, 30, 30), name_panel_rect)

        # Draw the chess board pattern at the bottom
        pattern_surface = pygame.Surface((WINDOW_WIDTH, 100), pygame.SRCALPHA)
        draw_chess_board_pattern(pattern_surface, (0, 0, WINDOW_WIDTH, 100),
                               light_color=(255, 255, 255), dark_color=(0, 0, 0), square_size=25)
        pattern_surface.set_alpha(150)  # Make it visible but not too distracting
        screen.blit(pattern_surface, (0, WINDOW_HEIGHT - 100))

        # No spectator name input needed

        # Draw error message if any
        if error_message:
            error_text = font.render(error_message, True, RED)
            error_rect = error_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
            screen.blit(error_text, error_rect)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

def quick_match_screen():
    """Quick Match screen - allows setting up a two-player game quickly"""
    # Create panel for form
    panel_width = 500
    panel_height = 400  # Increased height to accommodate the new layout
    panel_rect = pygame.Rect(
        WINDOW_WIDTH // 2 - panel_width // 2,
        WINDOW_HEIGHT // 2 - panel_height // 2,
        panel_width,
        panel_height
    )

    # Create input box for player 1 only
    input_width = 400
    player1_name_input = InputBox(
        WINDOW_WIDTH // 2 - input_width // 2,
        WINDOW_HEIGHT // 2 - 60,  # Centered better vertically
        input_width,
        50,
        "",
        "Enter your name..."
    )

    # Default name for player 2 (used internally, not displayed)
    player2_name = "Player 2"

    # Bot options
    play_against_bot = False
    bot_difficulty = "medium"  # Default difficulty

    # Bot difficulty buttons - horizontal layout with better spacing
    difficulty_button_width = 100
    difficulty_button_height = 40
    button_spacing = 20

    # Calculate positions to center the three buttons
    total_width = 3 * difficulty_button_width + 2 * button_spacing
    left_button_x = WINDOW_WIDTH // 2 - total_width // 2

    easy_button = Button(
        left_button_x,
        WINDOW_HEIGHT // 2 + 60,  # Positioned below the toggle with more space
        difficulty_button_width,
        difficulty_button_height,
        "Easy",
        BUTTON_COLOR,
        BUTTON_HOVER_COLOR,
        WHITE,
        "easy"
    )

    medium_button = Button(
        left_button_x + difficulty_button_width + button_spacing,
        WINDOW_HEIGHT // 2 + 60,
        difficulty_button_width,
        difficulty_button_height,
        "Medium",
        ACCENT_COLOR,  # Highlighted by default
        BUTTON_HOVER_COLOR,
        WHITE,
        "medium"
    )

    hard_button = Button(
        left_button_x + 2 * (difficulty_button_width + button_spacing),
        WINDOW_HEIGHT // 2 + 60,
        difficulty_button_width,
        difficulty_button_height,
        "Hard",
        BUTTON_COLOR,
        BUTTON_HOVER_COLOR,
        WHITE,
        "hard"
    )

    start_button = Button(
        WINDOW_WIDTH // 2 - 150,
        WINDOW_HEIGHT // 2 + 120,  # Moved down to make room for difficulty buttons
        300,  # Wider button
        50,
        "Start Game",
        (0, 180, 0),  # Green
        (0, 220, 0),  # Lighter green
        WHITE,
        "start"
    )

    back_button = Button(
        50,
        50,
        120,
        50,
        "Back",
        GRAY,
        LIGHT_GRAY,
        WHITE,
        "back"
    )

    error_message = ""
    time_passed = 0

    running = True
    while running:
        time_passed += 1/FPS

        # Get mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        start_button.update(mouse_pos)
        back_button.update(mouse_pos)
        easy_button.update(mouse_pos)
        medium_button.update(mouse_pos)
        hard_button.update(mouse_pos)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle input box events
            player1_name_input.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check bot toggle area
                    bot_toggle_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 10, 300, 30)
                    if bot_toggle_rect.collidepoint(mouse_pos):
                        play_against_bot = not play_against_bot

                    # Check difficulty buttons if playing against bot
                    if play_against_bot:
                        action = easy_button.check_click(mouse_pos)
                        if action == "easy":
                            bot_difficulty = "easy"

                        action = medium_button.check_click(mouse_pos)
                        if action == "medium":
                            bot_difficulty = "medium"

                        action = hard_button.check_click(mouse_pos)
                        if action == "hard":
                            bot_difficulty = "hard"

                    action = start_button.check_click(mouse_pos)
                    if action == "start":
                        # Validate inputs
                        if not player1_name_input.text:
                            error_message = "Please enter Player 1's name"
                        else:
                            # Generate a unique game ID
                            import uuid
                            game_id = str(uuid.uuid4())

                            if play_against_bot:
                                # Start a game against the bot
                                import subprocess
                                subprocess.Popen([
                                    "python",
                                    "two_player_chess.py",
                                    "white",
                                    game_id,
                                    player1_name_input.text,
                                    "--bot",
                                    bot_difficulty
                                ])
                            else:
                                # Start a regular two-player game
                                import subprocess

                                # Launch the white player window
                                subprocess.Popen([
                                    "python",
                                    "two_player_chess.py",
                                    "white",
                                    game_id,
                                    player1_name_input.text
                                ])

                                # Launch the black player window
                                subprocess.Popen([
                                    "python",
                                    "two_player_chess.py",
                                    "black",
                                    game_id,
                                    player2_name
                                ])
                            return

                    action = back_button.check_click(mouse_pos)
                    if action == "back":
                        return

        # Draw everything
        draw_background(screen)

        # Draw form panel
        draw_chess_panel(screen, panel_rect, border_color=TITLE_COLOR)

        # Draw title with animation
        title_offset = int(math.sin(time_passed * 2) * 3)
        title_shadow = header_font.render("Quick Match", True, (30, 30, 30))
        title_text = header_font.render("Quick Match", True, TITLE_COLOR)

        # Shadow
        shadow_rect = title_shadow.get_rect(center=(WINDOW_WIDTH // 2 + 2, panel_rect.y - 50 + 2 + title_offset))
        screen.blit(title_shadow, shadow_rect)

        # Main text
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, panel_rect.y - 50 + title_offset))
        screen.blit(title_text, title_rect)

        # Draw explanation text above the name input if bot is selected
        if play_against_bot:
            explanation_text = font.render("Play against the computer - test your skills!", True, (255, 255, 150))
            explanation_rect = explanation_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 120))
            screen.blit(explanation_text, explanation_rect)

        # Draw labels with icons
        draw_chess_icon(screen, "king", "white", (WINDOW_WIDTH // 2 - input_width // 2 - 30, WINDOW_HEIGHT // 2 - 60 + 25), 20)
        player1_label = font.render("Your Name:", True, WHITE)
        screen.blit(player1_label, (WINDOW_WIDTH // 2 - input_width // 2, WINDOW_HEIGHT // 2 - 90))

        # Draw input box
        player1_name_input.draw(screen)

        # No Player 2 info displayed

        # Draw bot toggle option
        bot_toggle_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 10, 300, 30)
        pygame.draw.rect(screen, (50, 50, 70), bot_toggle_rect, border_radius=15)

        # Draw toggle switch
        toggle_pos = (WINDOW_WIDTH // 2 - 130 + (260 if play_against_bot else 0), WINDOW_HEIGHT // 2 + 10 + 15)
        toggle_radius = 15
        pygame.draw.circle(screen, (100, 200, 100) if play_against_bot else (150, 150, 170), toggle_pos, toggle_radius)

        # Draw toggle text
        toggle_text = font.render("Play against Bot", True, WHITE)
        toggle_text_rect = toggle_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10 + 15))
        screen.blit(toggle_text, toggle_text_rect)

        # Draw difficulty buttons if bot is selected
        if play_against_bot:
            # Define a more distinct color for selected difficulty
            SELECTED_COLOR = (100, 180, 255)  # Brighter blue for selected

            # Update button colors based on selected difficulty
            easy_button.color = SELECTED_COLOR if bot_difficulty == "easy" else BUTTON_COLOR
            medium_button.color = SELECTED_COLOR if bot_difficulty == "medium" else BUTTON_COLOR
            hard_button.color = SELECTED_COLOR if bot_difficulty == "hard" else BUTTON_COLOR

            # Draw buttons first
            easy_button.draw(screen)
            medium_button.draw(screen)
            hard_button.draw(screen)

            # Add chess piece icons to the buttons
            # Pawn for Easy
            draw_chess_icon(screen, "pawn", "white",
                           (easy_button.rect.x + 20, easy_button.rect.y + easy_button.rect.height // 2), 20)

            # Knight for Medium
            draw_chess_icon(screen, "knight", "white",
                           (medium_button.rect.x + 20, medium_button.rect.y + medium_button.rect.height // 2), 20)

            # Queen for Hard
            draw_chess_icon(screen, "queen", "white",
                           (hard_button.rect.x + 20, hard_button.rect.y + hard_button.rect.height // 2), 20)

            # Add "SELECTED" indicator to the chosen difficulty
            selected_text = small_font.render("SELECTED", True, (255, 255, 100))

            # Position the indicator below the selected button
            if bot_difficulty == "easy":
                selected_rect = selected_text.get_rect(center=(easy_button.rect.centerx, easy_button.rect.bottom + 15))
                # Draw a highlight around the selected button
                pygame.draw.rect(screen, (255, 255, 100), easy_button.rect.inflate(8, 8), 2, border_radius=10)
            elif bot_difficulty == "medium":
                selected_rect = selected_text.get_rect(center=(medium_button.rect.centerx, medium_button.rect.bottom + 15))
                # Draw a highlight around the selected button
                pygame.draw.rect(screen, (255, 255, 100), medium_button.rect.inflate(8, 8), 2, border_radius=10)
            else:  # hard
                selected_rect = selected_text.get_rect(center=(hard_button.rect.centerx, hard_button.rect.bottom + 15))
                # Draw a highlight around the selected button
                pygame.draw.rect(screen, (255, 255, 100), hard_button.rect.inflate(8, 8), 2, border_radius=10)

            # Draw the selected text
            screen.blit(selected_text, selected_rect)

        # Draw buttons
        start_button.draw(screen)
        back_button.draw(screen)

        # Add chess icon to start button
        draw_chess_icon(screen, "king", "white",
                       (start_button.rect.x + 30, start_button.rect.y + start_button.rect.height // 2), 25)

        # Draw explanation text for two-player mode
        if not play_against_bot:
            explanation_text = small_font.render("This will open two game windows - one for each player", True, LIGHT_GRAY)
            explanation_rect = explanation_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 180))
            screen.blit(explanation_text, explanation_rect)

        # Draw error message if any
        if error_message:
            # Create error panel
            error_panel = pygame.Rect(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 + 210, 400, 40)
            pygame.draw.rect(screen, (80, 0, 0), error_panel, border_radius=10)
            pygame.draw.rect(screen, RED, error_panel, 2, border_radius=10)

            error_text = font.render(error_message, True, WHITE)
            error_rect = error_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 230))
            screen.blit(error_text, error_rect)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

def local_game_screen():
    """Local two-player game screen - allows playing chess on the same computer"""
    # Create panel for form
    panel_width = 500
    panel_height = 350
    panel_rect = pygame.Rect(
        WINDOW_WIDTH // 2 - panel_width // 2,
        WINDOW_HEIGHT // 2 - panel_height // 2,
        panel_width,
        panel_height
    )

    # Create input boxes
    input_width = 400
    player1_name_input = InputBox(
        WINDOW_WIDTH // 2 - input_width // 2,
        WINDOW_HEIGHT // 2 - 80,
        input_width,
        50,
        "",
        "Enter Player 1 name (White)..."
    )

    player2_name_input = InputBox(
        WINDOW_WIDTH // 2 - input_width // 2,
        WINDOW_HEIGHT // 2 + 20,
        input_width,
        50,
        "",
        "Enter Player 2 name (Black)..."
    )

    start_button = Button(
        WINDOW_WIDTH // 2 - 100,
        WINDOW_HEIGHT // 2 + 120,
        200,
        50,
        "Start Game",
        (0, 180, 0),  # Green
        (0, 220, 0),  # Lighter green
        WHITE,
        "start"
    )

    back_button = Button(
        50,
        50,
        120,
        50,
        "Back",
        GRAY,
        LIGHT_GRAY,
        WHITE,
        "back"
    )

    error_message = ""
    time_passed = 0

    running = True
    while running:
        time_passed += 1/FPS

        # Get mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        start_button.update(mouse_pos)
        back_button.update(mouse_pos)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle input box events
            player1_name_input.handle_event(event)
            player2_name_input.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    action = start_button.check_click(mouse_pos)
                    if action == "start":
                        # Validate inputs
                        if not player1_name_input.text:
                            error_message = "Please enter Player 1's name"
                        elif not player2_name_input.text:
                            error_message = "Please enter Player 2's name"
                        else:
                            # Start the game directly using two_player_chess.py
                            import subprocess

                            # Generate a unique game ID
                            game_id = str(uuid.uuid4())

                            # Launch the white player window
                            subprocess.Popen([
                                "python",
                                "two_player_chess.py",
                                "white",
                                game_id,
                                player1_name_input.text
                            ])

                            # Launch the black player window
                            subprocess.Popen([
                                "python",
                                "two_player_chess.py",
                                "black",
                                game_id,
                                player2_name_input.text
                            ])
                            return

                    action = back_button.check_click(mouse_pos)
                    if action == "back":
                        return

        # Draw everything
        draw_background(screen)

        # Draw form panel
        draw_chess_panel(screen, panel_rect, border_color=TITLE_COLOR)

        # Draw title with animation
        title_offset = int(math.sin(time_passed * 2) * 3)
        title_shadow = header_font.render("Local Two-Player Game", True, (30, 30, 30))
        title_text = header_font.render("Local Two-Player Game", True, TITLE_COLOR)

        # Shadow
        shadow_rect = title_shadow.get_rect(center=(WINDOW_WIDTH // 2 + 2, panel_rect.y - 50 + 2 + title_offset))
        screen.blit(title_shadow, shadow_rect)

        # Main text
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, panel_rect.y - 50 + title_offset))
        screen.blit(title_text, title_rect)

        # Draw labels with icons
        draw_chess_icon(screen, "king", "white", (WINDOW_WIDTH // 2 - input_width // 2 - 30, WINDOW_HEIGHT // 2 - 80 + 25), 20)
        player1_label = font.render("Player 1 (White):", True, WHITE)
        screen.blit(player1_label, (WINDOW_WIDTH // 2 - input_width // 2, WINDOW_HEIGHT // 2 - 110))

        draw_chess_icon(screen, "king", "black", (WINDOW_WIDTH // 2 - input_width // 2 - 30, WINDOW_HEIGHT // 2 + 20 + 25), 20)
        player2_label = font.render("Player 2 (Black):", True, WHITE)
        screen.blit(player2_label, (WINDOW_WIDTH // 2 - input_width // 2, WINDOW_HEIGHT // 2 - 10))

        # Draw input boxes
        player1_name_input.draw(screen)
        player2_name_input.draw(screen)

        # Draw buttons
        start_button.draw(screen)
        back_button.draw(screen)

        # Draw explanation text
        explanation_text = small_font.render("Play chess with two players on the same computer", True, LIGHT_GRAY)
        explanation_rect = explanation_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        screen.blit(explanation_text, explanation_rect)

        # Draw error message if any
        if error_message:
            # Create error panel
            error_panel = pygame.Rect(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 + 180, 400, 40)
            pygame.draw.rect(screen, (80, 0, 0), error_panel, border_radius=10)
            pygame.draw.rect(screen, RED, error_panel, 2, border_radius=10)

            error_text = font.render(error_message, True, WHITE)
            error_rect = error_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 200))
            screen.blit(error_text, error_rect)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

def main():
    """Main function"""
    running = True
    try:
        while running:
            action = main_menu()

            if action == "local_game":
                local_game_screen()
            elif action == "quick_match":
                quick_match_screen()
            elif action == "create_game":
                create_game_screen()
            elif action == "join_game":
                join_game_screen()
            elif action == "spectate_games":
                spectate_game_screen()
            elif action == "exit":
                running = False
    finally:
        # Clean up resources
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
