import os
from app import create_app

env_name = os.getenv('FLASK_ENV', 'development')

app = create_app()

if __name__ == "__main__":
    app.run(port=5555, debug=True)