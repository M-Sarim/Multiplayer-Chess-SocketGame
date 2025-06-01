#!/usr/bin/env python3
"""
Chess Game Server
Handles multiple chess games using sockets and threads
"""

import socket
import threading
import json
import time
import uuid
import os
import signal
import sys
from queue import Queue

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 5555        # Port to listen on
BUFFER_SIZE = 4096  # Socket buffer size

# Game state storage
games = {}  # Dictionary to store active games
clients = {}  # Dictionary to store connected clients
client_locks = {}  # Locks for thread safety

# Create a lock for thread-safe operations on shared resources
games_lock = threading.Lock()
clients_lock = threading.Lock()

# Message queue for broadcasting
message_queue = Queue()

class ChessGameState:
    """Class to store and manage chess game state"""
    def __init__(self, game_id=None, creator_name=None):
        self.game_id = game_id if game_id else str(uuid.uuid4())
        self.board = self.create_initial_board()
        self.turn = 'white'
        self.status = 'in_progress'
        self.messages = []
        self.chat_messages = []
        self.last_update = time.time()
        self.white_player_name = creator_name if creator_name else "White Player"
        self.black_player_name = "Waiting for opponent..."
        self.white_player_socket = None
        self.black_player_socket = None
        self.spectators = []

        # Add initial messages
        self.add_message("System", "Game created!")
        self.add_chat("System", "Chat enabled. Type messages below.")

    def create_initial_board(self):
        """Create the initial chess board"""
        # 8x8 board with pieces
        board = [[None for _ in range(8)] for _ in range(8)]

        # Set up pawns
        for col in range(8):
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
        """Add a message to the chat"""
        self.chat_messages.append({'sender': sender, 'text': text, 'time': time.time()})
        if len(self.chat_messages) > 20:
            self.chat_messages.pop(0)

    def set_black_player(self, player_name):
        """Set the black player name when they join"""
        self.black_player_name = player_name
        self.add_message("System", f"{player_name} has joined as Black!")
        self.add_chat("System", f"{player_name} has joined the game.")

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
        self.board = data['board']
        self.turn = data['turn']
        self.status = data['status']
        self.messages = data['messages']
        self.chat_messages = data.get('chat_messages', self.chat_messages)
        self.last_update = data['last_update']
        self.white_player_name = data.get('white_player_name', self.white_player_name)
        self.black_player_name = data.get('black_player_name', self.black_player_name)

def handle_client(client_socket, client_address):
    """Handle a client connection"""
    print(f"New connection from {client_address}")
    client_id = str(uuid.uuid4())

    with clients_lock:
        clients[client_id] = {
            'socket': client_socket,
            'address': client_address,
            'game_id': None,
            'player_color': None,
            'player_name': None
        }

    try:
        while True:
            # Receive data from client
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break

            # Parse the JSON message
            try:
                message = json.loads(data.decode('utf-8'))
                handle_message(client_id, message)
            except json.JSONDecodeError:
                print(f"Invalid JSON from client {client_id}")
            except Exception as e:
                print(f"Error handling message from client {client_id}: {e}")

    except Exception as e:
        print(f"Error with client {client_id}: {e}")

    finally:
        # Clean up when client disconnects
        cleanup_client(client_id)
        client_socket.close()
        print(f"Connection closed for {client_address}")

def handle_message(client_id, message):
    """Process a message from a client"""
    message_type = message.get('type')

    if message_type == 'create_game':
        create_game(client_id, message)

    elif message_type == 'join_game':
        join_game(client_id, message)

    elif message_type == 'spectate_game':
        spectate_game(client_id, message)

    elif message_type == 'make_move':
        make_move(client_id, message)

    elif message_type == 'chat_message':
        handle_chat(client_id, message)

    elif message_type == 'request_state':
        send_game_state(client_id)

    else:
        print(f"Unknown message type: {message_type}")

def create_game(client_id, message):
    """Create a new game"""
    player_name = message.get('player_name', 'Player')

    with games_lock:
        # Create a new game
        game_id = str(uuid.uuid4())
        games[game_id] = ChessGameState(game_id, player_name)

        # Update client info
        with clients_lock:
            clients[client_id]['game_id'] = game_id
            clients[client_id]['player_color'] = 'white'
            clients[client_id]['player_name'] = player_name
            games[game_id].white_player_socket = clients[client_id]['socket']

        # Send response to client
        response = {
            'type': 'game_created',
            'game_id': game_id,
            'player_color': 'white',
            'game_state': games[game_id].to_dict()
        }
        send_to_client(client_id, response)

        print(f"Game {game_id} created by {player_name}")

