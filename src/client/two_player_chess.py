"""
Enhanced Two-Player Chess Game with Pygame and Chat

Usage:
- python two_player_chess.py                                    # Interactive menu
- python two_player_chess.py white [game_id] [player_name]      # Play as white
- python two_player_chess.py black [game_id] [player_name]      # Play as black
- python two_player_chess.py spectator [game_id] [player_name]  # Spectate game
- python two_player_chess.py white [game_id] [player_name] --bot [difficulty]  # Play vs AI

If no arguments are provided, an interactive menu will be shown.
"""
import pygame
import sys
import os
import json
import time
import math
import uuid
import argparse
from .chess_client import get_client
from ..utils.chess_game_assets import (
    draw_enhanced_board,
    draw_enhanced_sidebar,
    draw_enhanced_highlight,
    EnhancedButton
)
from ..utils.enhanced_chess_pieces import create_enhanced_piece_images
from ..utils.chess_bot import ChessBot

# Initialize pygame
pygame.init()

# Set window size (not fullscreen, matching screenshot)
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 600

# Calculate board size - make it match the screenshot
SQUARE_SIZE = 65  # Adjusted square size to fit the height
BOARD_SIZE = 8
BOARD_WIDTH = BOARD_SIZE * SQUARE_SIZE
SIDEBAR_WIDTH = 300  # Adjusted sidebar width
FPS = 60

# Calculate board position to center it
BOARD_X_OFFSET = (WINDOW_WIDTH - SIDEBAR_WIDTH - BOARD_WIDTH) // 2
BOARD_Y_OFFSET = (WINDOW_HEIGHT - BOARD_WIDTH) // 2

# Set window icon with classic black-and-white color scheme
icon = pygame.Surface((32, 32), pygame.SRCALPHA)
pygame.draw.rect(icon, (255, 255, 255), (0, 0, 16, 16))  # White
pygame.draw.rect(icon, (0, 0, 0), (16, 0, 16, 16))       # Black
pygame.draw.rect(icon, (0, 0, 0), (0, 16, 16, 16))       # Black
pygame.draw.rect(icon, (255, 255, 255), (16, 16, 16, 16))  # White
pygame.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (255, 255, 255)  # White for light squares
DARK_SQUARE = (0, 0, 0)         # Black for dark squares
HIGHLIGHT = (102, 205, 170, 150)  # Seafoam green highlight
GRAY = (80, 80, 80)
DARK_GRAY = (40, 40, 60)        # Slightly bluish dark gray
LIGHT_GRAY = (220, 220, 220)
RED = (220, 60, 60)             # Softer red
GREEN = (60, 200, 60)           # Softer green
BLUE = (60, 120, 255)           # Brighter blue
GOLD = (212, 175, 55)           # More natural gold
BUTTON_COLOR = (70, 130, 180)   # Steel Blue
BUTTON_HOVER_COLOR = (100, 149, 237)  # Cornflower Blue
CREAM = (255, 253, 208)         # Cream color for text contrast

# Piece types and colors
PIECE_TYPES = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
COLORS = ['white', 'black']

# File for sharing game state
GAME_STATE_FILE_TEMPLATE = "../../data/game_states/chess_game_state_{}.json"

# Fonts
title_font = pygame.font.SysFont('Arial', 28, bold=True)
header_font = pygame.font.SysFont('Arial', 18, bold=True)
font = pygame.font.SysFont('Arial', 16)
small_font = pygame.font.SysFont('Arial', 14)

# Button class for interactive UI elements
class Button:
    def __init__(self, x, y, width, height, text, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, text_color=WHITE, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action
        self.is_hovered = False

    def draw(self, screen):
        # Draw button with hover effect
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, LIGHT_GRAY, self.rect, 2, border_radius=10)  # Border

        # Draw text
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        # Update hover state
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        # Check if button was clicked
        if self.rect.collidepoint(mouse_pos) and self.action:
            return self.action
        return None

