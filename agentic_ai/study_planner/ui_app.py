import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Study Planner", layout="wide")

st.title("🎓 AI Study Planner")

# ==================================================
# INPUT SECTION
# ==================================================

goal = st.text_input("Enter Subject")
days = st.number_input("Total Days", min_value=1, value=30)

difficulty = st.selectbox(
    "Difficulty Level",
    ["beginner", "intermediate", "advanced"]
)

if st.button("Generate Study Plan"):

    response = requests.post(
        f"{BACKEND_URL}/goal",
        json={
            "goal": goal,
            "days": days,
            "difficulty": difficulty
        }
    )

    if response.status_code == 200:
        st.session_state["plan"] = response.json()
        st.session_state["progress_data"] = {}
    else:
        st.error("Failed to generate plan.")

# ==================================================
# DISPLAY PLAN
# ==================================================

if "plan" in st.session_state:

    plan_data = st.session_state["plan"]

    if "plan" in plan_data:
        plan_data = plan_data["plan"]

    topics = plan_data["topics"]

    if "progress_data" not in st.session_state:
        st.session_state["progress_data"] = {}

    total_subtopics = 0
    completed_subtopics = 0

    for topic in topics:

        topic_name = topic["name"]

        if topic_name not in st.session_state["progress_data"]:
            st.session_state["progress_data"][topic_name] = {
                "subtopics": {},
                "quiz_score": None
            }

        with st.expander(f"{topic_name} ({topic['days']} days)"):

            # ----------------------------------------
            # SUBTOPICS + RESOURCES ONLY
            # ----------------------------------------

            st.markdown("### 📂 Subtopics")

            for sub in topic["subtopics"]:

                sub_name = sub["name"]
                total_subtopics += 1

                st.markdown(f"#### 🔹 {sub_name}")

                st.markdown(
                    f"[📘 Documentation]({sub['resource']['documentation']})"
                )

                st.markdown(
                    f"[🎥 Video Lecture]({sub['resource']['youtube']})"
                )

                status = st.selectbox(
                    f"Progress for {sub_name}",
                    ["not_done", "partial", "completed"],
                    key=f"{topic_name}_{sub_name}"
                )

                st.session_state["progress_data"][topic_name]["subtopics"][sub_name] = status

                if status == "completed":
                    completed_subtopics += 1

                st.markdown("---")

            # ----------------------------------------
            # QUIZ SECTION
            # ----------------------------------------

            quiz_key = f"quiz_{topic_name}"

            if st.button(f"Generate Quiz for {topic_name}", key=f"btn_{quiz_key}"):

                quiz_response = requests.post(
                    f"{BACKEND_URL}/quiz",
                    json={
                        "topic": topic_name,
                        "difficulty": difficulty
                    }
                )

                if quiz_response.status_code == 200:
                    st.session_state[quiz_key] = quiz_response.json()

            if quiz_key in st.session_state:

                quiz = st.session_state[quiz_key]

                st.markdown("## 📝 Quiz")

                user_answers = {}

                for i, q in enumerate(quiz):

                    st.markdown(f"### Q{i+1}. {q['question']}")

                    user_answers[i] = st.radio(
                        "Select your answer:",
                        q["options"],
                        key=f"{quiz_key}_q_{i}"
                    )

                if st.button(f"Submit Quiz for {topic_name}", key=f"submit_{quiz_key}"):

                    score = 0
                    for i, q in enumerate(quiz):
                        if user_answers[i] == q["answer"]:
                            score += 1

                    st.session_state["progress_data"][topic_name]["quiz_score"] = score

                    st.markdown(f"## 🎯 Score: {score} / {len(quiz)}")

                    if score == len(quiz):
                        st.success("🏆 Mastery Achieved!")
                    elif score >= len(quiz) // 2:
                        st.info("Good understanding. Minor revision needed.")
                    else:
                        st.warning("Weak area detected. Recommend revision.")

            # ----------------------------------------
            # MASTERY LOGIC
            # ----------------------------------------

            topic_progress = st.session_state["progress_data"][topic_name]

            if (
                topic_progress["quiz_score"] is not None
                and topic_progress["quiz_score"] >= 3
                and all(
                    s == "completed"
                    for s in topic_progress["subtopics"].values()
                )
            ):
                st.success("✅ Topic Mastered")

            elif topic_progress["quiz_score"] is not None:
                st.warning("⚠ Topic In Progress")

    # ==================================================
    # GLOBAL PROGRESS BAR
    # ==================================================

    if total_subtopics > 0:
        overall_progress = completed_subtopics / total_subtopics
        st.markdown("## 📊 Overall Progress")
        st.progress(overall_progress)
