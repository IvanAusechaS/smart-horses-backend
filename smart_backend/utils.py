"""
Utility functions for the Smart Horses Backend.
"""

from typing import List, Tuple


def format_board(board: List[List[int]]) -> str:
    """
    Format a board for display.
    
    Args:
        board: 2D list representing the board
        
    Returns:
        Formatted string representation
    """
    size = len(board)
    max_digits = len(str(size * size - 1))
    
    lines = []
    for row in board:
        formatted_row = ' '.join(f'{cell:>{max_digits}}' if cell >= 0 else ' .' * max_digits for cell in row)
        lines.append(formatted_row)
    
    return '\n'.join(lines)


def path_to_board(path: List[Tuple[int, int]], board_size: int) -> List[List[int]]:
    """
    Convert a path to a board representation.
    
    Args:
        path: List of (row, col) positions
        board_size: Size of the board
        
    Returns:
        2D list with move numbers
    """
    board = [[-1 for _ in range(board_size)] for _ in range(board_size)]
    
    for move_num, (row, col) in enumerate(path):
        board[row][col] = move_num
    
    return board


def board_to_path(board: List[List[int]]) -> List[Tuple[int, int]]:
    """
    Convert a board representation to a path.
    
    Args:
        board: 2D list with move numbers
        
    Returns:
        List of (row, col) positions in order
    """
    size = len(board)
    total_moves = size * size
    path = [None] * total_moves
    
    for row in range(size):
        for col in range(size):
            move_num = board[row][col]
            if move_num >= 0:
                path[move_num] = (row, col)
    
    return [pos for pos in path if pos is not None]


def calculate_coverage(path: List[Tuple[int, int]], board_size: int) -> float:
    """
    Calculate the percentage of board covered.
    
    Args:
        path: List of positions
        board_size: Size of the board
        
    Returns:
        Coverage percentage (0-100)
    """
    total_squares = board_size * board_size
    covered = len(set(path))
    return (covered / total_squares) * 100


def is_valid_tour(path: List[Tuple[int, int]], board_size: int) -> bool:
    """
    Check if a path is a valid knight's tour.
    
    Args:
        path: List of positions
        board_size: Size of the board
        
    Returns:
        Boolean indicating if tour is valid
    """
    if len(path) != board_size * board_size:
        return False
    
    # Check all positions are unique
    if len(set(path)) != len(path):
        return False
    
    # Check all moves are valid knight moves
    knight_moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    for i in range(len(path) - 1):
        current = path[i]
        next_pos = path[i + 1]
        
        dr = next_pos[0] - current[0]
        dc = next_pos[1] - current[1]
        
        if (dr, dc) not in knight_moves:
            return False
    
    return True