# Game state
class ChessGame:
    def __init__(self, game_id=None, player_name=None):
        self.game_id = game_id if game_id else str(uuid.uuid4())
        self.board = self.create_initial_board()
        self.selected_piece = None
        self.valid_moves = []  # Store valid moves for the selected piece
        self.turn = 'white'
        self.status = 'in_progress'
        self.messages = []
        self.chat_messages = []
        self.last_update = time.time()
        self.white_player_name = player_name if player_name else "White Player"
        self.black_player_name = "Waiting for opponent..."
        self.add_message("System", "Welcome to Chess!")
        self.add_chat("System", "Chat enabled. Type messages below to communicate with your opponent.")

    def reset_game(self):
        """Reset the game to initial state"""
        self.board = self.create_initial_board()
        self.selected_piece = None
        self.valid_moves = []
        self.turn = 'white'
        self.status = 'in_progress'
        self.last_update = time.time()
        self.add_message("System", "Game has been reset!")
        self.add_chat("System", "New game started! Chat is enabled for this game.")

    def clean_expired_messages(self):
        """Remove chat messages that have expired"""
        # Removed disappearing message expiration functionality
        pass

    def set_black_player(self, player_name):
        """Set the black player name when they join"""
        self.black_player_name = player_name
        self.add_message("System", f"{player_name} has joined as Black!")
        self.add_chat("System", f"{player_name} has joined the game.")

    def create_initial_board(self):
        """Create the initial chess board"""
        board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # Set up pawns
        for col in range(BOARD_SIZE):
            board[1][col] = {'type': 'pawn', 'color': 'black'}
            board[6][col] = {'type': 'pawn', 'color': 'white'}

        # Set up other pieces for black
        board[0][0] = {'type': 'rook', 'color': 'black'}
        board[0][1] = {'type': 'knight', 'color': 'black'}
        board[0][2] = {'type': 'bishop', 'color': 'black'}
        board[0][3] = {'type': 'queen', 'color': 'black'}
        board[0][4] = {'type': 'king', 'color': 'black'}
        board[0][5] = {'type': 'bishop', 'color': 'black'}
        board[0][6] = {'type': 'knight', 'color': 'black'}
        board[0][7] = {'type': 'rook', 'color': 'black'}

        # Set up other pieces for white
        board[7][0] = {'type': 'rook', 'color': 'white'}
        board[7][1] = {'type': 'knight', 'color': 'white'}
        board[7][2] = {'type': 'bishop', 'color': 'white'}
        board[7][3] = {'type': 'queen', 'color': 'white'}
        board[7][4] = {'type': 'king', 'color': 'white'}
        board[7][5] = {'type': 'bishop', 'color': 'white'}
        board[7][6] = {'type': 'knight', 'color': 'white'}
        board[7][7] = {'type': 'rook', 'color': 'white'}

        return board

    def add_message(self, sender, text):
        """Add a message to the game log"""
        self.messages.append({'sender': sender, 'text': text})
        if len(self.messages) > 10:
            self.messages.pop(0)

    def add_chat(self, sender, text):
        """Add a message to the chat

        Args:
            sender: Name of the message sender
            text: Content of the message
        """
        self.chat_messages.append({
            'sender': sender,
            'text': text,
            'time': time.time()
        })
        if len(self.chat_messages) > 20:
            self.chat_messages.pop(0)

    def get_valid_moves(self, pos):
        """Get all valid moves for a piece at the given position"""
        row, col = pos
        piece = self.board[row][col]

        if not piece:
            return []

        valid_moves = []
        piece_type = piece['type']
        color = piece['color']

        # Pawn movement
        if piece_type == 'pawn':
            # Direction depends on color
            direction = -1 if color == 'white' else 1

            # Forward move (1 square)
            new_row = row + direction
            if 0 <= new_row < BOARD_SIZE and not self.board[new_row][col]:
                valid_moves.append((new_row, col))

                # Initial two-square move
                if (color == 'white' and row == 6) or (color == 'black' and row == 1):
                    new_row = row + 2 * direction
                    if 0 <= new_row < BOARD_SIZE and not self.board[new_row][col] and not self.board[row + direction][col]:
                        valid_moves.append((new_row, col))

            # Diagonal captures
            for offset in [-1, 1]:
                new_col = col + offset
                new_row = row + direction
                if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                    target = self.board[new_row][new_col]
                    if target and target['color'] != color:
                        valid_moves.append((new_row, new_col))

        # Rook movement (horizontal and vertical)
        elif piece_type == 'rook':
            # Check in all four directions (up, right, down, left)
            directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            for dr, dc in directions:
                for i in range(1, BOARD_SIZE):
                    new_row, new_col = row + i * dr, col + i * dc

                    # Check if position is on the board
                    if not (0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE):
                        break

                    target = self.board[new_row][new_col]
                    if not target:
                        valid_moves.append((new_row, new_col))
                    elif target['color'] != color:
                        valid_moves.append((new_row, new_col))
                        break
                    else:
                        break

        # Knight movement (L-shape)
        elif piece_type == 'knight':
            knight_moves = [
                (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)
            ]

            for dr, dc in knight_moves:
                new_row, new_col = row + dr, col + dc

                # Check if position is on the board
                if not (0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE):
                    continue

                target = self.board[new_row][new_col]
                if not target or target['color'] != color:
                    valid_moves.append((new_row, new_col))

        # Bishop movement (diagonal)
        elif piece_type == 'bishop':
            # Check in all four diagonal directions
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                for i in range(1, BOARD_SIZE):
                    new_row, new_col = row + i * dr, col + i * dc

                    # Check if position is on the board
                    if not (0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE):
                        break

                    target = self.board[new_row][new_col]
                    if not target:
                        valid_moves.append((new_row, new_col))
                    elif target['color'] != color:
                        valid_moves.append((new_row, new_col))
                        break
                    else:
                        break

        # Queen movement (combination of rook and bishop)
        elif piece_type == 'queen':
            # Check in all eight directions
            directions = [
                (-1, 0), (0, 1), (1, 0), (0, -1),  # Horizontal and vertical
                (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
            ]

            for dr, dc in directions:
                for i in range(1, BOARD_SIZE):
                    new_row, new_col = row + i * dr, col + i * dc

                    # Check if position is on the board
                    if not (0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE):
                        break

                    target = self.board[new_row][new_col]
                    if not target:
                        valid_moves.append((new_row, new_col))
                    elif target['color'] != color:
                        valid_moves.append((new_row, new_col))
                        break
                    else:
                        break

        # King movement (one square in any direction)
        elif piece_type == 'king':
            # Check all eight surrounding squares
            directions = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),           (0, 1),
                (1, -1),  (1, 0),  (1, 1)
            ]

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc

                # Check if position is on the board
                if not (0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE):
                    continue

                target = self.board[new_row][new_col]
                if not target or target['color'] != color:
                    valid_moves.append((new_row, new_col))

        return valid_moves

    def is_valid_move(self, from_pos, to_pos, player_color):
        """Check if a move is valid"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # Check if positions are on the board
        if not (0 <= from_row < BOARD_SIZE and 0 <= from_col < BOARD_SIZE and
                0 <= to_row < BOARD_SIZE and 0 <= to_col < BOARD_SIZE):
            return False

        # Check if there's a piece at the from position
        piece = self.board[from_row][from_col]
        if not piece:
            return False

        # Check if it's the piece's turn and color
        if piece['color'] != self.turn or piece['color'] != player_color:
            return False

        # Check if the destination has a piece of the same color
        dest_piece = self.board[to_row][to_col]
        if dest_piece and dest_piece['color'] == piece['color']:
            return False

        # Get valid moves for the piece and check if the destination is among them
        valid_moves = self.get_valid_moves(from_pos)
        return (to_row, to_col) in valid_moves

    def find_king(self, color):
        """Find the position of the king of the given color"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece['type'] == 'king' and piece['color'] == color:
                    return (row, col)
        return None  # Should never happen in a valid chess game

    def is_square_under_attack(self, pos, attacking_color):
        """Check if a square is under attack by any piece of the given color"""
        row, col = pos

        # Check attacks from pawns
        pawn_direction = 1 if attacking_color == 'white' else -1
        for offset in [-1, 1]:
            attack_row = row + pawn_direction
            attack_col = col + offset
            if 0 <= attack_row < BOARD_SIZE and 0 <= attack_col < BOARD_SIZE:
                piece = self.board[attack_row][attack_col]
                if piece and piece['type'] == 'pawn' and piece['color'] == attacking_color:
                    return True

        # Check attacks from knights
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in knight_moves:
            attack_row, attack_col = row + dr, col + dc
            if 0 <= attack_row < BOARD_SIZE and 0 <= attack_col < BOARD_SIZE:
                piece = self.board[attack_row][attack_col]
                if piece and piece['type'] == 'knight' and piece['color'] == attacking_color:
                    return True

        # Check attacks from kings (for adjacent squares)
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        for dr, dc in king_moves:
            attack_row, attack_col = row + dr, col + dc
            if 0 <= attack_row < BOARD_SIZE and 0 <= attack_col < BOARD_SIZE:
                piece = self.board[attack_row][attack_col]
                if piece and piece['type'] == 'king' and piece['color'] == attacking_color:
                    return True

        # Check attacks from rooks, bishops, and queens (along lines)
        # Rook directions (horizontal and vertical)
        rook_directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        # Bishop directions (diagonal)
        bishop_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Check all directions
        for dr, dc in rook_directions + bishop_directions:
            for i in range(1, BOARD_SIZE):
                attack_row, attack_col = row + i * dr, col + i * dc

                # Check if position is on the board
                if not (0 <= attack_row < BOARD_SIZE and 0 <= attack_col < BOARD_SIZE):
                    break

                piece = self.board[attack_row][attack_col]
                if piece:
                    if piece['color'] == attacking_color:
                        # Check if this piece can attack along this direction
                        can_attack = False
                        if piece['type'] == 'queen':
                            can_attack = True
                        elif piece['type'] == 'rook' and (dr, dc) in rook_directions:
                            can_attack = True
                        elif piece['type'] == 'bishop' and (dr, dc) in bishop_directions:
                            can_attack = True

                        if can_attack:
                            return True
                    # If we hit any piece (even our own), we can't go further in this direction
                    break

        return False

    def is_in_check(self, color):
        """Check if the king of the given color is in check"""
        king_pos = self.find_king(color)
        if not king_pos:
            return False  # Should never happen

        # The opposing color
        opposing_color = 'black' if color == 'white' else 'white'

        # Check if the king's position is under attack
        return self.is_square_under_attack(king_pos, opposing_color)

    def would_move_cause_check(self, from_pos, to_pos, color):
        """Check if making a move would put or leave the king in check"""
        # Make a temporary move
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # Save the current state
        original_piece = self.board[from_row][from_col]
        captured_piece = self.board[to_row][to_col]

        # Make the move temporarily
        self.board[to_row][to_col] = original_piece
        self.board[from_row][from_col] = None

        # Check if the king is in check after the move
        in_check = self.is_in_check(color)

        # Restore the board
        self.board[from_row][from_col] = original_piece
        self.board[to_row][to_col] = captured_piece

        return in_check

    def get_all_valid_moves_for_color(self, color):
        """Get all valid moves for all pieces of the given color"""
        all_moves = []

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece['color'] == color:
                    from_pos = (row, col)
                    # Get all potential moves for this piece
                    potential_moves = self.get_valid_moves(from_pos)

                    # Filter out moves that would leave the king in check
                    for to_pos in potential_moves:
                        if not self.would_move_cause_check(from_pos, to_pos, color):
                            all_moves.append((from_pos, to_pos))

        return all_moves

    def is_checkmate(self, color):
        """Check if the given color is in checkmate"""
        # First, check if the king is in check
        if not self.is_in_check(color):
            return False

        # If in check, see if there are any valid moves that can get out of check
        return len(self.get_all_valid_moves_for_color(color)) == 0

    def is_stalemate(self, color):
        """Check if the given color is in stalemate"""
        # First, check if the king is NOT in check
        if self.is_in_check(color):
            return False

        # If not in check, see if there are any valid moves
        return len(self.get_all_valid_moves_for_color(color)) == 0

    def make_move(self, from_pos, to_pos, player_color):
        """Make a move on the board"""
        if not self.is_valid_move(from_pos, to_pos, player_color):
            return False

        # Check if this move would leave the king in check
        if self.would_move_cause_check(from_pos, to_pos, player_color):
            self.add_message("System", "Invalid move: would leave your king in check")
            return False

        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # Get the piece and update its position
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]

        # Update the board
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None

        # Add message about the move
        move_text = f"{piece['color']} {piece['type']} moved from ({from_row},{from_col}) to ({to_row},{to_col})"
        if captured:
            move_text += f", capturing {captured['color']} {captured['type']}"
        self.add_message("System", move_text)

        # Switch turns
        next_color = 'black' if player_color == 'white' else 'white'
        self.turn = next_color

        # Check for check, checkmate, or stalemate
        if self.is_in_check(next_color):
            if self.is_checkmate(next_color):
                self.status = f"{player_color}_wins"
                self.add_message("System", f"Checkmate! {player_color.capitalize()} wins!")
                # Disable chat when game ends
                self.add_chat("System", "Game has ended. Chat is now disabled.")
            else:
                self.add_message("System", f"{next_color.capitalize()} is in check!")
        elif self.is_stalemate(next_color):
            self.status = "stalemate"
            self.add_message("System", "Stalemate! The game is a draw.")
            # Disable chat when game ends
            self.add_chat("System", "Game has ended. Chat is now disabled.")

        # Update timestamp
        self.last_update = time.time()

        return True

    def to_dict(self):
        """Convert game state to dictionary"""
        return {
            'game_id': self.game_id,
            'board': self.board,
            'turn': self.turn,
            'status': self.status,
            'messages': self.messages,
            'chat_messages': self.chat_messages,
            'last_update': self.last_update,
            'white_player_name': self.white_player_name,
            'black_player_name': self.black_player_name
        }

    def from_dict(self, data):
        """Update game state from dictionary"""
        self.game_id = data.get('game_id', self.game_id)
        self.board = data['board']
        self.turn = data['turn']
        self.status = data['status']
        self.messages = data['messages']
        self.last_update = data['last_update']

        # Handle player names
        self.white_player_name = data.get('white_player_name', "White Player")
        self.black_player_name = data.get('black_player_name', "Black Player")

        # Handle chat messages (for backward compatibility)
        if 'chat_messages' in data:
            # Preserve existing chat messages if we're loading
            self.chat_messages = data['chat_messages']

