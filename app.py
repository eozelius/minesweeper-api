import os

from flask import Flask
from flask_cors import CORS

from database import db
from config import config
from routes.highScore import high_scores_route

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(config_name) -> Flask:
  application = Flask(__name__)

  # Config
  application.config.from_object(config[config_name])

  # Routes
  application.register_blueprint(high_scores_route)

  # SQLAlchemy
  application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'minesweeper-api.db')
  db.init_app(application)

  # CORS
  CORS(
    application,
    resources={r"/high-scores": {
      "origins": [
        "https://minesweeper.ethanoz.com",
        'http://localhost:8080'
      ]
    }}
  )

  return application


flask_env = os.getenv("FLASK_ENV") or "local"
app = create_app(flask_env)
