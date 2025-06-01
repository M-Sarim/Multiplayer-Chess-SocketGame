# 🏆 Multiplayer-Chess-SocketGame

A **multiplayer chess game platform** built with Python using socket programming for local network gameplay. This project demonstrates network programming concepts, game state management, and real-time communication between multiple clients.

## ✨ Key Features

### 🎮 **Core Gameplay**
- **Real-time multiplayer** over LAN using socket programming
- **Local two-player mode** for offline gameplay
- **AI opponents** with 3 difficulty levels (Easy, Medium, Hard)
- **Spectator mode** with live game viewing
- **Game state persistence** and synchronization
- **Full chess rules implementation** with move validation

### 🎨 **User Interface**
- **Pygame-based GUI** with classic black-and-white chess theme
- **Interactive piece movement** with click-to-move mechanics
- **Visual move highlighting** and piece selection
- **Real-time game status** and move history display
- **Intuitive lobby system** for game management

### 💬 **Communication**
- **Real-time chat system** for players and spectators
- **Lobby system** for game creation and joining
- **Game state broadcasting** to all participants
- **Player name display** and role identification

### 🌐 **Network Architecture**
- **Socket-based server** handling multiple concurrent games
- **Thread-safe game state management**
- **JSON message protocol** for client-server communication
- **Robust error handling** and connection management
- **UUID-based game identification**

## 📁 Project Structure

```
Multiplayer-Chess-SocketGame/
├── 📁 src/                       # Source code directory
│   ├── 📁 server/               # Server components
│   │   └── chess_server.py      # Main server with socket handling
│   │
│   ├── 📁 client/               # Client components
│   │   ├── chess_client.py      # Network client communication
│   │   ├── lobby_menu.py        # Game lobby and menu system
│   │   └── two_player_chess.py  # Main chess game interface
│   │
│   ├── 📁 utils/                # Utility modules
│   │   ├── chess_bot.py         # AI opponent implementation
│   │   ├── chess_assets.py      # Asset loading utilities
│   │   ├── chess_game_assets.py # Game visual assets
│   │   └── enhanced_chess_pieces.py # Enhanced piece graphics
│   │
│   └── 📁 common/               # Shared components
│       └── (message protocols and constants)
│
├── 📁 data/                      # Data storage
│   ├── chess_games_list.json   # Active games registry
│   └── 📁 game_states/         # Individual game state files
│
├── run_server.py               # Server entry point
├── run_client.py               # Client entry point
├── run_lobby.py                # Lobby menu entry point
└── requirements.txt            # Python dependencies
```

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.8+** (recommended 3.10+)
- **Git** for cloning the repository