def join_game(client_id, message):
    """Join an existing game"""
    game_id = message.get('game_id')
    player_name = message.get('player_name', 'Player')

    with games_lock:
        if game_id not in games:
            response = {'type': 'error', 'message': 'Game not found'}
            send_to_client(client_id, response)
            return

        game = games[game_id]

        # Check if black player slot is available
        if game.black_player_name != "Waiting for opponent...":
            response = {'type': 'error', 'message': 'Game is full'}
            send_to_client(client_id, response)
            return

        # Join as black player
        game.set_black_player(player_name)

        # Update client info
        with clients_lock:
            clients[client_id]['game_id'] = game_id
            clients[client_id]['player_color'] = 'black'
            clients[client_id]['player_name'] = player_name
            game.black_player_socket = clients[client_id]['socket']

        # Send response to client
        response = {
            'type': 'game_joined',
            'game_id': game_id,
            'player_color': 'black',
            'game_state': game.to_dict()
        }
        send_to_client(client_id, response)

        # Notify white player
        if game.white_player_socket:
            notify = {
                'type': 'opponent_joined',
                'opponent_name': player_name,
                'game_state': game.to_dict()
            }
            game.white_player_socket.sendall(json.dumps(notify).encode('utf-8'))

        print(f"Player {player_name} joined game {game_id} as black")

def spectate_game(client_id, message):
    """Join a game as a spectator"""
    game_id = message.get('game_id')
    spectator_name = message.get('player_name', 'Spectator')

    with games_lock:
        if game_id not in games:
            response = {'type': 'error', 'message': 'Game not found'}
            send_to_client(client_id, response)
            return

        game = games[game_id]

        # Update client info
        with clients_lock:
            clients[client_id]['game_id'] = game_id
            clients[client_id]['player_color'] = 'spectator'
            clients[client_id]['player_name'] = spectator_name
            game.spectators.append(clients[client_id]['socket'])

        # Send response to client
        response = {
            'type': 'game_spectating',
            'game_id': game_id,
            'player_color': 'spectator',
            'game_state': game.to_dict()
        }
        send_to_client(client_id, response)

        # Notify players that a spectator joined
        game.add_chat("System", f"{spectator_name} is now spectating")

        # Broadcast updated game state
        broadcast_game_state(game_id)

        print(f"Player {spectator_name} is spectating game {game_id}")

def make_move(client_id, message):
    """Process a move from a player"""
    game_id = message.get('game_id')
    from_pos = message.get('from_pos')
    to_pos = message.get('to_pos')

    with games_lock:
        if game_id not in games:
            response = {'type': 'error', 'message': 'Game not found'}
            send_to_client(client_id, response)
            return

        game = games[game_id]
        client_info = clients.get(client_id)

        if not client_info:
            return

        player_color = client_info['player_color']

        # Check if it's this player's turn
        if game.turn != player_color:
            response = {'type': 'error', 'message': 'Not your turn'}
            send_to_client(client_id, response)
            return

        # Update the game state with the move
        # This is a simplified version - in a real implementation, you would validate the move
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # Get the piece and check if it exists
        piece = game.board[from_row][from_col]
        if not piece or piece['color'] != player_color:
            response = {'type': 'error', 'message': 'Invalid piece selection'}
            send_to_client(client_id, response)
            return

        # Move the piece
        captured = game.board[to_row][to_col]
        game.board[to_row][to_col] = piece
        game.board[from_row][from_col] = None

        # Add message about the move
        move_text = f"{piece['color']} {piece['type']} moved from ({from_row},{from_col}) to ({to_row},{to_col})"
        if captured:
            move_text += f", capturing {captured['color']} {captured['type']}"
        game.add_message("System", move_text)

        # Switch turns
        game.turn = 'black' if game.turn == 'white' else 'white'

        # Update timestamp
        game.last_update = time.time()

        # Broadcast the updated game state to all clients in this game
        broadcast_game_state(game_id)

        print(f"Move made in game {game_id} by {player_color}")

