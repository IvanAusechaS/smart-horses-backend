"""
Board management utilities.
"""

from typing import Dict, Tuple, Optional, List


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """
    Calculate Manhattan distance between two positions.

    Args:
        pos1: First position (row, col)
        pos2: Second position (row, col)

    Returns:
        Manhattan distance
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def is_center_position(position: Tuple[int, int]) -> bool:
    """
    Check if position is in the center of the board.

    Center positions: (3,3), (3,4), (4,3), (4,4)

    Args:
        position: Position to check (row, col)

    Returns:
        True if in center, False otherwise
    """
    center_positions = [(3, 3), (3, 4), (4, 3), (4, 4)]
    return position in center_positions


def get_valuable_squares(
    board: Dict[Tuple[int, int], Optional[str | int]],
) -> List[Tuple[Tuple[int, int], int]]:
    """
    Get all valuable (positive points) non-destroyed squares.

    Args:
        board: Game board dictionary

    Returns:
        List of tuples: (position, value)
    """
    valuable = []

    for position, value in board.items():
        if value and value != "destroyed" and isinstance(value, int) and value > 0:
            valuable.append((position, value))

    return valuable


def get_board_statistics(board: Dict[Tuple[int, int], Optional[str | int]]) -> Dict:
    """
    Get statistics about the current board state.

    Args:
        board: Game board dictionary

    Returns:
        Dictionary with statistics
    """
    destroyed = 0
    empty = 0
    positive_points = 0
    negative_points = 0
    total_positive_value = 0
    total_negative_value = 0

    for value in board.values():
        if value == "destroyed":
            destroyed += 1
        elif value is None:
            empty += 1
        elif isinstance(value, int):
            if value > 0:
                positive_points += 1
                total_positive_value += value
            else:
                negative_points += 1
                total_negative_value += value

    return {
        "destroyed": destroyed,
        "empty": empty,
        "positive_points": positive_points,
        "negative_points": negative_points,
        "total_positive_value": total_positive_value,
        "total_negative_value": total_negative_value,
        "available_squares": 64 - destroyed,
    }
