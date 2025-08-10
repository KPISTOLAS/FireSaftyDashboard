"""
Main application entry point
"""
import os
import logging
from app import create_app
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main application entry point"""
    # Get configuration from environment
    config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    # Create application instance
    app = create_app(config_name)
    
    # Get configuration
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', False)
    
    # Run the application
    app.logger.info(f"Starting Fire Detection Dashboard System on {host}:{port}")
    app.logger.info(f"Debug mode: {debug}")
    app.logger.info(f"Configuration: {config_name}")
    
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main() 