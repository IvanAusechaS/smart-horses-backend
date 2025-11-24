"""
Heuristic evaluation function for Smart Horses game.

This module implements the evaluation function used by the Minimax algorithm
to assess board positions and guide decision-making. The heuristic combines
multiple strategic factors to determine how favorable a position is for the
machine player (white).

Mathematical Formula:
====================
H(s) = w₁·ΔScore + w₂·ΔMobility + w₃·ΔProximity + w₄·ΔCenter + w₅·NoMoves

Where:
    - ΔScore: Difference in points between white and black
    - ΔMobility: Difference in number of available moves
    - ΔProximity: Difference in proximity to valuable squares
    - ΔCenter: Center control advantage
    - NoMoves: Penalty for having no legal moves

Weights (w₁, w₂, w₃, w₄, w₅):
    w₁ = 100  (Score difference - most important)
    w₂ = 10   (Mobility - strategic advantage)
    w₃ = 5    (Proximity to valuable squares)
    w₄ = 3    (Center control bonus)
    w₅ = -400 (No-moves penalty)

Complexity Analysis:
===================
Time Complexity: O(n + m)
    - n = number of valuable squares on board (max 10)
    - m = number of legal moves per knight (max 8)

Space Complexity: O(1)
    - Uses constant auxiliary space regardless of board size

Justification:
=============
The weight distribution prioritizes immediate point gains (w₁) while
considering strategic positioning (w₂, w₃, w₄). The heavy no-moves penalty
(w₅) strongly discourages positions that lead to being trapped.

Example Usage:
=============
>>> from smart_backend.core.game_state import GameState
>>> game = GameState('beginner')
>>> score = evaluate_game_state(game)
>>> print(f"Position evaluation: {score}")
Position evaluation: 153.5

Author: Smart Horses Team
Universidad del Valle - Inteligencia Artificial
"""

from typing import Dict, Tuple, Optional
from smart_backend.core.move_generator import count_valid_moves
from smart_backend.core.board_manager import (
    manhattan_distance,
    is_center_position,
    get_valuable_squares,
)


def evaluate_game_state(game_state) -> float:
    """
    Evaluate how favorable the game state is for the machine (white).

    This is the core heuristic function used by Minimax to assess positions.
    It evaluates the game state from the perspective of the white player
    (machine). Positive values favor white, negative values favor black.

    Mathematical Implementation:
    ===========================
    H(s) = 100·(S_w - S_b) + 10·(M_w - M_b) + 5·(P_w - P_b) + 3·(C_w - C_b) - 400·N_w + 400·N_b

    Where:
        S_w, S_b: Scores for white and black
        M_w, M_b: Number of legal moves for white and black
        P_w, P_b: Proximity values to valuable squares
        C_w, C_b: Center control (1 if in center, 0 otherwise)
        N_w, N_b: No-moves indicator (1 if no moves, 0 otherwise)

    Evaluation Factors (in order of importance):
    ============================================

    1. **Terminal States** (Weight: ±10,000)
       - Victory: +10,000 (white wins)
       - Defeat: -10,000 (black wins)
       - Tie: 0 (equal scores)
       Purpose: Absolute values for game-ending positions

    2. **Score Difference** (Weight: 100)
       - Formula: (white_score - black_score) × 100
       - Most important factor in non-terminal states
       - Directly reflects point advantage
       - Example: If white has 15 points and black has 8:
         Contribution = (15 - 8) × 100 = 700

    3. **Mobility** (Weight: 10)
       - Formula: (white_moves - black_moves) × 10
       - More moves = more flexibility and strategic options
       - Encourages positions with high mobility
       - Example: If white has 6 moves and black has 4:
         Contribution = (6 - 4) × 10 = 20

    4. **Proximity to Valuable Squares** (Weight: 5)
       - Formula: Σ(value / distance) for each valuable square
       - Measures strategic positioning near high-value squares
       - Closer distance = higher value
       - Being on square: value × 2
       - Example: Square with value +10 at distance 3:
         Contribution = 10 / 3 ≈ 3.33 per square

    5. **Center Control** (Weight: 3)
       - Center positions: (3,3), (3,4), (4,3), (4,4)
       - Bonus for occupying center (better mobility)
       - +3 for white in center, -3 for black in center

    6. **No-Move Penalty** (Weight: -400)
       - Heavy penalty if a player has no legal moves
       - Represents being trapped or stuck
       - -400 for white with no moves (4 points × 100)
       - +400 if opponent has no moves

    Args:
        game_state: Current game state object containing:
            - board: Dictionary of board positions and values
            - white_knight: Tuple (row, col) for white position
            - black_knight: Tuple (row, col) for black position
            - white_score: Integer score for white
            - black_score: Integer score for black
            - game_over: Boolean indicating if game ended
            - winner: String ('white', 'black', 'tie', or None)

    Returns:
        float: Evaluation score
            - Positive values favor white (machine)
            - Negative values favor black (human)
            - Range: [-10,000, +10,000] for terminal states
            - Range: typically [-1000, +1000] for mid-game

    Complexity:
        Time: O(n + m) where n = valuable squares (≤10), m = moves (≤8)
        Space: O(1) constant auxiliary space

    Example:
        >>> game = GameState('beginner')
        >>> eval_score = evaluate_game_state(game)
        >>> if eval_score > 0:
        ...     print("White (machine) has advantage")
        >>> elif eval_score < 0:
        ...     print("Black (human) has advantage")
        >>> else:
        ...     print("Position is equal")

        Example calculation for mid-game position:
        ==========================================
        Given:
            - White Score: 15, Black Score: 8  → ΔScore = 7
            - White Moves: 6, Black Moves: 4   → ΔMobility = 2
            - White Proximity: 10, Black: 7    → ΔProximity = 3
            - White in Center: Yes (1)         → ΔCenter = 1
            - No penalties                     → NoMoves = 0

        Calculation:
            H(s) = 100·7 + 10·2 + 5·3 + 3·1 + 0
                 = 700 + 20 + 15 + 3
                 = 738

        Interpretation: Strong advantage for white (machine)

    Notes:
        - Heuristic is non-perfect by design (allows strategic exploration)
        - Values are tuned for 8×8 board with knight movement
        - Weights can be adjusted for different playing styles
    """
    # Terminal state (game over)
    if game_state.game_over:
        if game_state.winner == "white":
            return 10000  # Victory
        elif game_state.winner == "black":
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


