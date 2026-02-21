import streamlit as st
from backend.services.goal_service import get_goals

USER_ID = st.session_state.user_id

st.title("🧠 AI Insights")

goals = get_goals(USER_ID)

if not goals:
    st.info("No goals available.")
    st.stop()

total = len(goals)
avg_streak = sum(g["current_streak"] for g in goals) / total
best_streak = max(g["best_streak"] for g in goals)

performance_score = (avg_streak * 0.6) + (best_streak * 0.4)

st.metric("Performance Score", round(performance_score, 2))

if performance_score < 5:
    st.warning("You need stronger consistency.")
elif performance_score < 10:
    st.info("Good progress. Improve discipline.")
else:
    st.success("Excellent performance! Increase difficulty.")