def save_game_state(game):
    """Save game state using the network client"""
    try:
        # Get the client instance
        client = get_client()

        # If we're connected to the server, send the move
        if client.connected and client.game_id:
            # The actual saving happens on the server side
            return True

        # Fallback to file-based saving if not connected
        os.makedirs(os.path.dirname("game_states/"), exist_ok=True)
        game_state_file = GAME_STATE_FILE_TEMPLATE.format(game.game_id)
        with open(game_state_file, 'w') as f:
            json.dump(game.to_dict(), f)
        return True
    except Exception as e:
        print(f"Error saving game state: {e}")
        return False

def load_game_state(game, player_color=None, preserve_player_name=True):
    """Load game state from server or file"""
    try:
        # Get the client instance
        client = get_client()

        # If we're connected to the server, request the latest state
        if client.connected and client.game_id:
            client.request_game_state()

            # The game state will be updated via callback
            # For now, use the client's cached state if available
            if client.game_state:
                # Save current player name if needed
                original_player_name = None
                if preserve_player_name and player_color:
                    if player_color == 'white':
                        original_player_name = game.white_player_name
                    elif player_color == 'black':
                        original_player_name = game.black_player_name

                # Update game from client state
                game.from_dict(client.game_state)

                # Restore player name if needed
                if preserve_player_name and player_color and original_player_name and original_player_name != "Waiting for opponent...":
                    if player_color == 'white':
                        game.white_player_name = original_player_name
                    elif player_color == 'black':
                        game.black_player_name = original_player_name

                return True

        # Fallback to file-based loading if not connected
        game_state_file = GAME_STATE_FILE_TEMPLATE.format(game.game_id)
        if os.path.exists(game_state_file):
            # Save current player name if needed
            original_player_name = None
            if preserve_player_name and player_color:
                if player_color == 'white':
                    original_player_name = game.white_player_name
                elif player_color == 'black':
                    original_player_name = game.black_player_name

            # Load game state
            with open(game_state_file, 'r') as f:
                data = json.load(f)
                game.from_dict(data)

            # Restore player name if needed
            if preserve_player_name and player_color and original_player_name and original_player_name != "Waiting for opponent...":
                if player_color == 'white':
                    game.white_player_name = original_player_name
                elif player_color == 'black':
                    game.black_player_name = original_player_name

            return True
        return False
    except Exception as e:
        print(f"Error loading game state: {e}")
        return False

