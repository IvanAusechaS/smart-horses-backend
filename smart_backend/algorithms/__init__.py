"""
Algorithm implementations for Smart Horses game.

This package contains:
- Minimax with alpha-beta pruning
- Heuristic evaluation function
"""

from smart_backend.algorithms.minimax import find_best_move, minimax_alpha_beta
from smart_backend.algorithms.heuristic import evaluate_game_state

__all__ = ['find_best_move', 'minimax_alpha_beta', 'evaluate_game_state']

