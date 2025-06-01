#!/usr/bin/env python3
"""
Entry point for running the Chess Game Server
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    from src.server.chess_server import main
    main()