def handle_game_update(message_type, game_state):
    """Callback function for game state updates from the server"""
    if not game_state:
        return

    # This function will be called when the server sends a game state update
    # We'll update our local game state in the main game loop

# Create piece images
def create_piece_images():
    """Create enhanced 3D-looking chess piece images"""
    images = {}

    for color in COLORS:
        for piece_type in PIECE_TYPES:
            # Create a surface
            surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)

            # Fill with transparent background
            surface.fill((0, 0, 0, 0))

            # Base colors
            if color == 'white':
                main_color = (240, 240, 240)  # White
                highlight_color = (255, 255, 255)  # Pure white for highlights
                shadow_color = (180, 180, 180)  # Light gray for shadows
                outline_color = (30, 30, 30)  # Dark outline
                detail_color = (50, 50, 50)  # Dark details
            else:
                main_color = (40, 40, 40)  # Black
                highlight_color = (80, 80, 80)  # Dark gray for highlights
                shadow_color = (20, 20, 20)  # Very dark gray for shadows
                outline_color = (200, 200, 200)  # Light outline
                detail_color = (180, 180, 180)  # Light details

            # Center coordinates
            cx, cy = SQUARE_SIZE // 2, SQUARE_SIZE // 2

            # Draw different 3D-looking pieces
            if piece_type == 'pawn':
                # Base
                pygame.draw.ellipse(surface, shadow_color, (cx-12, cy+10, 24, 10))

                # Stem
                pygame.draw.rect(surface, main_color, (cx-5, cy-5, 10, 20), border_radius=2)
                pygame.draw.rect(surface, highlight_color, (cx-5, cy-5, 5, 20), border_radius=2)

                # Head
                pygame.draw.circle(surface, main_color, (cx, cy-12), 10)
                pygame.draw.circle(surface, highlight_color, (cx-3, cy-14), 7)

                # Outline
                pygame.draw.ellipse(surface, outline_color, (cx-12, cy+10, 24, 10), 1)
                pygame.draw.rect(surface, outline_color, (cx-5, cy-5, 10, 20), 1, border_radius=2)
                pygame.draw.circle(surface, outline_color, (cx, cy-12), 10, 1)

            elif piece_type == 'rook':
                # Base
                pygame.draw.ellipse(surface, shadow_color, (cx-15, cy+10, 30, 10))

                # Main body
                pygame.draw.rect(surface, main_color, (cx-12, cy-15, 24, 30), border_radius=2)
                pygame.draw.rect(surface, highlight_color, (cx-12, cy-15, 12, 30), border_radius=2)

                # Castle top
                for i in range(3):
                    x_offset = -12 + i*12
                    pygame.draw.rect(surface, main_color, (cx+x_offset, cy-20, 8, 10))
                    pygame.draw.rect(surface, highlight_color, (cx+x_offset, cy-20, 4, 10))
                    pygame.draw.rect(surface, outline_color, (cx+x_offset, cy-20, 8, 10), 1)

                # Outline
                pygame.draw.ellipse(surface, outline_color, (cx-15, cy+10, 30, 10), 1)
                pygame.draw.rect(surface, outline_color, (cx-12, cy-15, 24, 30), 1, border_radius=2)

            elif piece_type == 'knight':
                # Base
                pygame.draw.ellipse(surface, shadow_color, (cx-15, cy+10, 30, 10))

                # Body
                points = [
                    (cx-10, cy+10),  # Bottom left
                    (cx-5, cy-15),   # Top left
                    (cx+5, cy-20),   # Top
                    (cx+15, cy-5),   # Top right
                    (cx+10, cy+10)   # Bottom right
                ]
                pygame.draw.polygon(surface, main_color, points)

                # Highlight
                highlight_points = [
                    (cx-10, cy+10),  # Bottom left
                    (cx-5, cy-15),   # Top left
                    (cx+5, cy-20),   # Top
                    (cx, cy-5),      # Middle
                    (cx, cy+10)      # Bottom middle
                ]
                pygame.draw.polygon(surface, highlight_color, highlight_points)

                # Eye
                pygame.draw.circle(surface, detail_color, (cx+5, cy-10), 2)

                # Mane
                for i in range(3):
                    y_offset = -15 + i*5
                    pygame.draw.ellipse(surface, shadow_color, (cx-2, cy+y_offset, 12, 5))

                # Outline
                pygame.draw.ellipse(surface, outline_color, (cx-15, cy+10, 30, 10), 1)
                pygame.draw.polygon(surface, outline_color, points, 1)

            elif piece_type == 'bishop':
                # Base
                pygame.draw.ellipse(surface, shadow_color, (cx-15, cy+10, 30, 10))

                # Body
                pygame.draw.polygon(surface, main_color, [
                    (cx, cy-20),        # Top
                    (cx-12, cy+10),     # Bottom left
                    (cx+12, cy+10)      # Bottom right
                ])

                # Highlight
                pygame.draw.polygon(surface, highlight_color, [
                    (cx, cy-20),        # Top
                    (cx-12, cy+10),     # Bottom left
                    (cx, cy+10)         # Bottom middle
                ])

                # Cross on top
                pygame.draw.rect(surface, detail_color, (cx-1, cy-25, 2, 10))
                pygame.draw.rect(surface, detail_color, (cx-5, cy-21, 10, 2))

                # Outline
                pygame.draw.ellipse(surface, outline_color, (cx-15, cy+10, 30, 10), 1)
                pygame.draw.polygon(surface, outline_color, [
                    (cx, cy-20),
                    (cx-12, cy+10),
                    (cx+12, cy+10)
                ], 1)

            elif piece_type == 'queen':
                # Base
                pygame.draw.ellipse(surface, shadow_color, (cx-15, cy+10, 30, 10))

                # Body
                pygame.draw.polygon(surface, main_color, [
                    (cx, cy-20),        # Top
                    (cx-15, cy+10),     # Bottom left
                    (cx+15, cy+10)      # Bottom right
                ])

                # Highlight
                pygame.draw.polygon(surface, highlight_color, [
                    (cx, cy-20),        # Top
                    (cx-15, cy+10),     # Bottom left
                    (cx, cy+10)         # Bottom middle
                ])

                # Crown points
                for i in range(5):
                    angle = math.pi/2 + i * 2*math.pi/5
                    px = cx + 15 * math.cos(angle)
                    py = cy - 20 + 15 * math.sin(angle)
                    pygame.draw.circle(surface, main_color, (int(px), int(py)), 4)
                    pygame.draw.circle(surface, highlight_color, (int(px-1), int(py-1)), 2)
                    pygame.draw.circle(surface, outline_color, (int(px), int(py)), 4, 1)

                # Outline
                pygame.draw.ellipse(surface, outline_color, (cx-15, cy+10, 30, 10), 1)
                pygame.draw.polygon(surface, outline_color, [
                    (cx, cy-20),
                    (cx-15, cy+10),
                    (cx+15, cy+10)
                ], 1)

            elif piece_type == 'king':
                # Base
                pygame.draw.ellipse(surface, shadow_color, (cx-15, cy+10, 30, 10))

                # Body
                pygame.draw.polygon(surface, main_color, [
                    (cx, cy-15),        # Top
                    (cx-15, cy+10),     # Bottom left
                    (cx+15, cy+10)      # Bottom right
                ])

                # Highlight
                pygame.draw.polygon(surface, highlight_color, [
                    (cx, cy-15),        # Top
                    (cx-15, cy+10),     # Bottom left
                    (cx, cy+10)         # Bottom middle
                ])

                # Crown
                pygame.draw.rect(surface, main_color, (cx-10, cy-25, 20, 10), border_radius=3)
                pygame.draw.rect(surface, highlight_color, (cx-10, cy-25, 10, 10), border_radius=3)

                # Cross on top
                pygame.draw.rect(surface, detail_color, (cx-1, cy-35, 2, 15))
                pygame.draw.rect(surface, detail_color, (cx-5, cy-28, 10, 2))

                # Outline
                pygame.draw.ellipse(surface, outline_color, (cx-15, cy+10, 30, 10), 1)
                pygame.draw.polygon(surface, outline_color, [
                    (cx, cy-15),
                    (cx-15, cy+10),
                    (cx+15, cy+10)
                ], 1)
                pygame.draw.rect(surface, outline_color, (cx-10, cy-25, 20, 10), 1, border_radius=3)

            # Add shadow beneath piece for 3D effect
            shadow_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            shadow_radius = 15
            pygame.draw.ellipse(shadow_surface, (0, 0, 0, 40), (cx-shadow_radius, cy+15, shadow_radius*2, 8))
            surface.blit(shadow_surface, (0, 0))

            images[(piece_type, color)] = surface

    return images

