"""
Legacy runner for local development.

This file now delegates to the application factory and blueprints
located under the `app/` package (professional structure).
Use `python run.py` or `flask --app run.py run` in production-like setups.
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Default dev server
    app.run(host=app.config.get('HOST', '0.0.0.0'), port=app.config.get('PORT', 5000), debug=app.config.get('DEBUG', True))