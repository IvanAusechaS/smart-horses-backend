"""
Heuristic evaluation function for Smart Horses game.
"""

from typing import Dict, Tuple, Optional
from smart_backend.core.move_generator import count_valid_moves
from smart_backend.core.board_manager import (
    manhattan_distance,
    is_center_position,
    get_valuable_squares
)


def evaluate_game_state(game_state) -> float:
    """
    Evaluate how favorable the game state is for the machine (white).
    
    This function evaluates the game state from the perspective of the
    white player (machine). Positive values favor white, negative favor black.
    
    Factors considered:
        1. Score difference (weight: 100)
        2. Mobility - number of valid moves (weight: 10)
        3. Proximity to valuable squares (weight: 5)
        4. Center control (weight: 3)
        5. No moves penalty (weight: -400)
        6. Terminal state evaluation (+/-10000)
    
    Args:
        game_state: Current game state
        
    Returns:
        float: Evaluation score (positive favors white, negative favors black)
    """
    # Terminal state (game over)
    if game_state.game_over:
        if game_state.winner == 'white':
            return 10000  # Victory
        elif game_state.winner == 'black':
            return -10000  # Defeat
        else:
            return 0  # Tie
    
    evaluation = 0.0
    
    # 1. Score Difference (most important factor)
    score_weight = 100
    score_diff = game_state.white_score - game_state.black_score
    evaluation += score_diff * score_weight
    
    # 2. Mobility (number of valid moves)
    mobility_weight = 10
    white_moves = count_valid_moves(game_state.white_knight, game_state.board)
    black_moves = count_valid_moves(game_state.black_knight, game_state.board)
    mobility_diff = white_moves - black_moves
    evaluation += mobility_diff * mobility_weight
    
    # 3. Proximity to valuable squares
    proximity_weight = 5
    valuable_squares = get_valuable_squares(game_state.board)
    
    if valuable_squares:
        white_proximity = 0
        black_proximity = 0
        
        for position, value in valuable_squares:
            white_dist = manhattan_distance(game_state.white_knight, position)
            black_dist = manhattan_distance(game_state.black_knight, position)
            
            # Closer is better, avoid division by zero
            if white_dist > 0:
                white_proximity += value / white_dist
            else:
                white_proximity += value * 2  # On the square
            
            if black_dist > 0:
                black_proximity += value / black_dist
            else:
                black_proximity += value * 2  # On the square
        
        evaluation += (white_proximity - black_proximity) * proximity_weight
    
    # 4. Center Control
    center_weight = 3
    if is_center_position(game_state.white_knight):
        evaluation += center_weight
    if is_center_position(game_state.black_knight):
        evaluation -= center_weight
    
    # 5. Penalty for having no moves
    if white_moves == 0:
        evaluation -= 400  # -4 points * 100
    if black_moves == 0:
        evaluation += 400  # Opponent has no moves
    
    return evaluation


def evaluate_move_quality(
    game_state,
    move: Tuple[int, int],
    player: str
) -> float:
    """
    Quick evaluation of a single move without full state simulation.
    
    Args:
        game_state: Current game state
        move: Target position (row, col)
        player: 'white' or 'black'
        
    Returns:
        float: Move quality score
    """
    score = 0.0
    
    # Points gained from the square
    square_value = game_state.board.get(move, 0)
    if square_value and square_value != 'destroyed' and isinstance(square_value, int):
        score += square_value * 10  # Weight for immediate gain
    
    # Center bonus
    if is_center_position(move):
        score += 5
    
    # Mobility after move (estimated)
    # This is a simplified estimate without actually making the move
    from smart_backend.core.move_generator import get_knight_moves
    future_moves = get_knight_moves(move)
    available_future_moves = sum(
        1 for m in future_moves 
        if game_state.board.get(m) != 'destroyed'
    )
    score += available_future_moves * 2
    
    return score
