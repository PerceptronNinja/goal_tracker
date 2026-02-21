import streamlit as st
from backend.services.goal_service import create_goal, get_goals, complete_goal, delete_goal

USER_ID = st.session_state.user_id

st.title("📌 Dashboard")

# Sidebar Add Goal
st.sidebar.header("➕ Add Goal")

title = st.sidebar.text_input("Goal Title")
repeat_type = st.sidebar.selectbox(
    "Repeat Type",
    ["daily", "weekly", "monthly", "yearly", "custom", "once"]
)

reminder_time = st.sidebar.text_input("Reminder Time (HH:MM)")
custom_days = None

if repeat_type == "custom":
    custom_days = st.sidebar.number_input("Repeat every X days", min_value=1, value=1)

if st.sidebar.button("Add Goal"):
    if title:
        create_goal(USER_ID, title, repeat_type, reminder_time, custom_days)
        st.success("Goal Added!")
        st.rerun()

# Load goals
goals = get_goals(USER_ID)

if not goals:
    st.info("No goals yet.")
else:
    for goal in goals:
        col1, col2, col3 = st.columns([5,1,1])

        with col1:
            st.write(f"### {goal['title']}")
            st.caption(
                f"Repeat: {goal['repeat_type']} | "
                f"Streak: {goal['current_streak']} | "
                f"Best: {goal['best_streak']}"
            )

        with col2:
            if st.button("✅", key=f"complete_{goal['id']}"):
                complete_goal(goal['id'])
                st.rerun()

        with col3:
            if st.button("🗑️", key=f"delete_{goal['id']}"):
                delete_goal(goal['id'])
                st.rerun()