# Draw functions
def draw_board(screen):
    """Draw the chess board with coordinates and border"""
    # Use the enhanced board drawing function
    draw_enhanced_board(screen, BOARD_X_OFFSET, BOARD_Y_OFFSET, BOARD_WIDTH, SQUARE_SIZE)

def draw_pieces(screen, board, piece_images):
    """Draw the chess pieces"""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece:
                piece_type = piece['type']
                color = piece['color']
                image = piece_images.get((piece_type, color))
                if image:
                    screen.blit(image, (
                        BOARD_X_OFFSET + col * SQUARE_SIZE,
                        BOARD_Y_OFFSET + row * SQUARE_SIZE
                    ))

def draw_highlight(screen, pos, valid_moves=None, board=None):
    """Draw a highlight at the given position and show valid moves"""
    # Use the enhanced highlight drawing function
    draw_enhanced_highlight(screen, pos, BOARD_X_OFFSET, BOARD_Y_OFFSET, SQUARE_SIZE, valid_moves, board)

def draw_sidebar(screen, game, player_color, chat_input="", is_typing=False, new_game_button=None, spectator_name=None, is_bot_game=False):
    """Draw the sidebar with game info and chat"""
    # Use the enhanced sidebar drawing function
    draw_enhanced_sidebar(
        screen,
        WINDOW_WIDTH - SIDEBAR_WIDTH,
        SIDEBAR_WIDTH,
        WINDOW_HEIGHT,
        game,
        player_color,
        title_font,
        header_font,
        font,
        small_font,
        chat_input,
        is_typing,
        new_game_button,
        spectator_name,
        is_bot_game
    )


