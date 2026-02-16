import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Study Planner", layout="wide")

st.title("🎓 AI Study Planner")
st.write("Generate structured study topics with YouTube & documentation links.")

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

    plan = st.session_state["plan"]["plan"]

    st.header("📚 Your Study Plan")

    for topic in plan["topics"]:

        with st.expander(f"📖 {topic['name']} ({topic['days']} days)", expanded=False):

            # -------------------------
            # MAIN TOPIC RESOURCES
            # -------------------------

            st.subheader("📺 YouTube Resources")

            for link in topic["resources"]["youtube"]:
                st.markdown(f"- [Watch Here]({link})")

            st.subheader("📘 Documentation")

            for link in topic["resources"]["documentation"]:
                st.markdown(f"- [Read Here]({link})")

            st.markdown("---")

            # -------------------------
            # SUBTOPICS
            # -------------------------

            st.subheader("📂 Subtopics")

            for sub in topic["subtopics"]:

                st.markdown(f"### 🔹 {sub['name']}")

                st.markdown("**YouTube:**")
                for link in sub["resources"]["youtube"]:
                    st.markdown(f"- [Watch Here]({link})")

                st.markdown("**Documentation:**")
                for link in sub["resources"]["documentation"]:
                    st.markdown(f"- [Read Here]({link})")

                st.markdown("---")

# ===============================
# PROGRESS SECTION
# ===============================

if "plan" in st.session_state:

    st.header("📊 Track Your Progress")

    progress = {}

    for topic in st.session_state["plan"]["plan"]["topics"]:
        status = st.selectbox(
            f"{topic['name']}",
            ["completed", "partial", "not_done"],
            key=topic["name"]
        )
        progress[topic["name"]] = status

    if st.button("Update Plan Based on Progress"):

        response = requests.post(
            f"{BACKEND_URL}/progress",
            json={"progress": progress}
        )

        if response.status_code == 200:
            st.session_state["plan"]["plan"] = response.json()["updated_plan"]
            st.success("Plan updated successfully!")
        else:
            st.error("Failed to update plan.")