def handle_chat(client_id, message):
    """Process a chat message"""
    game_id = message.get('game_id')
    chat_text = message.get('text', '')

    with games_lock:
        if game_id not in games:
            return

        game = games[game_id]
        client_info = clients.get(client_id)

        if not client_info:
            return

        player_name = client_info['player_name']
        player_color = client_info['player_color']

        # Format sender name based on role
        if player_color == 'spectator':
            sender_name = f"[Spectator] {player_name}"
        else:
            sender_name = player_name

        # Add the chat message
        game.add_chat(sender_name, chat_text)

        # Broadcast the updated game state
        broadcast_game_state(game_id)

        print(f"Chat in game {game_id} from {sender_name}: {chat_text}")

def send_game_state(client_id):
    """Send the current game state to a client"""
    client_info = clients.get(client_id)
    if not client_info or not client_info['game_id']:
        return

    game_id = client_info['game_id']

    with games_lock:
        if game_id not in games:
            return

        game = games[game_id]

        response = {
            'type': 'game_state_update',
            'game_state': game.to_dict()
        }

        send_to_client(client_id, response)

def broadcast_game_state(game_id):
    """Broadcast game state to all clients in a game"""
    with games_lock:
        if game_id not in games:
            return

        game = games[game_id]
        game_state = game.to_dict()

        # Prepare the message
        message = {
            'type': 'game_state_update',
            'game_state': game_state
        }

        # Send to white player
        if game.white_player_socket:
            try:
                game.white_player_socket.sendall(json.dumps(message).encode('utf-8'))
            except:
                pass

        # Send to black player
        if game.black_player_socket:
            try:
                game.black_player_socket.sendall(json.dumps(message).encode('utf-8'))
            except:
                pass

        # Send to all spectators
        for spectator_socket in game.spectators:
            try:
                spectator_socket.sendall(json.dumps(message).encode('utf-8'))
            except:
                # Remove disconnected spectators later
                pass

def send_to_client(client_id, message):
    """Send a message to a specific client"""
    with clients_lock:
        if client_id not in clients:
            return

        client_socket = clients[client_id]['socket']

        try:
            client_socket.sendall(json.dumps(message).encode('utf-8'))
        except Exception as e:
            print(f"Error sending to client {client_id}: {e}")

def cleanup_client(client_id):
    """Clean up when a client disconnects"""
    with clients_lock:
        if client_id not in clients:
            return

        client_info = clients[client_id]
        game_id = client_info.get('game_id')
        player_color = client_info.get('player_color')
        player_name = client_info.get('player_name')

        # Remove from clients dictionary
        del clients[client_id]

    # Handle game cleanup if needed
    if game_id:
        with games_lock:
            if game_id in games:
                game = games[game_id]

                if player_color == 'white':
                    # White player left
                    game.add_message("System", f"{player_name} (White) has left the game")
                    game.add_chat("System", f"{player_name} (White) has left the game")
                    game.white_player_socket = None

                    # If black player is still connected, let them know
                    if game.black_player_socket:
                        notify = {
                            'type': 'opponent_left',
                            'opponent_color': 'white',
                            'game_state': game.to_dict()
                        }
                        try:
                            game.black_player_socket.sendall(json.dumps(notify).encode('utf-8'))
                        except:
                            pass

                elif player_color == 'black':
                    # Black player left
                    game.add_message("System", f"{player_name} (Black) has left the game")
                    game.add_chat("System", f"{player_name} (Black) has left the game")
                    game.black_player_socket = None

                    # If white player is still connected, let them know
                    if game.white_player_socket:
                        notify = {
                            'type': 'opponent_left',
                            'opponent_color': 'black',
                            'game_state': game.to_dict()
                        }
                        try:
                            game.white_player_socket.sendall(json.dumps(notify).encode('utf-8'))
                        except:
                            pass

                elif player_color == 'spectator':
                    # Spectator left
                    game.add_chat("System", f"{player_name} has stopped spectating")

                    # Remove from spectators list
                    if client_info['socket'] in game.spectators:
                        game.spectators.remove(client_info['socket'])

                # If both players are gone and no spectators, remove the game
                if not game.white_player_socket and not game.black_player_socket and not game.spectators:
                    del games[game_id]
                    print(f"Game {game_id} removed as all players left")
                else:
                    # Broadcast updated state to remaining players/spectators
                    broadcast_game_state(game_id)

def main():
    """Main server function"""
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Chess server started on {HOST}:{PORT}")

        # Handle graceful shutdown
        def signal_handler(sig, frame):
            print("\nShutting down server...")
            server_socket.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        # Accept connections
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True
            client_thread.start()

    except Exception as e:
        print(f"Server error: {e}")

    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
