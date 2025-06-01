"""
Chess Game Assets Module
Contains helper functions for drawing chess-themed UI elements for the main game
"""
import pygame
import math
import random
import time

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
GOLD = (200, 200, 200)          # Changed to light gray for classic theme
BUTTON_COLOR = (30, 30, 30)     # Dark gray
BUTTON_HOVER_COLOR = (70, 70, 70)  # Lighter gray
CREAM = (240, 240, 240)         # Off-white for text contrast

def draw_enhanced_board(screen, board_x, board_y, board_width, square_size):
    """Draw an enhanced chess board with better visuals"""
    board_size = 8

    # Draw outer decorative border
    outer_border = pygame.Rect(board_x - 20, board_y - 20, board_width + 40, board_width + 40)
    pygame.draw.rect(screen, (30, 30, 40), outer_border, border_radius=5)

    # Draw gold border
    border_rect = pygame.Rect(board_x - 10, board_y - 10, board_width + 20, board_width + 20)
    pygame.draw.rect(screen, GOLD, border_rect, border_radius=3)

    # Draw inner border
    inner_border = pygame.Rect(board_x - 5, board_y - 5, board_width + 10, board_width + 10)
    pygame.draw.rect(screen, (50, 50, 60), inner_border, border_radius=2)

    # Draw squares with classic black-and-white color scheme
    for row in range(board_size):
        for col in range(board_size):
            # Classic black-and-white color scheme
            if (row + col) % 2 == 0:
                color = (255, 255, 255)  # White/light grey for light squares
            else:
                color = (0, 0, 0)  # Black for dark squares

            # Draw square
            pygame.draw.rect(screen, color, (
                board_x + col * square_size,
                board_y + row * square_size,
                square_size, square_size
            ))

    # Draw coordinates
    coord_font = pygame.font.SysFont('Arial', 14)

    # Draw column coordinates (A-H)
    for col in range(board_size):
        # Draw at the bottom
        col_text = coord_font.render(chr(65 + col), True, GOLD)
        screen.blit(col_text, (
            board_x + col * square_size + square_size // 2 - col_text.get_width() // 2,
            board_y + board_width + 5
        ))

    # Draw row coordinates (1-8)
    for row in range(board_size):
        # Draw on the left
        row_text = coord_font.render(str(8 - row), True, GOLD)
        screen.blit(row_text, (
            board_x - 20,
            board_y + row * square_size + square_size // 2 - row_text.get_height() // 2
        ))

