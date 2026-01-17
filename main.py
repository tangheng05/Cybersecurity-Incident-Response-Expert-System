import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Only enable debug mode in development
    debug_mode = os.environ.get('FLASK_ENV') == 'development' or os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)