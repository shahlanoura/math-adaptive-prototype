import streamlit as st
import time
from puzzle_generator import generate, LEVELS
from tracker import Tracker
from adaptive_engine import AdaptiveEngineML


def main():
    st.set_page_config(page_title="Math Adventures — Adaptive Prototype", layout="centered")
    st.title("🧮 Math Adventures — Adaptive Prototype")

    # --- Session State Initialization ---
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "engine" not in st.session_state:
        st.session_state.engine = None
    if "tracker" not in st.session_state:
        st.session_state.tracker = None
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
    if "question" not in st.session_state:
        st.session_state.question = None
    if "answer" not in st.session_state:
        st.session_state.answer = None
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "feedback" not in st.session_state:
        st.session_state.feedback = ""
    if "finished" not in st.session_state:
        st.session_state.finished = False

    # --- Step 1: User Info ---
    if not st.session_state.name:
        st.session_state.name = st.text_input("👤 Enter learner's name:", "").strip()
        if not st.session_state.name:
            st.stop()

    # --- Step 2: Choose Starting Difficulty ---
    if st.session_state.engine is None:
        start_level = st.radio("🎯 Choose starting difficulty:", ["Easy", "Medium", "Hard"])
        if st.button("Start Session"):
            st.session_state.engine = AdaptiveEngineML(start_level=start_level)
            st.session_state.tracker = Tracker()
            st.session_state.question_index = 0
            st.session_state.finished = False
            st.session_state.feedback = ""
            st.rerun()
        st.stop()

    engine = st.session_state.engine
    tracker = st.session_state.tracker

    num_questions = 12

    # --- Step 3: Display Questions ---
    if st.session_state.question_index < num_questions and not st.session_state.finished:
        if st.session_state.question is None:
            level = engine.current_level
            q, ans = generate(level)
            st.session_state.question = q
            st.session_state.answer = ans
            st.session_state.start_time = time.time()

        level = engine.current_level
        st.subheader(f"Problem {st.session_state.question_index + 1} [{level}]")
        st.markdown(f"**{st.session_state.question}**")

        user_answer = st.text_input("✏️ Your answer:", key=f"ans_{st.session_state.question_index}")
        if st.button("Submit", key=f"submit_{st.session_state.question_index}"):
            try:
                uans = int(user_answer.strip())
            except ValueError:
                uans = None

            t1 = time.time()
            time_taken = t1 - st.session_state.start_time
            correct = (uans == st.session_state.answer)
            if correct:
                st.session_state.feedback = "✅ Correct!"
            else:
                st.session_state.feedback = f"❌ Incorrect. Correct answer: {st.session_state.answer}"

            tracker.log(
                st.session_state.question,
                st.session_state.answer,
                uans if uans is not None else -999,
                time_taken,
                level,
            )

            next_level = engine.decide(tracker)
            if next_level != level:
                st.session_state.feedback += f"\n🔁 Difficulty changed: {level} → {next_level}"

            # Reset for next question
            st.session_state.question_index += 1
            st.session_state.question = None
            st.session_state.answer = None
            st.session_state.start_time = None

            if st.session_state.question_index >= num_questions:
                st.session_state.finished = True

            st.rerun()

        if st.session_state.feedback:
            st.info(st.session_state.feedback)

    # --- Step 4: Summary ---
    if st.session_state.finished:
        s = tracker.summary()
        st.success("🎉 Session Complete!")
        st.write(f"**Learner:** {st.session_state.name}")
        st.write(f"**Total Problems:** {s['total']}")
        st.write(f"**Correct Answers:** {s['correct']}")
        st.write(f"**Accuracy:** {s['accuracy']*100:.1f}%")
        st.write(f"**Avg Time per Question:** {s['avg_time']:.2f}s")
        st.write(f"**Recommended Next Level:** {engine.current_level}")
        recommended_level = engine.current_level
        

        st.markdown("---")
        st.subheader("Would you like to continue to the next level?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Yes, continue"):
                st.session_state.engine = AdaptiveEngineML(start_level=recommended_level)
                st.session_state.tracker = Tracker()
                st.session_state.question_index = 0
                st.session_state.finished = False
                st.session_state.feedback = ""
                st.rerun()

        with col2:
            if st.button("🔁 No, Restart"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()



if __name__ == "__main__":
    main()
