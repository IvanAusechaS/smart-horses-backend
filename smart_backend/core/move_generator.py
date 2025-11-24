"""
Move generator for knight pieces.
"""

from typing import List, Tuple, Dict, Optional


# Knight moves in L-shape
KNIGHT_MOVES = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]


def get_knight_moves(position: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Generate all possible knight moves from a position.

    Args:
        position: Current position (row, col)

    Returns:
        List of possible positions within 8x8 board
    """
    row, col = position
    moves = []

    for dr, dc in KNIGHT_MOVES:
        new_row, new_col = row + dr, col + dc

        # Check if within board bounds
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            moves.append((new_row, new_col))

    return moves


def get_valid_moves(
    knight_position: Tuple[int, int], board: Dict[Tuple[int, int], Optional[str | int]]
) -> List[Tuple[int, int]]:
    """
    Get valid moves for a knight (not destroyed squares).

    Args:
        knight_position: Current knight position
        board: Game board dictionary

    Returns:
        List of valid positions (not destroyed)
    """
    all_moves = get_knight_moves(knight_position)

    # Filter out destroyed squares
    valid_moves = [move for move in all_moves if board.get(move) != "destroyed"]

    return valid_moves


def count_valid_moves(
    knight_position: Tuple[int, int], board: Dict[Tuple[int, int], Optional[str | int]]
) -> int:
    """
    Count the number of valid moves for a knight.

    Args:
        knight_position: Current knight position
        board: Game board dictionary

    Returns:
        Number of valid moves
    """
    return len(get_valid_moves(knight_position, board))
