from flask import Flask
from flask_caching import Cache
from config import config

# Initialize cache
cache = Cache()

def create_app(config_name='default'):
    """Application factory pattern"""
    # Point Flask to the project's shared static and templates directories
    app = Flask(
        __name__,
        static_folder='../static',
        template_folder='../templates'
    )
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    cache.init_app(app)
    
    # Register blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # Register error handlers
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    return app 