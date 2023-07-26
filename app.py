import os
import sys
import traceback

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'minesweeper-api.db')
db = SQLAlchemy()
db.init_app(app)

# CORS
cors = CORS(
  app,
  resources={r"/high-scores": {
    "origins": [
      "https://minesweeper.ethanoz.com",
      'http://localhost:8080'
    ]
  }}
)

# Models
class HighScore(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  initials = db.Column(db.String, unique=False, nullable=False)
  score = db.Column(db.Integer, unique=False, nullable=False)
  time = db.Column(db.Integer, unique=False, nullable=False)
  created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
  updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())

  def __repr__(self):
    return f'<HighScore id: {self.id}; initials: {self.initials}; score: {self.score}; time: {self.time}; created_at: {self.created_at}; updated_at: {self.updated_at};>'

  @property
  def serialize(self):
    return {
      'id': self.id,
      'initials': self.initials,
      'score': self.score,
      'time': self.time,
      'created_at': f'{self.created_at}',
      'updated_at': f'{self.updated_at}'
    }

# Retrieve all High Scores
@app.get('/high-scores')
def get_high_scores():
  high_scores = HighScore.query.all()
  return jsonify([ hs.serialize for hs in high_scores ])

# Save a High Score
@app.post('/high-scores')
def save_high_score():
  try:
    high_score_request_data: dict = request.get_json(silent=True)

    # basic error checking request
    if None in [
      high_score_request_data.get('initials'),
      high_score_request_data.get('time'),
    ]:
      app.logger.error('invalid request, missing arguments')
      return jsonify({
        'code': 400,
        'message': 'invalid request, missing required args: "initials", "time" and/or "score"'
      })

    new_high_score = HighScore(
      initials=high_score_request_data.get('initials'),
      time=high_score_request_data.get('time'),
      score=high_score_request_data.get('score')
    )

    db.session.add(new_high_score)
    db.session.commit()

    return jsonify({
      'code': 200,
      'message': 'success',
      'high_score': new_high_score.serialize
    })
  except:
    db.session.rollback()
    error = sys.exc_info()[0]
    app.logger.error('error => %s', error)
    traceback.print_exc()
    return jsonify({
      'code': 400,
      'message': 'Error, unable to process request'
    })

if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = 443, debug = True)