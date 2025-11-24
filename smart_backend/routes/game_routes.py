"""
Game routes for Smart Horses API.
"""

from flask import Blueprint, request, jsonify
from smart_backend.core.game_state import GameState
from smart_backend.algorithms.minimax import find_best_move

game_bp = Blueprint("game", __name__)


@game_bp.route("/new", methods=["POST"])
def new_game():
    """
    Create a new game.

    POST /api/game/new
    Body: {
        "difficulty": "beginner" | "amateur" | "expert"
    }

    Returns:
        New game state with machine's first move
    """
    try:
        data = request.get_json() or {}
        difficulty = data.get("difficulty", "beginner")

        # Validate difficulty
        if difficulty not in ["beginner", "amateur", "expert"]:
            return (
                jsonify(
                    {
                        "error": "Invalid difficulty",
                        "message": "Difficulty must be beginner, amateur, or expert",
                    }
                ),
                400,
            )

        # Create new game
        game_state = GameState(difficulty=difficulty)

        # Machine (white) makes first move
        result = find_best_move(game_state)

        if result.move:
            game_state.make_move("white", result.move)

        response = game_state.to_dict()
        response["message"] = "Juego iniciado. La máquina (blancas) ha movido."
        response["machine_first_move"] = list(result.move) if result.move else None

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@game_bp.route("/move", methods=["POST"])
def player_move():
    """
    Process player move and get machine response.

    POST /api/game/move
    Body: {
        "game_state": {...},
        "move": [row, col]
    }

    Returns:
        Updated game state with machine's response move
    """
    try:
        data = request.get_json()

        if not data:
            return (
                jsonify({"error": "Bad Request", "message": "No JSON data provided"}),
                400,
            )

        if "game_state" not in data or "move" not in data:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": "Missing required fields: game_state, move",
                    }
                ),
                400,
            )

        # Reconstruct game state
        game_state = GameState.from_dict(data["game_state"])
        player_move_pos = tuple(data["move"])

        # Validate it's player's turn
        if game_state.current_player != "black":
            return (
                jsonify({"error": "Invalid Move", "message": "Not player's turn"}),
                400,
            )

        # Validate move is valid
        valid_moves = game_state.get_valid_moves("black")
        if player_move_pos not in valid_moves:
            return (
                jsonify(
                    {
                        "error": "Invalid Move",
                        "message": "This is not a valid move",
                        "valid_moves": [list(m) for m in valid_moves],
                    }
                ),
                400,
            )

        # Make player move
        move_result = game_state.make_move("black", player_move_pos)

        # Check if game over after player move
        if game_state.game_over:
            response = game_state.to_dict()
            response["message"] = f"¡Juego terminado! Ganador: {game_state.winner}"
            response["machine_move"] = None
            return jsonify(response), 200

        # Machine's turn
        machine_result = find_best_move(game_state)

        if machine_result.move:
            game_state.make_move("white", machine_result.move)
            machine_move = list(machine_result.move)
        else:
            machine_move = None

        # Prepare response
        response = game_state.to_dict()
        response["machine_move"] = machine_move
        response["machine_evaluation"] = machine_result.evaluation
        response["nodes_evaluated"] = machine_result.nodes_evaluated

        if game_state.game_over:
            response["message"] = f"¡Juego terminado! Ganador: {game_state.winner}"
        else:
            response["message"] = "Turno del jugador (negras)"

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@game_bp.route("/valid-moves", methods=["POST"])
def get_valid_moves():
    """
    Get valid moves for a knight.

    POST /api/game/valid-moves
    Body: {
        "game_state": {...},
        "knight": "white" | "black"
    }

    Returns:
        List of valid moves
    """
    try:
        data = request.get_json()

        if not data or "game_state" not in data:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": "Missing required field: game_state",
                    }
                ),
                400,
            )

        game_state = GameState.from_dict(data["game_state"])
        knight = data.get("knight", "black")

        if knight not in ["white", "black"]:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": 'Knight must be "white" or "black"',
                    }
                ),
                400,
            )

        valid_moves = game_state.get_valid_moves(knight)

        return (
            jsonify(
                {
                    "knight": knight,
                    "position": list(
                        game_state.white_knight
                        if knight == "white"
                        else game_state.black_knight
                    ),
                    "valid_moves": [list(move) for move in valid_moves],
                    "count": len(valid_moves),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@game_bp.route("/machine-move", methods=["POST"])
def get_machine_move():
    """
    Get best move for machine without applying it.

    POST /api/game/machine-move
    Body: {
        "game_state": {...}
    }

    Returns:
        Best move and evaluation
    """
    try:
        data = request.get_json()

        if not data or "game_state" not in data:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": "Missing required field: game_state",
                    }
                ),
                400,
            )

        game_state = GameState.from_dict(data["game_state"])

        # Find best move
        result = find_best_move(game_state)

        return (
            jsonify(
                {
                    "move": list(result.move) if result.move else None,
                    "evaluation": result.evaluation,
                    "nodes_evaluated": result.nodes_evaluated,
                    "depth_reached": result.depth_reached,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
