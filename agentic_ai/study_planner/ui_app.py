import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Study Planner", layout="wide")

st.title("🎓 AI Study Planner")
st.write("Generate a clean academic study roadmap with structured topics.")

# ===============================
# INPUT SECTION
# ===============================

st.header("📌 Set Your Study Goal")

goal = st.text_input("Enter Subject or Goal", placeholder="Machine Learning")

days = st.number_input(
    "Total Days Available",
    min_value=1,
    max_value=365,
    value=30
)

if st.button("Generate Study Plan"):

    if not goal:
        st.error("Please enter a study goal.")
    else:
        with st.spinner("Generating structured study plan..."):

            response = requests.post(
                f"{BACKEND_URL}/goal",
                json={"goal": goal, "days": days}
            )

            if response.status_code == 200:
                st.session_state["plan"] = response.json()
                st.success("Study Plan Generated Successfully!")
            else:
                st.error("Backend error occurred.")

# ===============================
# DISPLAY PLAN
# ===============================

if "plan" in st.session_state:

    plan_data = st.session_state["plan"]

    # compatibility safeguard
    if "plan" in plan_data:
        plan_data = plan_data["plan"]

    st.header("📚 Structured Study Roadmap")

    for topic in plan_data["topics"]:

        st.markdown("---")
        st.markdown(f"## 📖 {topic['name']} ({topic['days']} days)")

        # -------------------------
        # Documentation
        # -------------------------
        st.markdown("### 📘 Documentation to Study")

        docs = topic.get("resources", {}).get("documentation", [])

        if docs:
            for link in docs:
                st.markdown(f"- 📄 [Open Resource]({link})")
        else:
            st.write("No documentation available.")

        # -------------------------
        # Subtopics
        # -------------------------
        st.markdown("### 📂 Topics to Cover")

        subtopics = topic.get("subtopics", [])

        if subtopics:
            for sub in subtopics:
                st.markdown(f"- {sub}")
        else:
            st.write("No subtopics available.")

# ===============================
# PROGRESS SECTION
# ===============================

if "plan" in st.session_state:

    plan_data = st.session_state["plan"]

    if "plan" in plan_data:
        plan_data = plan_data["plan"]

    st.header("📊 Track Your Progress")

    progress = {}

    for topic in plan_data["topics"]:
        status = st.selectbox(
            f"{topic['name']}",
            ["not_started", "in_progress", "completed"],
            key=f"progress_{topic['name']}"
        )
        progress[topic["name"]] = status

    if st.button("Update Plan Based on Progress"):

        response = requests.post(
            f"{BACKEND_URL}/progress",
            json={"progress": progress}
        )

        if response.status_code == 200:
            st.success("Plan updated successfully!")
        else:
            st.error("Failed to update plan.")
