from flask import Flask
import os

def create_app():
    # Determine the correct path to the 'frontend' directory relative to this file
    # backend/app/__init__.py -> ../../frontend
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend'))
    
    app = Flask(__name__, 
                template_folder=os.path.join(frontend_dir, 'templates'),
                static_folder=os.path.join(frontend_dir, 'static'))

    from . import routes
    app.register_blueprint(routes.bp)

    return app
