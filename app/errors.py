"""
Error handlers for the application
"""
from flask import render_template, current_app

def register_error_handlers(app):
    """Register error handlers with the Flask app"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors"""
        current_app.logger.warning(f"404 error: {error}")
        return render_template('error.html', 
                             error_message="Page not found."), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        current_app.logger.error(f"500 error: {error}")
        return render_template('error.html', 
                             error_message="Database connection error. Please check your internet connection and try again."), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle 403 errors"""
        current_app.logger.warning(f"403 error: {error}")
        return render_template('error.html', 
                             error_message="Access forbidden."), 403

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle unhandled exceptions"""
        current_app.logger.error(f"Unhandled exception: {error}")
        return render_template('error.html', 
                             error_message="An unexpected error occurred. Please try again."), 500 