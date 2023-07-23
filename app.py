import sys
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from HighScore import HighScore

high_scores = []
app = Flask(__name__)
cors = CORS(app, resources={r"/high-scores": {"origins": "https://minesweeper.ethanoz.com"}})
cors = CORS(app, resources={r"/save-high-score": {"origins": "https://minesweeper.ethanoz.com"}})

# Retrieve all High Scores
@app.get('/high-scores')
def get_high_scores():
  my_scores = jsonify_high_scores()
  return jsonify(my_scores)

# Save a High Score
@app.post('/save-high-score')
def save_high_score():
  try:
    name = request.json['name']
    time = request.json['time']
    score = request.json['score']
    new_high_score = HighScore(name, score, time)
    high_scores.append(new_high_score)

    return jsonify({
      'code': 200,
      'message': 'success'
    })
  except:
    error = sys.exc_info()[0]
    app.logger.error('error => %s', error)
    return jsonify({
      'code': 400,
      'message': 'Error, unable to process request'
    })

def jsonify_high_scores():
  scores_to_return = []
  for s in high_scores:
    scores_to_return.append(s.to_json())
  return scores_to_return

if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = 443, debug = True)