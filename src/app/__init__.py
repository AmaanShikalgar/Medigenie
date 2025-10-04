from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    from .routes import med_bp
    app.register_blueprint(med_bp)
    return app
