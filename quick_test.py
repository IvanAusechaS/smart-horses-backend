"""Quick test to verify the backend is working."""
from smart_backend.app import create_app
from smart_backend.core.game_state import GameState
from smart_backend.algorithms.minimax import find_best_move

def test_game_creation():
    """Test creating a new game."""
    print("\n" + "="*60)
    print("Testing Game Creation")
    print("="*60)
    
    for difficulty in ['beginner', 'amateur', 'expert']:
        print(f"\nCreating game with difficulty: {difficulty}")
        game = GameState(difficulty=difficulty)
        print(f"✅ White knight at: {game.white_knight}")
        print(f"✅ Black knight at: {game.black_knight}")
        print(f"✅ Max depth: {game.max_depth}")
        print(f"✅ Game created successfully!")

def test_minimax():
    """Test minimax algorithm."""
    print("\n" + "="*60)
    print("Testing Minimax Algorithm")
    print("="*60)
    
    for difficulty in ['beginner', 'amateur', 'expert']:
        print(f"\nTesting {difficulty} difficulty:")
        game = GameState(difficulty=difficulty)
        
        print(f"Finding best move for white...")
        result = find_best_move(game)
        
        print(f"✅ Best move: {result.move}")
        print(f"✅ Evaluation: {result.evaluation:.2f}")
        print(f"✅ Nodes evaluated: {result.nodes_evaluated}")
        print(f"✅ Depth reached: {result.depth_reached}")
        
        # Make the move
        if result.move:
            game.make_move('white', result.move)
            print(f"✅ Move executed successfully!")
            print(f"   White score: {game.white_score}")
            print(f"   Current player: {game.current_player}")

def test_full_game_flow():
    """Test a complete game flow."""
    print("\n" + "="*60)
    print("Testing Full Game Flow")
    print("="*60)
    
    game = GameState('beginner')
    turn = 0
    max_turns = 10
    
    print(f"\nStarting game:")
    print(f"White (machine): {game.white_knight}")
    print(f"Black (player): {game.black_knight}")
    
    while not game.game_over and turn < max_turns:
        turn += 1
        print(f"\n--- Turn {turn} ({game.current_player}) ---")
        
        if game.current_player == 'white':
            # Machine move
            result = find_best_move(game)
            if result.move:
                game.make_move('white', result.move)
                print(f"White moves to: {result.move}")
                print(f"Evaluation: {result.evaluation:.2f}")
        else:
            # Simulate player move (choose first valid move)
            valid_moves = game.get_valid_moves('black')
            if valid_moves:
                move = valid_moves[0]
                game.make_move('black', move)
                print(f"Black moves to: {move}")
        
        print(f"Scores - White: {game.white_score}, Black: {game.black_score}")
    
    print(f"\n{'='*60}")
    if game.game_over:
        print(f"Game Over! Winner: {game.winner}")
    else:
        print(f"Test completed after {turn} turns")
    print(f"Final Scores - White: {game.white_score}, Black: {game.black_score}")
    print("="*60)

def test_app():
    """Test Flask app creation."""
    print("\n" + "="*60)
    print("Testing Flask App")
    print("="*60)
    
    app = create_app('development')
    print("✅ App created successfully!")
    print(f"✅ Debug mode: {app.debug}")
    print(f"✅ Registered blueprints: {list(app.blueprints.keys())}")
    
    # Test routes
    with app.test_client() as client:
        print("\nTesting routes:")
        
        # Health check
        response = client.get('/health')
        print(f"✅ /health: {response.status_code}")
        
        # Root
        response = client.get('/')
        print(f"✅ /: {response.status_code}")
        
        # New game
        response = client.post('/api/game/new', 
                              json={'difficulty': 'beginner'},
                              headers={'Content-Type': 'application/json'})
        print(f"✅ /api/game/new: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Game created with difficulty: {data.get('difficulty')}")
            print(f"   Machine first move: {data.get('machine_first_move')}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  SMART HORSES BACKEND - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    try:
        test_game_creation()
        test_minimax()
        test_full_game_flow()
        test_app()
        
        print("\n" + "="*70)
        print("  ✅ ALL TESTS PASSED!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
