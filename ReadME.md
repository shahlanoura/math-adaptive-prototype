# 🧮 Math Adventures — Adaptive Learning Prototype

## 🚀 Overview
**Math Adventures** is an **AI-powered adaptive learning system** built with **Python** and **Streamlit**.
It dynamically adjusts the difficulty of math problems based on a learner’s performance using a **machine learning (ML)-based adaptive engine**.

The goal is to personalize the learning journey for each student and keep them challenged—but not overwhelmed.

## 🧩 Features
- 🧠 Adaptive Difficulty — Automatically adjusts questions between Easy, Medium, and Hard.
- 📊 Performance Tracking — Logs every attempt, correctness, time taken, and difficulty.
- 🤖 ML-Based Adaptation — Uses Logistic Regression model for smart difficulty prediction.
- ⚡ Interactive UI — Streamlit front-end with instant feedback.
- 🔁 Continuous Learning — Model retrains as data grows.

## 🏗️ Architecture
```
Learner UI (Streamlit)
      │
Puzzle Generator ──▶ Tracker ──▶ Adaptive Engine (ML)
      │                             │
      └────────────▶ Feedback Loop ◀─┘
```

## ⚙️ Installation
```bash
git clone https://github.com/shahlanoura/math-adaptive-prototype.git
cd math-adaptive-prototype
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run main.py
```

## 🧠 Adaptive Logic (ML-Based)
**Model:** Logistic Regression
**Features:** difficulty index, rolling accuracy, avg time/question

```python
prob = model.predict_proba(features)[0, 1]
if prob > 0.8 and level < 2:
    level += 1
elif prob < 0.4 and level > 0:
    level -= 1
```

## 📈 Key Metrics
| Metric | Description | Influence |
|---------|-------------|------------|
| Accuracy | % correct | Higher → Harder |
| Avg Time | Time/question | Longer → Easier |
| Recent Accuracy | Short-term trend | Detects improvement |

## 💡 Why ML?
| Aspect | Rule-Based | ML-Based |
|---------|-------------|----------|
| Adaptability | Fixed logic | Learner-specific |
| Scalability | Manual tuning | Self-learning |
| Personalization | Generic | Dynamic & tailored |

## 🚧 Future Improvements
- Add persistence (SQLite)
- Visualization of progress
- Extend to more subjects
- Integrate neural models (RNN)

## 🧑‍💻 Author
Developed by: Shahlanoura
Technologies: Python, Streamlit, scikit-learn
License: MIT
