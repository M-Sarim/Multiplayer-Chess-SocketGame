"""
Chess Bot Implementation
This file contains a simple chess bot that can play against a human player
"""
import random
import time

# Use the BOARD_SIZE constant directly
BOARD_SIZE = 8

class ChessBot:
    """A simple chess bot that can play chess"""
    def __init__(self, difficulty="medium"):
        """Initialize the bot with a difficulty level"""
        self.difficulty = difficulty  # "easy", "medium", or "hard"
        self.name = f"Chess Bot ({difficulty.capitalize()})"
        self.color = None  # Will be set when the game starts

    def set_color(self, color):
        """Set the bot's color"""
        self.color = color

    def make_move(self, game):
        """Make a move based on the current game state"""
        # Add a small delay to make it seem like the bot is "thinking"
        thinking_time = {
            "easy": 0.5,
            "medium": 1.0,
            "hard": 1.5
        }.get(self.difficulty, 1.0)

        time.sleep(thinking_time)

        # Print debug info
        print(f"Bot {self.name} is thinking...")
        print(f"Bot color: {self.color}")
        print(f"Current turn: {game.turn}")

        # Get all valid moves for the bot's pieces
        valid_moves = self._get_all_valid_moves(game)

        # Print number of valid moves found
        print(f"Found {len(valid_moves)} valid moves")

        if not valid_moves:
            print("No valid moves available")
            return None  # No valid moves available

        # Choose a move based on difficulty
        chosen_move = None
        if self.difficulty == "easy":
            # Easy: Choose a random move
            chosen_move = self._choose_random_move(valid_moves)
        elif self.difficulty == "medium":
            # Medium: Prefer captures and checks, but sometimes make random moves
            chosen_move = self._choose_medium_move(valid_moves, game)
        else:  # hard
            # Hard: Evaluate positions and choose the best move
            chosen_move = self._choose_hard_move(valid_moves, game)

        # Print the chosen move
        if chosen_move:
            from_pos, to_pos = chosen_move
            print(f"Bot chose move: {from_pos} -> {to_pos}")
        else:
            print("Bot couldn't find a move")

        return chosen_move

    def _get_all_valid_moves(self, game):
        """Get all valid moves for the bot's pieces"""
        valid_moves = []

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = game.board[row][col]
                # Check if there's a piece and it's the bot's color
                if piece and isinstance(piece, dict) and piece.get('color') == self.color:
                    # For each piece of the bot's color, find all valid moves
                    from_pos = (row, col)

                    # Use the game's get_valid_moves method to get valid moves for this piece
                    piece_valid_moves = game.get_valid_moves(from_pos)
                    for to_pos in piece_valid_moves:
                        valid_moves.append((from_pos, to_pos))

        return valid_moves

    def _choose_random_move(self, valid_moves):
        """Choose a random move from the list of valid moves"""
        if not valid_moves:
            return None
        return random.choice(valid_moves)

    def _choose_medium_move(self, valid_moves, game):
        """Choose a move with medium difficulty strategy"""
        # Categorize moves
        capture_moves = []
        center_moves = []
        other_moves = []

        for from_pos, to_pos in valid_moves:
            # Check if it's a capture move
            if game.board[to_pos[0]][to_pos[1]]:
                capture_moves.append((from_pos, to_pos))
            # Check if it's a move to the center (4 center squares)
            elif 3 <= to_pos[0] <= 4 and 3 <= to_pos[1] <= 4:
                center_moves.append((from_pos, to_pos))
            else:
                other_moves.append((from_pos, to_pos))

        # Make sure we have at least one valid move
        if not valid_moves:
            return None

        # 60% chance to choose a capture if available
        if capture_moves and random.random() < 0.6:
            return random.choice(capture_moves)
        # 30% chance to choose a center move if available
        elif center_moves and random.random() < 0.3:
            return random.choice(center_moves)
        # Otherwise choose randomly from all moves
        else:
            return random.choice(valid_moves)

    def _choose_hard_move(self, valid_moves, game):
        """Choose a move with hard difficulty strategy"""
        if not valid_moves:
            return None

        best_move = None
        best_score = float('-inf')

        for from_pos, to_pos in valid_moves:
            # Make a copy of the game to simulate the move
            # Since we don't have a deep copy method, we'll evaluate without simulation
            score = self._evaluate_move(from_pos, to_pos, game)

            if score > best_score:
                best_score = score
                best_move = (from_pos, to_pos)

        return best_move

    def _evaluate_move(self, from_pos, to_pos, game):
        """Evaluate a move and return a score"""
        score = 0

        # Get the pieces involved
        piece = game.board[from_pos[0]][from_pos[1]]
        target = game.board[to_pos[0]][to_pos[1]]

        # Piece values
        piece_values = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 0  # King has no capture value
        }

        # If it's a capture, add the value of the captured piece
        if target:
            score += piece_values.get(target.get('type', ''), 0)

        # Prefer moving to the center of the board
        center_distance = abs(3.5 - to_pos[0]) + abs(3.5 - to_pos[1])
        score += (7 - center_distance) * 0.1

        # Prefer developing knights and bishops early
        if piece.get('type') in ['knight', 'bishop']:
            # Check if piece is in starting position
            if (self.color == 'white' and from_pos[0] == 7) or (self.color == 'black' and from_pos[0] == 0):
                score += 0.5

        # Add some randomness to avoid predictability
        score += random.uniform(0, 0.1)

        return score