### 1. Clone the Repository
```bash
git clone https://github.com/M-Sarim/Multiplayer-Chess-SocketGame.git
cd "Multiplayer-Chess-SocketGame"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Optional: Install Stockfish (for enhanced AI)
For enhanced AI analysis capabilities:
- **Windows**: Download from [stockfishchess.org](https://stockfishchess.org/download/)
- **Linux**: `sudo apt-get install stockfish`
- **macOS**: `brew install stockfish`

## 🎯 Quick Start

### Method 1: Using Entry Point Scripts (Recommended)

#### Start the Server
```bash
python run_server.py
```

#### Launch the Lobby Menu
```bash
python run_lobby.py
```

#### Launch the Game Client Directly
```bash
python run_client.py
```

### Method 2: Direct Module Execution

#### Start the Server
```bash
python src/server/chess_server.py
```

#### Launch the Lobby
```bash
python src/client/lobby_menu.py
```

#### Launch the Game Client
```bash
python src/client/two_player_chess.py
```

## 🎮 How to Play

### 🏁 **Getting Started**

#### For Online Multiplayer:
1. **Start the server** by running `python run_server.py`
2. **Launch the lobby** with `python run_lobby.py`
3. **Choose "Online Quick Match"** or **"Create Online Game"**
4. **Enter your player name** and game details
5. **Wait for opponent** or join an existing game
6. **Play chess** using standard rules!

#### For Local Two-Player:
1. **Launch the lobby** with `python run_lobby.py`
2. **Choose "Local Two-Player Game"**
3. **Enter player names** for both White and Black
4. **Play chess** on the same computer, taking turns

#### For AI Opponent:
1. **Launch the lobby** with `python run_lobby.py`
2. **Choose "Play vs AI"**
3. **Select difficulty**: Easy, Medium, or Hard
4. **Choose your color** (White or Black)
5. **Challenge the AI** and test your skills!

### 🎯 **Game Controls**
- **Click** to select pieces and make moves
- **Click again** on a valid square to move the piece
- **Chat** with opponents using the chat box (online games)
- **View move history** in the message panel
- **Spectate games** by joining as a spectator

### 🎨 **Game Modes**
- **Local Two-Player**: Play on the same computer
- **Online Multiplayer**: Play over network with friends
- **AI Opponent**: Challenge computer opponents
- **Spectator Mode**: Watch ongoing games
- **Create/Join Games**: Host or join specific games

## 🔧 Configuration

### Server Settings
Edit `src/server/chess_server.py` for server configuration:
```python
HOST = '127.0.0.1'  # Server IP address
PORT = 5555         # Server port
BUFFER_SIZE = 4096  # Socket buffer size
```

### Game Settings
Modify game constants in `src/client/two_player_chess.py`:
```python
WINDOW_WIDTH = 1200   # Game window width
WINDOW_HEIGHT = 800   # Game window height
BOARD_SIZE = 480      # Chess board size
SQUARE_SIZE = 60      # Individual square size
```

### AI Difficulty Settings
AI behavior can be customized in `src/utils/chess_bot.py`:
- **Easy**: Random move selection
- **Medium**: Prefers captures and checks
- **Hard**: Advanced position evaluation

### Network Configuration
For network play across different machines:
1. Update `SERVER_HOST` in `src/client/chess_client.py`
2. Ensure firewall allows connections on port 5555
3. Use actual IP address instead of localhost for remote connections

## 📊 Technical Features

### 🔧 **Implementation Details**
| Component | Technology | Description |
|-----------|------------|-------------|
| **GUI Framework** | Pygame | Cross-platform game development |
| **Chess Engine** | Custom + python-chess | Full chess rules implementation |
| **Network Protocol** | Raw TCP Sockets | Direct socket communication |
| **AI Engine** | Custom Algorithm | 3-level difficulty system |
| **Data Storage** | JSON Files | Game state persistence |
| **Threading** | Python Threading | Concurrent client handling |
| **Message Protocol** | JSON | Structured client-server communication |

### 🎮 **Game Features**
- ✅ **Full Chess Rules**: All standard chess moves and rules
- ✅ **Move Validation**: Prevents illegal moves
- ✅ **Real-time Updates**: Live game state synchronization
- ✅ **Chat System**: In-game communication
- ✅ **Spectator Mode**: Watch games in progress
- ✅ **AI Opponents**: Three difficulty levels
- ✅ **Local Multiplayer**: Same-computer gameplay
- ✅ **Network Multiplayer**: LAN-based online play
- ✅ **Game Persistence**: Save and resume games

## 🛠️ Development

### 📁 **Project Architecture**
- **Server**: `src/server/chess_server.py` - Handles all network communication
- **Client**: `src/client/` - Contains UI and game logic
- **Utils**: `src/utils/` - Shared utilities and AI implementation
- **Data**: `data/` - Game state storage and persistence

### 🔧 **Adding New Features**
1. **Server-side**: Modify `chess_server.py` to handle new message types
2. **Client-side**: Update UI components in `src/client/`
3. **Protocol**: Extend JSON message format for new features
4. **Testing**: Test with multiple clients and game scenarios

### 📝 **Code Style**
- Follow **PEP 8** Python style guidelines
- Use **descriptive variable names** and comments
- Implement **error handling** for network operations
- Add **logging** for debugging purposes

## 🐛 Troubleshooting

### Common Issues

**🔌 Connection Failed**
- ✅ Check if server is running (`python run_server.py`)
- ✅ Verify server shows "Chess server started on 127.0.0.1:5555"
- ✅ Check firewall settings allow port 5555
- ✅ Ensure client and server are on same network (for LAN play)

**🎮 Game Not Loading**
- ✅ Ensure all dependencies are installed (`pip install -r requirements.txt`)
- ✅ Check `data/game_states/` directory exists
- ✅ Verify Python version is 3.8 or higher
- ✅ Check console for error messages

**🤖 AI Not Responding**
- ✅ Verify AI difficulty is set correctly
- ✅ Check if it's the AI's turn (color matches)
- ✅ Look for error messages in console
- ✅ Restart the game if AI gets stuck

**🐌 Performance Issues**
- ✅ Close other applications to free memory
- ✅ Reduce window size if needed
- ✅ Check system meets minimum requirements
- ✅ Monitor CPU usage during gameplay

## 🙏 Acknowledgments

- **Pygame** library for cross-platform game development
- **python-chess** library for chess logic and validation
- **Stockfish** engine for enhanced AI capabilities
- **Python Socket Programming** for network communication
- **Chess community** for rules and gameplay inspiration

## 🚀 Future Enhancements

### 🎯 **Planned Features**
- **Tournament Mode**: Bracket-style competitions
- **Rating System**: ELO-based player rankings
- **Game Analysis**: Move analysis and suggestions
- **Replay System**: Review completed games
- **Custom Themes**: Additional board and piece styles
- **Sound Effects**: Audio feedback for moves and events

### 🌐 **Network Improvements**
- **Internet Play**: Connect over the internet (not just LAN)
- **Reconnection**: Automatic reconnection on disconnect
- **Game Invitations**: Direct player invitations
- **Lobby Chat**: General chat in the lobby area

### 🤖 **AI Enhancements**
- **More Difficulty Levels**: 5+ difficulty settings
- **Opening Book**: Common chess opening knowledge
- **Endgame Tables**: Perfect endgame play
- **Analysis Mode**: Position evaluation and hints

---
## 🔗 References

- [Python Socket Programming](https://realpython.com/python-sockets/)
- [Chess Programming Guide](https://www.chessprogramming.org/Main_Page)
- [Beginner’s Guide to Game Networking](https://gafferongames.com/post/what_every_programmer_needs_to_know_about_game_networking/)

## 👨‍💻 Author

**Muhammad Sarim**


## 📝 License

This project is licensed under the **MIT License** - see the LICENSE file for details.
