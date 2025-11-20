"""
Minimax algorithm with alpha-beta pruning for Smart Horses.
"""

from typing import Tuple, Optional, Dict
import time
from smart_backend.algorithms.heuristic import evaluate_game_state


class MinimaxResult:
    """Container for minimax result."""
    
    def __init__(self, evaluation: float, move: Optional[Tuple[int, int]], 
                 nodes_evaluated: int, depth_reached: int):
        self.evaluation = evaluation
        self.move = move
        self.nodes_evaluated = nodes_evaluated
        self.depth_reached = depth_reached


def minimax_alpha_beta(
    game_state,
    depth: int,
    alpha: float,
    beta: float,
    is_maximizing: bool,
    nodes_evaluated: int = 0
) -> Tuple[float, Optional[Tuple[int, int]], int]:
    """
    Minimax algorithm with alpha-beta pruning.
    
    Args:
        game_state: Current game state
        depth: Remaining depth to search (0 = terminal node)
        alpha: Best value for MAX player
        beta: Best value for MIN player
        is_maximizing: True if maximizing player (white/machine)
        nodes_evaluated: Counter for nodes evaluated
        
    Returns:
        Tuple of (evaluation, best_move, nodes_evaluated)
    """
    nodes_evaluated += 1
    
    # Terminal conditions
    if depth == 0 or game_state.game_over:
        return evaluate_game_state(game_state), None, nodes_evaluated
    
    player = 'white' if is_maximizing else 'black'
    valid_moves = game_state.get_valid_moves(player)
    
    # No valid moves = terminal state
    if not valid_moves:
        return evaluate_game_state(game_state), None, nodes_evaluated
    
    best_move = None
    
    if is_maximizing:
        # Maximizing player (white/machine)
        max_eval = float('-inf')
        
        for move in valid_moves:
            # Simulate move
            new_state = game_state.copy()
            new_state.make_move(player, move)
            
            # Recursive call
            eval_score, _, nodes_evaluated = minimax_alpha_beta(
                new_state, depth - 1, alpha, beta, False, nodes_evaluated
            )
            
            # Update best
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            
            # Alpha-beta pruning
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cutoff
        
        return max_eval, best_move, nodes_evaluated
    
    else:
        # Minimizing player (black/human)
        min_eval = float('inf')
        
        for move in valid_moves:
            # Simulate move
            new_state = game_state.copy()
            new_state.make_move(player, move)
            
            # Recursive call
            eval_score, _, nodes_evaluated = minimax_alpha_beta(
                new_state, depth - 1, alpha, beta, True, nodes_evaluated
            )
            
            # Update best
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            
            # Alpha-beta pruning
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cutoff
        
        return min_eval, best_move, nodes_evaluated


def find_best_move(game_state, max_depth: Optional[int] = None) -> MinimaxResult:
    """
    Find the best move for the current player using minimax.
    
    Args:
        game_state: Current game state
        max_depth: Maximum search depth (uses game_state.max_depth if None)
        
    Returns:
        MinimaxResult with evaluation, move, and statistics
    """
    if max_depth is None:
        max_depth = game_state.max_depth
    
    start_time = time.time()
    
    is_maximizing = game_state.current_player == 'white'
    
    evaluation, best_move, nodes_evaluated = minimax_alpha_beta(
        game_state,
        depth=max_depth,
        alpha=float('-inf'),
        beta=float('inf'),
        is_maximizing=is_maximizing,
        nodes_evaluated=0
    )
    
    elapsed_time = time.time() - start_time
    
    result = MinimaxResult(
        evaluation=evaluation,
        move=best_move,
        nodes_evaluated=nodes_evaluated,
        depth_reached=max_depth
    )
    
    return result
