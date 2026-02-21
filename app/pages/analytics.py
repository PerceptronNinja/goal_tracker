import streamlit as st
from backend.services.goal_service import get_goals
import pandas as pd

USER_ID = st.session_state.user_id

st.title("📊 Analytics")

goals = get_goals(USER_ID)

if not goals:
    st.info("No data available.")
    st.stop()

total = len(goals)
avg_streak = sum(g["current_streak"] for g in goals) / total
best_streak = max(g["best_streak"] for g in goals)

st.metric("Total Goals", total)
st.metric("Average Streak", round(avg_streak, 2))
st.metric("Best Streak", best_streak)

df = pd.DataFrame({
    "Goal": [g["title"] for g in goals],
    "Current Streak": [g["current_streak"] for g in goals],
    "Best Streak": [g["best_streak"] for g in goals],
})

st.bar_chart(df.set_index("Goal"))