"""
Validation functions for API requests.
"""

from smart_backend.config import Config


def validate_solve_request(data):
    """
    Validate a solve request.

    Args:
        data: Request data dictionary

    Returns:
        Tuple (is_valid, error_message)
    """
    # Check required fields
    if "board_size" not in data:
        return False, "Missing required field: board_size"

    if "start_position" not in data:
        return False, "Missing required field: start_position"

    # Validate board size
    board_size = data["board_size"]
    if not isinstance(board_size, int):
        return False, "board_size must be an integer"

    if board_size < Config.MIN_BOARD_SIZE:
        return False, f"board_size must be at least {Config.MIN_BOARD_SIZE}"

    if board_size > Config.MAX_BOARD_SIZE:
        return False, f"board_size must be at most {Config.MAX_BOARD_SIZE}"

    # Validate start position
    start_position = data["start_position"]
    if not isinstance(start_position, list) or len(start_position) != 2:
        return False, "start_position must be a list of two integers [row, col]"

    row, col = start_position
    if not isinstance(row, int) or not isinstance(col, int):
        return False, "start_position coordinates must be integers"

    if row < 0 or row >= board_size:
        return False, f"start_position row must be between 0 and {board_size - 1}"

    if col < 0 or col >= board_size:
        return False, f"start_position col must be between 0 and {board_size - 1}"

    # Validate algorithm if provided
    if "algorithm" in data:
        algorithm = data["algorithm"]
        if not isinstance(algorithm, str):
            return False, "algorithm must be a string"

        # We'll check valid algorithms in the service

    # Validate find_all if provided
    if "find_all" in data:
        find_all = data["find_all"]
        if not isinstance(find_all, bool):
            return False, "find_all must be a boolean"

    return True, None


def validate_position(position, board_size):
    """
    Validate a position on the board.

    Args:
        position: Tuple (row, col)
        board_size: Size of the board

    Returns:
        Boolean indicating if position is valid
    """
    row, col = position
    return 0 <= row < board_size and 0 <= col < board_size
