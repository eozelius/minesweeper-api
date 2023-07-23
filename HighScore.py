import json

class HighScore:
  def __init__(self, name, score, time):
    self.name = name
    self.score = score
    self.time = time
  
  def to_json(self):
    return json.dumps(self, default=lambda o: o.__dict__)
