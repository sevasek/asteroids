import json
import os
from datetime import date

from constants import LEADERBOARD_MAX_SCORES, LEADERBOARD_MAX_NAME_LENGTH

LEADERBOARD_FILE = "leaderboard.json"


class Leaderboard:
    def __init__(self, filepath=LEADERBOARD_FILE):
        self.filepath = filepath
        self.scores = self._load()

    def _load(self) -> list:
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.scores, f, indent=2)

    def is_high_score(self, score: int) -> bool:
        if not self.scores:
            return True
        if len(self.scores) < LEADERBOARD_MAX_SCORES:
            return True
        return score > self.scores[-1]["score"]

    def add_score(self, name: str, score: int) -> bool:
        name = name[:LEADERBOARD_MAX_NAME_LENGTH].upper()
        self.scores.append({"name": name, "score": score, "date": str(date.today())})
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:LEADERBOARD_MAX_SCORES]
        self.save()
        return any(s["name"] == name and s["score"] == score for s in self.scores)

    def get_top(self) -> list:
        return self.scores[:LEADERBOARD_MAX_SCORES]