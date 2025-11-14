import random
from typing import Tuple

# Difficulty levels
LEVELS = ["Easy", "Medium", "Hard"]


def generate(difficulty: str) -> Tuple[str, int]:
    """Return (question_text, correct_answer)

    Difficulty:
      - Easy: single-digit add/sub (0-9)
      - Medium: two-digit add/sub or single-digit multiplication
      - Hard: two-digit multiplication or division with integer quotient
    """
    if difficulty == "Easy":
        a = random.randint(0, 9)
        b = random.randint(0, 9)
        if random.random() < 0.6:
            q = f"{a} + {b} = ?"
            return q, a + b
        else:
            # ensure no negative results for the target age
            a, b = max(a, b), min(a, b)
            q = f"{a} - {b} = ?"
            return q, a - b

    if difficulty == "Medium":
        if random.random() < 0.5:
            a = random.randint(10, 99)
            b = random.randint(0, 99)
            q = f"{a} + {b} = ?"
            return q, a + b
        elif random.random() < 0.8:
            a = random.randint(10, 99)
            b = random.randint(0, 99)
            a, b = max(a, b), min(a, b)
            q = f"{a} - {b} = ?"
            return q, a - b
        else:
            # single-digit multiplication
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            q = f"{a} × {b} = ?"
            return q, a * b

    # Hard
    if difficulty == "Hard":
        if random.random() < 0.6:
            a = random.randint(10, 99)
            b = random.randint(2, 12)
            q = f"{a} × {b} = ?"
            return q, a * b
        else:
            # Division with integer quotient
            b = random.randint(2, 12)
            q_val = random.randint(2, 12)
            a = b * q_val
            q = f"{a} ÷ {b} = ?"
            return q, q_val

    # fallback
    return generate("Easy")


