import sys
import traceback

from flask import (
  Blueprint,
  current_app,
  jsonify,
  Response,
  request,
)

from database import db
from models.HighScore import HighScore

high_scores_route = Blueprint("high_scores_route", __name__, url_prefix="/high-scores")

@high_scores_route.route('', methods=["GET"])
def get_high_scores() -> Response:
  """
    Retrieve all the high scores in the database.
    :return: json list of all high scores
  """
  high_scores = HighScore.query.all()
  return jsonify([ hs.serialize for hs in high_scores ])


@high_scores_route.route('', methods=["POST"])
def post_high_scores() -> Response:
  """
    Save a new high score.
    :return: json object containing success/failure info.
  """
  try:
    high_score_request_data: dict = request.get_json(silent=True)

    # basic error checking request
    if None in [
      high_score_request_data.get('initials'),
      high_score_request_data.get('time'),
    ]:
      current_app.logger.error('invalid request, missing arguments')
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
    current_app.logger.error('error => %s', error)
    traceback.print_exc()
    return jsonify({
      'code': 400,
      'message': 'Error, unable to process request'
    })