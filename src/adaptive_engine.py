# adaptive_engine_ml.py
import numpy as np
from sklearn.linear_model import LogisticRegression

LEVELS = ["Easy", "Medium", "Hard"]

class AdaptiveEngineML:
    def __init__(self, start_level="Easy"):
        self.model = LogisticRegression()
        self.level_idx = LEVELS.index(start_level)
        self.X, self.y = [], []
        self.trained = False

    @property
    def current_level(self):
        return LEVELS[self.level_idx]

    def update_model(self, features, outcome):
        """
        Add a new training sample and (re)train the logistic regression model.
        features: list or array [difficulty_index, accuracy, avg_time]
        outcome: 1 if correct answer, 0 otherwise
        """
        self.X.append(features)
        self.y.append(outcome)

        # Train model when enough samples exist
        if len(self.y) >= 5:
            self.model.fit(self.X, self.y)
            self.trained = True

    def decide(self, tracker):
        """
        Decide next difficulty purely using ML model.
        Requires that the model has been trained.
        """
        if not self.trained:
            # Wait until we have enough data to train
            return LEVELS[self.level_idx]

        # Build feature vector from current performance
        features = np.array([[self.level_idx, tracker.accuracy(), tracker.avg_time()]])
        prob = self.model.predict_proba(features)[0, 1]  # Probability of correct answer

        # Adjust difficulty based on predicted success probability
        if prob > 0.8 and self.level_idx < 2:
            self.level_idx += 1
        elif prob < 0.4 and self.level_idx > 0:
            self.level_idx -= 1

        return LEVELS[self.level_idx]
