"""
Business logic services for the Smart Horses Backend.
"""

import time
from typing import Tuple, Dict, List, Optional


class KnightTourService:
    """Service for solving the Knight's Tour problem."""
    
    # Available algorithms (you'll implement these in algorithms/)
    AVAILABLE_ALGORITHMS = ['backtracking', 'warnsdorff', 'genetic', 'astar']
    
    def __init__(self):
        """Initialize the service."""
        pass
    
    @staticmethod
    def get_available_algorithms() -> List[str]:
        """Get list of available algorithms."""
        return KnightTourService.AVAILABLE_ALGORITHMS
    
    def solve(
        self,
        board_size: int,
        start_position: Tuple[int, int],
        algorithm: str = 'backtracking',
        find_all: bool = False
    ) -> Dict:
        """
        Solve the Knight's Tour problem.
        
        Args:
            board_size: Size of the board (n x n)
            start_position: Starting position (row, col)
            algorithm: Algorithm to use
            find_all: Whether to find all solutions
            
        Returns:
            Dictionary with solution and metadata
        """
        start_time = time.time()
        
        # Validate algorithm
        if algorithm not in self.AVAILABLE_ALGORITHMS:
            return {
                'success': False,
                'error': f'Unknown algorithm: {algorithm}. Available: {", ".join(self.AVAILABLE_ALGORITHMS)}',
                'execution_time': 0
            }
        
        # TODO: Here you'll call your algorithm implementations
        # For now, return a placeholder response
        
        # This is a placeholder - you'll replace this with actual algorithm calls
        solution = self._placeholder_solution(board_size, start_position)
        
        execution_time = time.time() - start_time
        
        return {
            'success': True,
            'algorithm': algorithm,
            'board_size': board_size,
            'start_position': list(start_position),
            'solution': solution,
            'execution_time': round(execution_time, 4),
            'moves_count': len(solution) if solution else 0,
            'message': 'Solution found successfully' if solution else 'No solution found'
        }
    
    def _placeholder_solution(
        self,
        board_size: int,
        start_position: Tuple[int, int]
    ) -> Optional[List[List[int]]]:
        """
        Placeholder solution generator.
        
        This is a temporary implementation. Replace with actual algorithm calls.
        
        Returns:
            List of moves [[row, col], ...] or None if no solution
        """
        # Simple placeholder: just return the starting position
        # In a real implementation, this would call your algorithm
        return [
            list(start_position),
            # Your algorithm will generate the complete path here
        ]
    
    @staticmethod
    def get_knight_moves() -> List[Tuple[int, int]]:
        """
        Get all possible knight moves (relative positions).
        
        Returns:
            List of (row_delta, col_delta) tuples
        """
        return [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
    
    @staticmethod
    def is_valid_move(
        position: Tuple[int, int],
        board_size: int,
        visited: set
    ) -> bool:
        """
        Check if a move is valid.
        
        Args:
            position: Position to check (row, col)
            board_size: Size of the board
            visited: Set of visited positions
            
        Returns:
            Boolean indicating if move is valid
        """
        row, col = position
        return (
            0 <= row < board_size and
            0 <= col < board_size and
            position not in visited
        )
