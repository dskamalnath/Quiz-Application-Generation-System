from flask import Flask
from flask_mysqldb import MySQL
import os

mysql = MySQL()

def create_app(config_name='development'):
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    from config import config as config_dict
    app.config.from_object(config_dict[config_name])
    
    # Initialize MySQL
    mysql.init_app(app)
    
    # Register blueprints
    from app.routes import auth_bp, teacher_bp, student_bp, quiz_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(quiz_bp)
    
    @app.before_request
    def before_request():
        from flask import session
        session.permanent = True
    
    return app
