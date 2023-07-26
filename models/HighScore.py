from sqlalchemy.sql import func

from database import db

class HighScore(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  initials = db.Column(db.String, unique=False, nullable=False)
  score = db.Column(db.Integer, unique=False, nullable=False)
  time = db.Column(db.Integer, unique=False, nullable=False)
  created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
  updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())

  def __repr__(self):
    return f'<HighScore id: "{self.id}"; initials: "{self.initials}"; score: "{self.score}"; time: "{self.time}"; created_at: "{self.created_at}"; updated_at: "{self.updated_at}";>'

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