import time
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Attempt:
    question: str
    correct_answer: int
    user_answer: int
    correct: bool
    time_taken: float
    difficulty: str


@dataclass
class Tracker:
    attempts: List[Attempt] = field(default_factory=list)

    def log(self, question: str, correct_answer: int, user_answer: int, time_taken: float, difficulty: str):
        self.attempts.append(Attempt(question, correct_answer, user_answer, user_answer == correct_answer, time_taken, difficulty))

    def accuracy(self, last_k: int = None) -> float:
        items = self.attempts if last_k is None else self.attempts[-last_k:]
        if not items:
            return 0.0
        correct = sum(1 for a in items if a.correct)
        return correct / len(items)

    def avg_time(self, last_k: int = None) -> float:
        items = self.attempts if last_k is None else self.attempts[-last_k:]
        if not items:
            return 0.0
        return sum(a.time_taken for a in items) / len(items)

    def summary(self) -> Dict:
        total = len(self.attempts)
        correct = sum(1 for a in self.attempts if a.correct)
        return {
            "total": total,
            "correct": correct,
            "accuracy": (correct / total) if total else 0.0,
            "avg_time": self.avg_time()
        }