def evaluate_move_quality(game_state, move: Tuple[int, int], player: str) -> float:
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
    if square_value and square_value != "destroyed" and isinstance(square_value, int):
        score += square_value * 10  # Weight for immediate gain

    # Center bonus
    if is_center_position(move):
        score += 5

    # Mobility after move (estimated)
    # This is a simplified estimate without actually making the move
    from smart_backend.core.move_generator import get_knight_moves

    future_moves = get_knight_moves(move)
    available_future_moves = sum(
        1 for m in future_moves if game_state.board.get(m) != "destroyed"
    )
    score += available_future_moves * 2

    return score


def describe_heuristic() -> str:
    """
    Return a textual description of the heuristic function for documentation.

    This function provides a human-readable explanation of the evaluation
    function, including the formula, weights, and interpretation. Useful
    for presentations, documentation, and understanding AI decisions.

    Returns:
        str: Detailed description of the heuristic function

    Example:
        >>> description = describe_heuristic()
        >>> print(description)
        Heuristic Function for Smart Horses
        ...
    """
    return """
╔══════════════════════════════════════════════════════════════════════════╗
║              HEURISTIC FUNCTION FOR SMART HORSES                         ║
╚══════════════════════════════════════════════════════════════════════════╝

Mathematical Formula:
────────────────────
H(s) = w₁·ΔScore + w₂·ΔMobility + w₃·ΔProximity + w₄·ΔCenter + w₅·NoMoves

Components:
──────────
1. ΔScore (w₁ = 100)
   • Score difference between white and black players
   • Most important factor - directly reflects point advantage
   • Formula: (white_score - black_score) × 100

2. ΔMobility (w₂ = 10)
   • Difference in number of available legal moves
   • More moves = better strategic flexibility
   • Formula: (white_moves - black_moves) × 10

3. ΔProximity (w₃ = 5)
   • Distance to valuable squares (high-point squares)
   • Closer to valuable squares = better positioning
   • Formula: Σ(square_value / distance) for each valuable square

4. ΔCenter (w₄ = 3)
   • Center control advantage (positions 3,3 / 3,4 / 4,3 / 4,4)
   • Center positions offer better mobility
   • Formula: +3 if white in center, -3 if black in center

5. NoMoves Penalty (w₅ = -400)
   • Heavy penalty for having no legal moves (trapped)
   • Encourages maintaining mobility
   • Formula: -400 if white has no moves, +400 if black has no moves

Terminal States:
───────────────
• White Victory:  +10,000
• Black Victory:  -10,000
• Tie:            0

Complexity:
──────────
• Time: O(n + m) where n = valuable squares (≤10), m = moves (≤8)
• Space: O(1) constant

Weight Justification:
────────────────────
w₁ >> w₂ > w₃ > w₄ > w₅

• Points (w₁=100) are paramount - winning is about score
• Mobility (w₂=10) is strategic - allows future opportunities
• Proximity (w₃=5) is tactical - prepares for point capture
• Center (w₄=3) is positional - slight advantage
• No-moves (w₅=-400) is critical - avoid being trapped

Example Calculation:
──────────────────
Given position:
  White Score: 15, Black Score: 8
  White Moves: 6, Black Moves: 4
  White Proximity: 10, Black Proximity: 7
  White in center: Yes

Calculation:
  H(s) = 100(15-8) + 10(6-4) + 5(10-7) + 3(1) + 0
       = 700 + 20 + 15 + 3
       = 738 points

Interpretation: Strong advantage for white (machine)

╚══════════════════════════════════════════════════════════════════════════╝
Universidad del Valle - Inteligencia Artificial
Smart Horses Team: Andrey Quiceno, Ivan Ausecha, Jonathan Aristizabal, Jose Martínez
"""
