"""
Game state representation for Smart Horses.
"""

from typing import Dict, Tuple, Optional, List
import random


class GameState:
    """
    Represents the complete state of the Smart Horses game.
    
    Attributes:
        board: dict {(row, col): value}
            - None: casilla vacía disponible
            - 'destroyed': casilla destruida
            - -10, -5, -4, -3, -1, +1, +3, +4, +5, +10: casillas con puntos
        
        white_knight: tuple (row, col) - Máquina
        black_knight: tuple (row, col) - Jugador humano
        
        white_score: int
        black_score: int
        
        current_player: 'white' | 'black'
        
        difficulty: 'beginner' | 'amateur' | 'expert'
        max_depth: int (2, 4, o 6 según dificultad)
        
        game_over: bool
        winner: 'white' | 'black' | 'tie' | None
    """
    
    def __init__(self, difficulty: str = 'beginner'):
        """
        Initialize a new game state.
        
        Args:
            difficulty: 'beginner', 'amateur', or 'expert'
        """
        self.board: Dict[Tuple[int, int], Optional[str | int]] = {}
        self.white_knight: Tuple[int, int] = (0, 0)
        self.black_knight: Tuple[int, int] = (7, 7)
        self.white_score: int = 0
        self.black_score: int = 0
        self.current_player: str = 'white'  # Máquina empieza
        self.difficulty: str = difficulty
        self.max_depth: int = self._get_max_depth(difficulty)
        self.game_over: bool = False
        self.winner: Optional[str] = None
        
        self._initialize_board()
    
    def _get_max_depth(self, difficulty: str) -> int:
        """Get max depth based on difficulty."""
        depths = {
            'beginner': 2,
            'amateur': 4,
            'expert': 6
        }
        return depths.get(difficulty, 2)
    
    def _initialize_board(self):
        """
        Initialize board with random special squares.
        
        Distribution:
        - 4 casillas +10
        - 4 casillas +5
        - 4 casillas +4
        - 4 casillas +3
        - 4 casillas +1
        - 4 casillas -1
        - 4 casillas -3
        - 4 casillas -4
        - 4 casillas -5
        - 4 casillas -10
        - Resto: None (vacías)
        """
        # Initialize all squares as empty
        for row in range(8):
            for col in range(8):
                self.board[(row, col)] = None
        
        # Define special values and their counts
        special_values = [
            (10, 4), (5, 4), (4, 4), (3, 4), (1, 4),
            (-1, 4), (-3, 4), (-4, 4), (-5, 4), (-10, 4)
        ]
        
        # Get all positions
        all_positions = [(r, c) for r in range(8) for c in range(8)]
        
        # Place knights first
        white_pos = random.choice(all_positions)
        all_positions.remove(white_pos)
        black_pos = random.choice(all_positions)
        all_positions.remove(black_pos)
        
        self.white_knight = white_pos
        self.black_knight = black_pos
        
        # Place special squares
        for value, count in special_values:
            for _ in range(count):
                if all_positions:
                    pos = random.choice(all_positions)
                    all_positions.remove(pos)
                    self.board[pos] = value
    
    def get_valid_moves(self, knight: str) -> List[Tuple[int, int]]:
        """
        Get valid moves for a knight.
        
        Args:
            knight: 'white' or 'black'
            
        Returns:
            List of valid positions (not destroyed)
        """
        from smart_backend.core.move_generator import get_valid_moves
        
        position = self.white_knight if knight == 'white' else self.black_knight
        return get_valid_moves(position, self.board)
    
    def make_move(self, knight: str, new_position: Tuple[int, int]) -> Dict:
        """
        Make a move and update game state.
        
        Args:
            knight: 'white' or 'black'
            new_position: Target position (row, col)
            
        Returns:
            Dict with move result information
        """
        old_position = self.white_knight if knight == 'white' else self.black_knight
        
        # Get square value
        square_value = self.board.get(new_position, 0)
        if square_value == 'destroyed':
            return {
                'valid': False,
                'error': 'Cannot move to destroyed square'
            }
        
        # Update knight position
        if knight == 'white':
            self.white_knight = new_position
        else:
            self.black_knight = new_position
        
        # Collect points
        points_gained = 0
        if square_value and square_value != 'destroyed':
            points_gained = square_value
            if knight == 'white':
                self.white_score += points_gained
            else:
                self.black_score += points_gained
        
        # Destroy the square
        self.board[old_position] = 'destroyed'
        
        # Switch player
        self.current_player = 'black' if knight == 'white' else 'white'
        
        # Check for game over
        self._check_game_over()
        
        return {
            'valid': True,
            'points_gained': points_gained,
            'new_position': new_position,
            'square_destroyed': old_position
        }
    
    def _check_game_over(self):
        """Check if game is over and determine winner."""
        white_moves = self.get_valid_moves('white')
        black_moves = self.get_valid_moves('black')
        
        # Check if either player has no moves
        if not white_moves or not black_moves:
            self.game_over = True
            
            # Apply penalty if one has moves and other doesn't
            if not white_moves and black_moves:
                self.white_score -= 4
            elif white_moves and not black_moves:
                self.black_score -= 4
            
            # Determine winner
            if self.white_score > self.black_score:
                self.winner = 'white'
            elif self.black_score > self.white_score:
                self.winner = 'black'
            else:
                self.winner = 'tie'
    
    def to_dict(self) -> Dict:
        """Convert game state to dictionary for JSON serialization."""
        # Convert board to serializable format
        board_dict = {}
        for pos, value in self.board.items():
            key = f"{pos[0]},{pos[1]}"
            board_dict[key] = value
        
        return {
            'board': board_dict,
            'white_knight': list(self.white_knight),
            'black_knight': list(self.black_knight),
            'white_score': self.white_score,
            'black_score': self.black_score,
            'current_player': self.current_player,
            'difficulty': self.difficulty,
            'max_depth': self.max_depth,
            'game_over': self.game_over,
            'winner': self.winner
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GameState':
        """Create GameState from dictionary."""
        game = cls.__new__(cls)
        
        # Convert board back from string keys
        game.board = {}
        for key, value in data['board'].items():
            row, col = map(int, key.split(','))
            game.board[(row, col)] = value
        
        game.white_knight = tuple(data['white_knight'])
        game.black_knight = tuple(data['black_knight'])
        game.white_score = data['white_score']
        game.black_score = data['black_score']
        game.current_player = data['current_player']
        game.difficulty = data['difficulty']
        game.max_depth = data['max_depth']
        game.game_over = data['game_over']
        game.winner = data.get('winner')
        
        return game
    
    def copy(self) -> 'GameState':
        """Create a deep copy of the game state."""
        return GameState.from_dict(self.to_dict())
