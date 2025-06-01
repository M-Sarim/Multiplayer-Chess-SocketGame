#!/usr/bin/env python3
"""
Chess Game Client
Connects to the chess server using sockets
"""

import socket
import threading
import json
import time
import queue

# Client configuration
SERVER_HOST = '127.0.0.1'  # Server IP
SERVER_PORT = 5555        # Server port
BUFFER_SIZE = 4096        # Socket buffer size

class ChessClient:
    """Client for connecting to the chess server"""
    def __init__(self):
        self.socket = None
        self.connected = False
        self.game_id = None
        self.player_color = None
        self.player_name = None
        self.game_state = None
        self.message_queue = queue.Queue()
        self.receive_thread = None
        self.callback = None
        self.chat_online = True  # Assume chat is online initially
    
    def connect(self, callback=None):
        """Connect to the chess server"""
        if self.connected:
            return True
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((SERVER_HOST, SERVER_PORT))
            self.connected = True
            self.callback = callback
            
            # Start receive thread
            self.receive_thread = threading.Thread(target=self._receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            print("Connected to chess server")
            return True
        
        except Exception as e:
            print(f"Connection error: {e}")
            self.connected = False
            self.chat_online = False
            return False
    
    def disconnect(self):
        """Disconnect from the chess server"""
        if not self.connected:
            return
        
        try:
            self.connected = False
            self.socket.close()
            print("Disconnected from chess server")
        except Exception as e:
            print(f"Disconnect error: {e}")
    
    def create_game(self, player_name):
        """Create a new game"""
        if not self.connected:
            print("Not connected to server")
            return False
        
        self.player_name = player_name
        
        message = {
            'type': 'create_game',
            'player_name': player_name
        }
        
        return self._send_message(message)
    
    def join_game(self, game_id, player_name):
        """Join an existing game"""
        if not self.connected:
            print("Not connected to server")
            return False
        
        self.player_name = player_name
        
        message = {
            'type': 'join_game',
            'game_id': game_id,
            'player_name': player_name
        }
        
        return self._send_message(message)
    
    def spectate_game(self, game_id, player_name):
        """Spectate an existing game"""
        if not self.connected:
            print("Not connected to server")
            return False
        
        self.player_name = player_name
        
        message = {
            'type': 'spectate_game',
            'game_id': game_id,
            'player_name': player_name
        }
        
        return self._send_message(message)
    
    def make_move(self, from_pos, to_pos):
        """Make a move in the game"""
        if not self.connected or not self.game_id:
            print("Not connected to a game")
            return False
        
        message = {
            'type': 'make_move',
            'game_id': self.game_id,
            'from_pos': from_pos,
            'to_pos': to_pos
        }
        
        return self._send_message(message)
    
    def send_chat(self, text):
        """Send a chat message"""
        if not self.connected or not self.game_id:
            print("Not connected to a game")
            return False
        
        message = {
            'type': 'chat_message',
            'game_id': self.game_id,
            'text': text
        }
        
        return self._send_message(message)
    
    def request_game_state(self):
        """Request the current game state"""
        if not self.connected or not self.game_id:
            print("Not connected to a game")
            return False
        
        message = {
            'type': 'request_state',
            'game_id': self.game_id
        }
        
        return self._send_message(message)
    
    def is_chat_online(self):
        """Check if chat is online"""
        return self.connected and self.chat_online
    
    def _send_message(self, message):
        """Send a message to the server"""
        if not self.connected:
            return False
        
        try:
            self.socket.sendall(json.dumps(message).encode('utf-8'))
            return True
        except Exception as e:
            print(f"Send error: {e}")
            self.connected = False
            self.chat_online = False
            return False
    
    def _receive_messages(self):
        """Receive messages from the server"""
        while self.connected:
            try:
                data = self.socket.recv(BUFFER_SIZE)
                if not data:
                    break
                
                # Parse the JSON message
                try:
                    message = json.loads(data.decode('utf-8'))
                    self._handle_message(message)
                except json.JSONDecodeError:
                    print("Invalid JSON received")
                except Exception as e:
                    print(f"Error handling message: {e}")
            
            except Exception as e:
                print(f"Receive error: {e}")
                self.connected = False
                self.chat_online = False
                break
        
        print("Receive thread ended")
    
    def _handle_message(self, message):
        """Process a message from the server"""
        message_type = message.get('type')
        
        if message_type == 'game_created':
            self.game_id = message.get('game_id')
            self.player_color = message.get('player_color')
            self.game_state = message.get('game_state')
            
            print(f"Game created with ID: {self.game_id}")
            print(f"You are playing as: {self.player_color}")
        
        elif message_type == 'game_joined':
            self.game_id = message.get('game_id')
            self.player_color = message.get('player_color')
            self.game_state = message.get('game_state')
            
            print(f"Joined game with ID: {self.game_id}")
            print(f"You are playing as: {self.player_color}")
        
        elif message_type == 'game_spectating':
            self.game_id = message.get('game_id')
            self.player_color = 'spectator'
            self.game_state = message.get('game_state')
            
            print(f"Spectating game with ID: {self.game_id}")
        
        elif message_type == 'game_state_update':
            self.game_state = message.get('game_state')
        
        elif message_type == 'opponent_joined':
            opponent_name = message.get('opponent_name')
            self.game_state = message.get('game_state')
            
            print(f"Opponent {opponent_name} joined the game")
        
        elif message_type == 'opponent_left':
            opponent_color = message.get('opponent_color')
            self.game_state = message.get('game_state')
            
            print(f"Opponent ({opponent_color}) left the game")
        
        elif message_type == 'error':
            error_message = message.get('message')
            print(f"Error: {error_message}")
        
        # Call the callback function if provided
        if self.callback:
            self.callback(message_type, self.game_state)

# Global client instance
chess_client = ChessClient()

def get_client():
    """Get the global client instance"""
    return chess_client
