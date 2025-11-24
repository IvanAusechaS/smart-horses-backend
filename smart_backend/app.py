"""
Main Flask application factory.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from smart_backend.config import get_config
from smart_backend.routes.game_routes import game_bp


def create_app(config_name=None):
    """
    Create and configure the Flask application.

    Args:
        config_name: Configuration name ('development' or 'production')

    Returns:
        Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)

    # Enable CORS with proper configuration
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": config.CORS_ORIGINS,
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "expose_headers": ["Content-Type"],
                "supports_credentials": True,
                "max_age": 3600,
            }
        },
    )

    # Register blueprints
    app.register_blueprint(game_bp, url_prefix="/api/game")

    # Health check endpoint
    @app.route("/")
    def index():
        return jsonify(
            {
                "status": "ok",
                "message": "Smart Horses Backend API",
                "game": "Smart Horses - Minimax AI Game",
                "version": "1.0.0",
                "endpoints": {
                    "health": "/health",
                    "new_game": "/api/game/new",
                    "move": "/api/game/move",
                    "valid_moves": "/api/game/valid-moves",
                    "machine_move": "/api/game/machine-move",
                },
            }
        )

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy", "service": "smart-horses-backend"})

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "error": "Not Found",
                    "message": "The requested resource was not found",
                }
            ),
            404,
        )

    @app.errorhandler(500)
    def internal_error(error):
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "An internal error occurred",
                }
            ),
            500,
        )

    return app