def show_menu():
    """Show interactive menu for game setup"""
    print("\n🏆 Chess Game - Interactive Menu")
    print("=" * 40)
    print("1. Play as White")
    print("2. Play as Black")
    print("3. Spectate Game")
    print("4. Play vs AI (White)")
    print("5. Play vs AI (Black)")
    print("6. Exit")
    print("=" * 40)

    while True:
        try:
            choice = input("Enter your choice (1-6): ").strip()

            if choice == "1":
                return "white", None, None
            elif choice == "2":
                return "black", None, None
            elif choice == "3":
                return "spectator", None, None
            elif choice == "4":
                # Play as white vs AI
                difficulty = input("AI Difficulty (easy/medium/hard) [medium]: ").strip().lower()
                if not difficulty:
                    difficulty = "medium"
                if difficulty not in ["easy", "medium", "hard"]:
                    difficulty = "medium"
                return "white", difficulty, None
            elif choice == "5":
                # Play as black vs AI (not typically used, but available)
                difficulty = input("AI Difficulty (easy/medium/hard) [medium]: ").strip().lower()
                if not difficulty:
                    difficulty = "medium"
                if difficulty not in ["easy", "medium", "hard"]:
                    difficulty = "medium"
                return "black", difficulty, None
            elif choice == "6":
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter 1-6.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Chess Game")
    parser.add_argument("color", nargs="?", help="Player color (white, black, or spectator)")
    parser.add_argument("game_id", nargs="?", help="Game ID")
    parser.add_argument("player_name", nargs="?", help="Player name")
    parser.add_argument("--bot", nargs="?", const="medium", help="Play against bot with specified difficulty (easy, medium, hard)")

    # Handle the case where sys.argv might have '--bot' as the 4th argument and the difficulty as the 5th
    if len(sys.argv) > 4 and sys.argv[4] == "--bot" and len(sys.argv) > 5:
        args = parser.parse_args(sys.argv[1:4] + ["--bot", sys.argv[5]])
    else:
        args = parser.parse_args()

    # If no color provided, show interactive menu
    if not args.color:
        player_color, bot_difficulty, _ = show_menu()
        game_id = args.game_id
        player_name = args.player_name
        play_against_bot = bot_difficulty is not None
        if not player_name:
            player_name = input("Enter your name (optional): ").strip()
            if not player_name:
                player_name = f"Player_{player_color}"
    else:
        player_color = args.color.lower()
        if player_color not in COLORS and player_color != 'spectator':
            print(f"Invalid color: {player_color}")
            print("Valid options: white, black, spectator")
            return

        # Get game ID and player name
        game_id = args.game_id
        player_name = args.player_name

        # Check if playing against bot
        play_against_bot = args.bot is not None
        bot_difficulty = args.bot if args.bot else "medium"

    # Create window (not fullscreen)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(f"Chess - {player_color.capitalize()} Player")
    clock = pygame.time.Clock()

    # Create game
    game = ChessGame(game_id, player_name)

    # Create beautiful 3D-style piece images
    piece_images = create_enhanced_piece_images(SQUARE_SIZE)

    # Initialize bot if playing against bot
    bot = None
    if play_against_bot and player_color == 'white':
        bot = ChessBot(bot_difficulty)
        bot.set_color('black')
        # Set the black player name to the bot name
        game.black_player_name = bot.name

    # Create buttons based on player role
    if player_color == 'spectator':
        # Spectators don't get a new game button
        new_game_button = None
    else:
        # Players get a new game button with enhanced style
        new_game_button = EnhancedButton(
            WINDOW_WIDTH - SIDEBAR_WIDTH + 20,
            205,
            SIDEBAR_WIDTH - 40,
            35,
            "New Game",
            "new_game"
        )

    # Initialize game state file if it doesn't exist
    game_state_file = GAME_STATE_FILE_TEMPLATE.format(game.game_id)
    if not os.path.exists(game_state_file):
        save_game_state(game)
    else:
        load_game_state(game, player_color)

    # If we're the black player joining an existing game, update our name
    if player_color == 'black' and player_name:
        if game.black_player_name == "Waiting for opponent...":
            game.set_black_player(player_name)
            save_game_state(game)

    # Main game loop
    running = True
    last_check_time = 0
    chat_input = ""
    is_typing = False

    # Background pattern with animated chess pieces
    def draw_background(screen):
        # Draw a gradient background - classic black-and-white
        for y in range(WINDOW_HEIGHT):
            # Create a gradient from dark gray to slightly lighter gray
            color_value = 30 + (y / WINDOW_HEIGHT * 20)
            color = (color_value, color_value, color_value)
            pygame.draw.line(screen, color, (0, y), (WINDOW_WIDTH, y))

        # Draw subtle chess pattern at the bottom with classic black-and-white color scheme
        pattern_height = 100
        pattern_surface = pygame.Surface((WINDOW_WIDTH, pattern_height), pygame.SRCALPHA)
        square_size = 25
        for row in range(pattern_height // square_size):
            for col in range(WINDOW_WIDTH // square_size):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
                pygame.draw.rect(pattern_surface, color, (
                    col * square_size, row * square_size, square_size, square_size
                ))
        pattern_surface.set_alpha(150)  # More visible
        screen.blit(pattern_surface, (0, WINDOW_HEIGHT - pattern_height))

    while running:
        try:
            # Get current mouse position for button hover effects
            mouse_pos = pygame.mouse.get_pos()
            if new_game_button:  # Only update if button exists (not for spectators)
                new_game_button.update(mouse_pos)

            # Check for game state updates every 0.5 seconds
            current_time = time.time()
            if current_time - last_check_time > 0.5:
                # Always check for updates to get new chat messages
                # But preserve our player name
                load_game_state(game, player_color)
                last_check_time = current_time

                # If playing against bot and it's the bot's turn, make a move
                if bot and game.turn == bot.color:
                    # Let the bot make a move
                    bot_move = bot.make_move(game)
                    if bot_move:
                        from_pos, to_pos = bot_move
                        if game.make_move(from_pos, to_pos, bot.color):
                            # Add a message about the bot's move
                            game.add_message("System", f"{bot.name} made a move")
                            # Save the updated game state
                            save_game_state(game)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if is_typing:
                            is_typing = False
                            chat_input = ""

                    # Only process chat input if not playing against bot and game is in progress
                    elif is_typing and not bot and game.status == "in_progress":
                        if event.key == pygame.K_RETURN:
                            if chat_input:
                                # Determine sender name for the chat
                                if player_color == 'spectator':
                                    # Spectators use their name with a [Spectator] tag
                                    sender_name = f"[Spectator] {player_name if player_name else 'Anonymous'}"
                                else:
                                    # Players use their player name
                                    sender_name = game.white_player_name if player_color == 'white' else game.black_player_name

                                # Send the chat message directly without filtering
                                game.add_chat(sender_name, chat_input)
                                save_game_state(game)

                                chat_input = ""
                        elif event.key == pygame.K_BACKSPACE:
                            chat_input = chat_input[:-1]
                        else:
                            # Add character to chat input
                            if len(chat_input) < 50:  # Limit input length
                                chat_input += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        try:
                            # Get mouse position
                            mouse_pos = pygame.mouse.get_pos()

                            # Spectators can't interact with the board or reset the game
                            if player_color != 'spectator':
                                # Check if new game button was clicked
                                if new_game_button:
                                    action = new_game_button.check_click(mouse_pos)
                                    if action == "new_game":
                                        game.reset_game()
                                        # If playing against bot, make sure the bot name is preserved
                                        if bot:
                                            game.black_player_name = bot.name
                                        save_game_state(game)
                                        continue

                                # Check if click is on the board
                                board_rect = pygame.Rect(BOARD_X_OFFSET, BOARD_Y_OFFSET, BOARD_WIDTH, BOARD_WIDTH)
                                if board_rect.collidepoint(mouse_pos):
                                    # Convert screen coordinates to board coordinates
                                    col = (mouse_pos[0] - BOARD_X_OFFSET) // SQUARE_SIZE
                                    row = (mouse_pos[1] - BOARD_Y_OFFSET) // SQUARE_SIZE

                                    # Check if it's our turn
                                    if (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and
                                        game.turn == player_color):
                                        # If a piece is already selected, try to move it
                                        if game.selected_piece:
                                            from_pos = game.selected_piece
                                            to_pos = (row, col)

                                            # Try to make the move
                                            if game.make_move(from_pos, to_pos, player_color):
                                                game.selected_piece = None
                                                game.valid_moves = []
                                                # Save the updated game state
                                                save_game_state(game)
                                            else:
                                                # If the move is invalid, check if clicked on another piece
                                                piece = game.board[row][col]
                                                if piece and piece['color'] == player_color:
                                                    game.selected_piece = (row, col)
                                                    # Calculate valid moves for the newly selected piece
                                                    game.valid_moves = game.get_valid_moves((row, col))
                                                else:
                                                    game.selected_piece = None
                                                    game.valid_moves = []
                                        else:
                                            # Check if clicked on a piece
                                            piece = game.board[row][col]
                                            if piece and piece['color'] == player_color:
                                                game.selected_piece = (row, col)
                                                # Calculate valid moves for the selected piece
                                                game.valid_moves = game.get_valid_moves((row, col))

                            # Check if chat is enabled (not playing against bot and game is in progress)
                            chat_enabled = not bot and game.status == "in_progress"

                            if chat_enabled:
                                # Check if the chat input box was clicked
                                chat_input_rect = pygame.Rect(
                                    WINDOW_WIDTH - SIDEBAR_WIDTH + 20,
                                    WINDOW_HEIGHT - 50,
                                    SIDEBAR_WIDTH - 40,  # Match the full width from the sidebar function
                                    40
                                )
                                if chat_input_rect.collidepoint(mouse_pos):
                                    is_typing = True
                                else:
                                    is_typing = False
                            else:
                                # Disable chat input when playing against bot or game is over
                                is_typing = False

                        except Exception as e:
                            print(f"Error handling click: {e}")

            # Clean up any expired messages
            game.clean_expired_messages()

            # Draw everything
            draw_background(screen)
            draw_board(screen)

            # Draw highlight for selected piece and valid moves
            if game.selected_piece:
                draw_highlight(screen, game.selected_piece, game.valid_moves, game.board)

            draw_pieces(screen, game.board, piece_images)

            # Draw sidebar (pass is_bot_game=True if playing against bot)
            draw_sidebar(screen, game, player_color, chat_input, is_typing, None, player_name, is_bot_game=bool(bot))

            # Draw new game button separately (since our enhanced button needs the font parameter)
            if new_game_button:
                new_game_button.draw(screen, font)

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(FPS)

        except Exception as e:
            print(f"Error in main loop: {e}")

    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        pygame.quit()
        sys.exit(1)
