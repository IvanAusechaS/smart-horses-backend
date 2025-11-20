"""
Entry point for running the Flask application.
"""

import os
from smart_backend.app import create_app

# Get environment from environment variable
env = os.getenv('FLASK_ENV', 'development')

# Create the Flask app
app = create_app(env)

if __name__ == '__main__':
    config = app.config
    
    print(f"\n{'='*60}")
    print(f"  Smart Horses Backend - {env.upper()} Mode")
    print(f"{'='*60}")
    print(f"  Running on: http://{config['HOST']}:{config['PORT']}")
    print(f"  Debug mode: {config['DEBUG']}")
    print(f"  CORS Origins: {', '.join(config['CORS_ORIGINS'])}")
    print(f"{'='*60}\n")
    
    app.run(
        host=config['HOST'],
        port=config['PORT'],
        debug=config['DEBUG']
    )
