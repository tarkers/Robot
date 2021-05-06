from flask import Flask ,Blueprint
from flask_sqlalchemy import SQLAlchemy
from api.config import Config
def init_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)   
    from .routes.music import music
    # app.register_blueprint(music,url_prefix='/music',static_folder='static',template_folder='templates')
    app.register_blueprint(music)

    with app.app_context():  
        # db.create_all()  # Create sql tables for our data models
        return app 
app=init_app()
# db.create_all()