import json
import os

class HighScoreManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.high_scores = self.load_high_scores()

    def load_high_scores(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return {"scores": []}  # Initialize with an empty list of scores

    def save_high_scores(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.high_scores, file)

    def update_high_scores(self, score):
        # Add the new score to the list
        self.high_scores["scores"].append(score)
        # Sort the scores in descending order and keep only the top 5
        self.high_scores["scores"] = sorted(self.high_scores["scores"], reverse=True)[:5]
        # Save the updated scores
        self.save_high_scores()

    def get_high_scores(self):
        return self.high_scores["scores"]