def draw_enhanced_sidebar(screen, sidebar_x, sidebar_width, window_height, game, player_color,
                         title_font, header_font, font, small_font, chat_input="", is_typing=False,
                         new_game_button=None, spectator_name=None, is_bot_game=False):
    """Draw an enhanced sidebar with better visuals"""
    # Draw sidebar background with gradient - classic black-and-white
    for y in range(window_height):
        # Create a gradient from dark gray to slightly lighter gray
        color_value = 30 + (y / window_height * 15)
        color = (color_value, color_value, color_value)
        pygame.draw.line(screen, color, (sidebar_x, y), (sidebar_x + sidebar_width, y))

    # Draw decorative border
    pygame.draw.line(screen, GOLD, (sidebar_x, 0), (sidebar_x, window_height), 3)

    # Draw decorative chess pattern at top and bottom
    pattern_height = 20
    pattern_surface_top = pygame.Surface((sidebar_width, pattern_height), pygame.SRCALPHA)
    pattern_surface_bottom = pygame.Surface((sidebar_width, pattern_height), pygame.SRCALPHA)

    # Draw chess patterns with classic black-and-white color scheme
    square_size = 5
    for row in range(pattern_height // square_size):
        for col in range(sidebar_width // square_size):
            color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
            # Top pattern
            pygame.draw.rect(pattern_surface_top, color, (
                col * square_size, row * square_size, square_size, square_size
            ))
            # Bottom pattern
            pygame.draw.rect(pattern_surface_bottom, color, (
                col * square_size, row * square_size, square_size, square_size
            ))

    # Apply transparency
    pattern_surface_top.set_alpha(50)
    pattern_surface_bottom.set_alpha(50)

    # Blit patterns
    screen.blit(pattern_surface_top, (sidebar_x, 0))
    screen.blit(pattern_surface_bottom, (sidebar_x, window_height - pattern_height))

    # Draw title with shadow
    title_text = title_font.render("CHESS GAME", True, GOLD)
    shadow_text = title_font.render("CHESS GAME", True, (30, 30, 30))
    title_rect = title_text.get_rect(center=(sidebar_x + sidebar_width // 2, 30))

    # Draw shadow slightly offset
    shadow_rect = shadow_text.get_rect(center=(sidebar_x + sidebar_width // 2 + 2, 30 + 2))
    screen.blit(shadow_text, shadow_rect)
    screen.blit(title_text, title_rect)

    # Different display for spectators vs players
    if player_color == 'spectator':
        # Draw spectator badge
        spectator_badge = small_font.render("SPECTATOR MODE", True, WHITE)
        badge_width = spectator_badge.get_width() + 20
        badge_rect = pygame.Rect(sidebar_x + (sidebar_width - badge_width) // 2, 65, badge_width, 25)
        pygame.draw.rect(screen, BLUE, badge_rect, border_radius=12)
        pygame.draw.rect(screen, LIGHT_GRAY, badge_rect, 1, border_radius=12)
        screen.blit(spectator_badge, (badge_rect.x + 10, badge_rect.y + 4))

        # Show spectator name if provided
        if spectator_name:
            spectator_text = small_font.render(f"Viewing as: {spectator_name}", True, LIGHT_GRAY)
            spectator_rect = spectator_text.get_rect(center=(sidebar_x + sidebar_width // 2, 100))
            screen.blit(spectator_text, spectator_rect)
    else:
        # Draw player info with icons
        player_y = 70

        # White player (circle icon)
        white_icon_rect = pygame.Rect(sidebar_x + 40, player_y, 20, 20)
        pygame.draw.circle(screen, WHITE, white_icon_rect.center, 10)
        pygame.draw.circle(screen, GRAY, white_icon_rect.center, 10, 1)

        white_text = font.render(f"You: {game.white_player_name if player_color == 'white' else game.black_player_name}",
                               True, WHITE)
        screen.blit(white_text, (sidebar_x + 65, player_y - 2))

        # Black player (circle icon)
        black_icon_rect = pygame.Rect(sidebar_x + 40, player_y + 30, 20, 20)
        pygame.draw.circle(screen, BLACK, black_icon_rect.center, 10)
        pygame.draw.circle(screen, LIGHT_GRAY, black_icon_rect.center, 10, 1)

        black_text = font.render(f"Opponent: {game.black_player_name if player_color == 'white' else game.white_player_name}",
                               True, LIGHT_GRAY)
        screen.blit(black_text, (sidebar_x + 65, player_y + 28))

    # Draw turn info with visual indicator
    if player_color == 'spectator':
        # For spectators, just show whose turn it is without the green/red indicator
        turn_y = 185
        turn_text = header_font.render(f"Turn: {game.turn.capitalize()}", True, WHITE)
        screen.blit(turn_text, (sidebar_x + 20, turn_y))
    else:
        # For players, show turn with color indicator
        turn_y = 125
        turn_color = GREEN if game.turn == player_color else RED

        # Draw animated turn indicator
        current_time = pygame.time.get_ticks() / 1000
        pulse_size = 12 + math.sin(current_time * 4) * 2  # Pulsing effect

        turn_indicator_rect = pygame.Rect(sidebar_x + 40, turn_y, 25, 25)
        pygame.draw.circle(screen, turn_color, turn_indicator_rect.center, pulse_size)
        pygame.draw.circle(screen, LIGHT_GRAY, turn_indicator_rect.center, pulse_size, 1)

        turn_text = header_font.render(f"Turn: {game.turn.capitalize()}", True, WHITE)
        screen.blit(turn_text, (sidebar_x + 95, turn_y + 2))

    # Draw status with styled box
    if player_color == 'spectator':
        status_y = 215
    else:
        status_y = 165

    status_rect = pygame.Rect(sidebar_x + 20, status_y, sidebar_width - 40, 30)

    # Change background color based on game status
    status_bg_color = (50, 50, 70)  # Default dark blue

    # Determine status text and colors
    status_text_color = WHITE
    if game.status == "in_progress":
        status_display = "In Progress"
        # Check if any player is in check
        if hasattr(game, 'is_in_check'):
            if game.is_in_check('white'):
                status_display = "White in Check!"
                status_text_color = (255, 100, 100)  # Red for check
                status_bg_color = (70, 40, 40)  # Darker red background
            elif game.is_in_check('black'):
                status_display = "Black in Check!"
                status_text_color = (255, 100, 100)  # Red for check
                status_bg_color = (70, 40, 40)  # Darker red background
    elif "wins" in game.status:
        winner = game.status.split("_")[0].capitalize()
        status_display = f"{winner} Wins!"
        status_text_color = (100, 255, 100)  # Green for win
        status_bg_color = (40, 70, 40)  # Darker green background
    elif game.status == "stalemate":
        status_display = "Stalemate - Draw"
        status_text_color = (255, 255, 100)  # Yellow for draw
        status_bg_color = (70, 70, 40)  # Darker yellow background
    else:
        status_display = game.status.replace('_', ' ').title()

    # Draw status background with appropriate color
    pygame.draw.rect(screen, status_bg_color, status_rect, border_radius=5)
    pygame.draw.rect(screen, LIGHT_GRAY, status_rect, 1, border_radius=5)

    # Draw status text
    status_text = font.render(f"Status: {status_display}", True, status_text_color)
    status_text_rect = status_text.get_rect(center=status_rect.center)
    screen.blit(status_text, status_text_rect)

    # Draw game log section
    log_section_y = 250
    log_header = header_font.render("Game Log", True, GOLD)
    log_header_rect = log_header.get_rect(center=(sidebar_x + sidebar_width // 2, log_section_y))
    screen.blit(log_header, log_header_rect)

    # Draw game log background
    log_bg_rect = pygame.Rect(sidebar_x + 20, log_section_y + 25,
                             sidebar_width - 40, 80)
    pygame.draw.rect(screen, (20, 20, 30), log_bg_rect, border_radius=5)
    pygame.draw.rect(screen, GRAY, log_bg_rect, 1, border_radius=5)

    # Draw game log messages
    y_offset = log_section_y + 35
    for message in game.messages[-3:]:  # Show last 3 game messages
        sender = message['sender']
        text = message['text']

        # Handle long messages with word wrapping
        available_width = sidebar_width - 60

        # Render the full message with sender
        message_text = font.render(f"{sender}: {text}", True, LIGHT_GRAY)

        # If message is too long, truncate with ellipsis
        if message_text.get_width() > available_width:
            # Try different lengths until it fits
            for length in range(len(text), 0, -1):
                test_text = font.render(f"{sender}: {text[:length]}...", True, LIGHT_GRAY)
                if test_text.get_width() <= available_width:
                    message_text = test_text
                    break

        message_rect = message_text.get_rect(x=sidebar_x + 30, y=y_offset)
        screen.blit(message_text, message_rect)
        y_offset += 25

    # Check if chat should be enabled
    # Disable chat if: 1) Playing against bot, 2) Game is over, or 3) Chat server is offline
    chat_disabled = is_bot_game or game.status != "in_progress"
    chat_disabled_reason = ""

    if is_bot_game:
        chat_disabled_reason = "Chat is disabled when\nplaying against bot"
    elif game.status != "in_progress":
        chat_disabled_reason = "Chat is disabled when\nthe game is over"

    if not chat_disabled:
        # Draw chat section
        chat_section_y = log_section_y + 120
        chat_header = header_font.render("Chat", True, GOLD)
        chat_header_rect = chat_header.get_rect(center=(sidebar_x + sidebar_width // 2, chat_section_y))
        screen.blit(chat_header, chat_header_rect)

        # Draw online status indicator
        status_x = sidebar_x + sidebar_width - 30
        status_y = chat_section_y
        status_color = (50, 200, 50)  # Green for online

        # Draw "ONLINE" text
        status_text = small_font.render("ONLINE", True, status_color)
        screen.blit(status_text, (status_x - status_text.get_width() - 5, status_y - 7))

        # Draw status dot
        pygame.draw.circle(screen, status_color, (status_x, status_y), 5)
        pygame.draw.circle(screen, LIGHT_GRAY, (status_x, status_y), 5, 1)

        # Draw chat area background
        chat_bg_rect = pygame.Rect(sidebar_x + 20, chat_section_y + 25,
                                sidebar_width - 40, window_height - chat_section_y - 80)
        pygame.draw.rect(screen, (20, 20, 30), chat_bg_rect, border_radius=5)
        pygame.draw.rect(screen, GRAY, chat_bg_rect, 1, border_radius=5)

        # Draw chat messages
        y_offset = chat_section_y + 35
        for message in game.chat_messages[-8:]:  # Show last 8 chat messages
            sender = message['sender']
            text = message['text']

            # Different colors for different senders
            if sender == "System":
                sender_color = GOLD
            elif sender == game.white_player_name:
                sender_color = WHITE
            elif sender == game.black_player_name:
                sender_color = LIGHT_GRAY
            else:
                sender_color = BLUE

            # Render sender name
            sender_text = small_font.render(f"{sender}:", True, sender_color)

            # Calculate available width for message text
            available_width = (sidebar_width - 60) - sender_text.get_width()

            # Handle long messages with word wrapping
            words = text.split()
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + " " + word if current_line else word
                test_text = small_font.render(test_line, True, LIGHT_GRAY)

                if test_text.get_width() <= available_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

            # If no lines were created (rare case), add the text as is
            if not lines:
                lines = [text]

            # Render the sender name
            screen.blit(sender_text, (sidebar_x + 30, y_offset))

            # Render first line next to sender
            if lines:
                first_line_text = small_font.render(lines[0], True, LIGHT_GRAY)
                screen.blit(first_line_text, (sidebar_x + 30 + sender_text.get_width() + 5, y_offset))
                y_offset += 20

                # Render additional lines with proper indentation
                for i in range(1, len(lines)):
                    line_text = small_font.render(lines[i], True, LIGHT_GRAY)
                    screen.blit(line_text, (sidebar_x + 30 + sender_text.get_width() + 5, y_offset))
                    y_offset += 20
            else:
                y_offset += 20

        # Draw chat input box
        chat_input_rect = pygame.Rect(sidebar_x + 20, window_height - 50,
                                    sidebar_width - 40, 40)  # Full width

        # Draw input background
        pygame.draw.rect(screen, WHITE, chat_input_rect, border_radius=5)

        # Draw border - highlighted when typing
        border_color = BLUE if is_typing else GRAY
        pygame.draw.rect(screen, border_color, chat_input_rect, 2, border_radius=5)

        # Draw input text or placeholder
        if chat_input:
            input_text = font.render(chat_input, True, BLACK)
            input_rect = input_text.get_rect(x=sidebar_x + 30, centery=window_height - 30)
            screen.blit(input_text, input_rect)

            # Draw cursor when typing
            if is_typing and (pygame.time.get_ticks() // 500) % 2 == 0:  # Blink every 0.5 seconds
                cursor_x = sidebar_x + 30 + input_text.get_width() + 2
                pygame.draw.line(screen, BLACK, (cursor_x, window_height - 45),
                            (cursor_x, window_height - 15), 2)
        else:
            placeholder_text = small_font.render("Type your message here...", True, GRAY)
            placeholder_rect = placeholder_text.get_rect(x=sidebar_x + 30, centery=window_height - 30)
            screen.blit(placeholder_text, placeholder_rect)




    else:
        # Draw a message about chat being disabled
        info_y = log_section_y + 150

        # Split the reason into lines
        reason_lines = chat_disabled_reason.split('\n')

        for i, line in enumerate(reason_lines):
            info_text = header_font.render(line, True, LIGHT_GRAY)
            info_rect = info_text.get_rect(center=(sidebar_x + sidebar_width // 2, info_y + i * 30))
            screen.blit(info_text, info_rect)

def draw_enhanced_highlight(screen, pos, board_x, board_y, square_size, valid_moves=None, board=None):
    """Draw an enhanced highlight for selected pieces and valid moves"""
    row, col = pos
    x = board_x + col * square_size
    y = board_y + row * square_size

    # Create a pulsing effect
    current_time = pygame.time.get_ticks() / 1000
    alpha = int(150 + 50 * math.sin(current_time * 4))  # Pulsing transparency

    # Create highlight surface with transparency
    highlight_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
    highlight_color = (255, 255, 0, alpha)  # Yellow with pulsing alpha
    highlight_surface.fill(highlight_color)

    # Draw highlight for selected piece
    screen.blit(highlight_surface, (x, y))

    # Draw corner indicators
    corner_size = 10
    corner_color = GOLD
    line_width = 2

    # Top-left corner
    pygame.draw.line(screen, corner_color, (x, y), (x + corner_size, y), line_width)
    pygame.draw.line(screen, corner_color, (x, y), (x, y + corner_size), line_width)

    # Top-right corner
    pygame.draw.line(screen, corner_color, (x + square_size, y), (x + square_size - corner_size, y), line_width)
    pygame.draw.line(screen, corner_color, (x + square_size, y), (x + square_size, y + corner_size), line_width)

    # Bottom-left corner
    pygame.draw.line(screen, corner_color, (x, y + square_size), (x + corner_size, y + square_size), line_width)
    pygame.draw.line(screen, corner_color, (x, y + square_size), (x, y + square_size - corner_size), line_width)

    # Bottom-right corner
    pygame.draw.line(screen, corner_color, (x + square_size, y + square_size),
                   (x + square_size - corner_size, y + square_size), line_width)
    pygame.draw.line(screen, corner_color, (x + square_size, y + square_size),
                   (x + square_size, y + square_size - corner_size), line_width)

    # Draw valid moves if provided
    if valid_moves:
        for move_row, move_col in valid_moves:
            move_x = board_x + move_col * square_size
            move_y = board_y + move_row * square_size

            # Check if there's a piece at this position (capture)
            is_capture = False
            if board and 0 <= move_row < len(board) and 0 <= move_col < len(board[0]):
                is_capture = board[move_row][move_col] is not None

            # Draw different indicators for empty squares vs. captures
            if is_capture:
                # Draw a capture indicator (red circle)
                capture_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                capture_color = (220, 60, 60, 120)  # Semi-transparent red
                pygame.draw.rect(capture_surface, capture_color, (0, 0, square_size, square_size))
                screen.blit(capture_surface, (move_x, move_y))

                # Draw a border
                pygame.draw.rect(screen, (220, 60, 60),
                               (move_x, move_y, square_size, square_size), 2)
            else:
                # Draw a move indicator (green circle)
                move_radius = square_size // 4
                move_alpha = int(100 + 50 * math.sin(current_time * 4))  # Pulsing transparency
                move_color = (60, 200, 60, move_alpha)  # Semi-transparent green

                # Create a surface for the move indicator
                move_surface = pygame.Surface((move_radius*2, move_radius*2), pygame.SRCALPHA)
                pygame.draw.circle(move_surface, move_color, (move_radius, move_radius), move_radius)

                # Blit to the center of the square
                screen.blit(move_surface, (
                    move_x + square_size//2 - move_radius,
                    move_y + square_size//2 - move_radius
                ))

def draw_enhanced_button(screen, rect, text, font, is_hovered=False):
    """Draw an enhanced button for the chess game"""
    x, y, width, height = rect

    # Base colors - classic black-and-white theme
    bg_color = (30, 30, 30)
    border_color = (150, 150, 150) if not is_hovered else (255, 255, 255)
    text_color = (240, 240, 240)

    # Draw button background with rounded corners
    pygame.draw.rect(screen, bg_color, rect, border_radius=10)

    # Draw border - thicker when hovered
    border_width = 2 if not is_hovered else 3
    pygame.draw.rect(screen, border_color, rect, border_width, border_radius=10)

    # Draw chess pattern on the sides
    pattern_rect_left = (x + 5, y + 5, 10, height - 10)
    pattern_rect_right = (x + width - 15, y + 5, 10, height - 10)

    # Draw mini chess patterns with classic black-and-white color scheme
    square_size = 5
    for row in range((height - 10) // square_size):
        for col in range(10 // square_size):
            # Left pattern
            left_color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
            pygame.draw.rect(screen, left_color, (
                pattern_rect_left[0] + col * square_size,
                pattern_rect_left[1] + row * square_size,
                square_size, square_size
            ))

            # Right pattern
            right_color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
            pygame.draw.rect(screen, right_color, (
                pattern_rect_right[0] + col * square_size,
                pattern_rect_right[1] + row * square_size,
                square_size, square_size
            ))

    # Draw text - slightly larger when hovered
    text_size = 1.05 if is_hovered else 1.0
    text_surf = font.render(text, True, text_color)
    if is_hovered:
        # Scale text slightly larger when hovered
        original_size = text_surf.get_size()
        new_size = (int(original_size[0] * text_size), int(original_size[1] * text_size))
        text_surf = pygame.transform.scale(text_surf, new_size)

    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)

    # Add glow effect when hovered
    if is_hovered:
        # Create a surface with per-pixel alpha for the glow
        glow_size = 5
        glow_surface = pygame.Surface((width + glow_size * 2, height + glow_size * 2), pygame.SRCALPHA)

        # Draw the glow with white color and transparency for classic black-and-white theme
        pygame.draw.rect(
            glow_surface,
            (255, 255, 255, 30),  # White with transparency
            (0, 0, width + glow_size * 2, height + glow_size * 2),
            border_radius=15
        )

        # Blit the glow surface
        screen.blit(glow_surface, (x - glow_size, y - glow_size))

class EnhancedButton:
    """Enhanced button class for the chess game"""
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False

    def draw(self, screen, font):
        draw_enhanced_button(screen, self.rect, self.text, font, self.is_hovered)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.action:
            return self.action
        return None
