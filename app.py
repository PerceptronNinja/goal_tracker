import streamlit as st
from database import add_goal, load_goals, mark_completed, delete_goal
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Goal Tracker", layout="wide")

st.title("🚀 AI Goal Tracker Dashboard")

# ==============================
# SIDEBAR - ADD GOAL
# ==============================
st.sidebar.header("➕ Add New Goal")

title = st.sidebar.text_input("Goal Title")

repeat_type = st.sidebar.selectbox(
    "Repeat Type",
    ["daily", "weekly", "monthly", "yearly", "custom", "once"]
)

reminder_time = st.sidebar.text_input("Reminder Time (HH:MM)")

custom_days = None
if repeat_type == "custom":
    custom_days = st.sidebar.number_input(
        "Repeat every X days",
        min_value=1,
        value=1
    )

if st.sidebar.button("Add Goal"):
    if title:
        add_goal(title, repeat_type, reminder_time, custom_days)
        st.sidebar.success("Goal Added!")
        st.rerun()
    else:
        st.sidebar.warning("Enter a goal title.")


# ==============================
# LOAD GOALS
# ==============================
goals = load_goals()

if not goals:
    st.info("No goals yet.")
    st.stop()

# ==============================
# DISPLAY GOALS
# ==============================
st.subheader("📌 Your Goals")

for i, goal in enumerate(goals):
    col1, col2, col3, col4 = st.columns([4,1,1,1])

    with col1:
        st.write(f"### {goal['title']}")
        st.caption(
            f"Repeat: {goal.get('repeat_type')} | "
            f"Streak: {goal.get('current_streak',0)} | "
            f"Best: {goal.get('best_streak',0)}"
        )

    with col2:
        if st.button("✅", key=f"complete{i}"):
            mark_completed(i)
            st.rerun()

    with col3:
        if st.button("🗑️", key=f"delete{i}"):
            delete_goal(i)
            st.rerun()

    with col4:
        status = "✅" if goal["completed"] else "❌"
        st.write(status)

st.divider()

# ==============================
# ANALYTICS SECTION
# ==============================
st.subheader("📊 Analytics")

total = len(goals)
completed = sum(1 for g in goals if g["completed"])
completion_rate = (completed / total) * 100

avg_streak = sum(g.get("current_streak", 0) for g in goals) / total
best_streak = max(g.get("best_streak", 0) for g in goals)

col1, col2, col3 = st.columns(3)

col1.metric("Total Goals", total)
col2.metric("Completion Rate", f"{completion_rate:.2f}%")
col3.metric("Best Streak", best_streak)

st.divider()

# ==============================
# AI PERFORMANCE INSIGHT
# ==============================
st.subheader("🧠 AI Performance Insight")

performance_score = (avg_streak * 0.6) + (completion_rate * 0.4)

if performance_score < 30:
    st.warning("⚠️ You are inconsistent. Focus on smaller habits.")
elif performance_score < 60:
    st.info("📘 Moderate consistency. Improve routine stability.")
else:
    st.success("🔥 Excellent discipline. Increase challenge level!")

st.divider()

# ==============================
# STREAK CHART
# ==============================
st.subheader("📈 Streak Comparison")

df = pd.DataFrame({
    "Goal": [g["title"] for g in goals],
    "Current Streak": [g.get("current_streak",0) for g in goals],
    "Best Streak": [g.get("best_streak",0) for g in goals],
})

st.bar_chart(df.set_index("Goal"))

st.divider()

# ==============================
# 🗓 GITHUB-STYLE CALENDAR
# ==============================
st.subheader("🗓 Last 60 Days Activity")

# collect all completion dates
all_history = []
for goal in goals:
    for date in goal.get("history", []):
        all_history.append(date)

if not all_history:
    st.info("No completion history yet.")
else:
    today = datetime.now().date()
    start_date = today - timedelta(days=60)

    date_range = pd.date_range(start=start_date, end=today)

    history_df = pd.DataFrame(date_range, columns=["date"])
    history_df["date"] = history_df["date"].dt.date
    history_df["completed"] = history_df["date"].astype(str).isin(all_history).astype(int)

    history_df["week"] = history_df["date"].apply(lambda x: x.isocalendar()[1])
    history_df["weekday"] = history_df["date"].apply(lambda x: x.weekday())

    fig = px.density_heatmap(
        history_df,
        x="week",
        y="weekday",
        z="completed",
        color_continuous_scale="greens",
        title="Completion Heatmap",
    )

    fig.update_layout(
        yaxis=dict(
            tickmode="array",
            tickvals=[0,1,2,3,4,5,6],
            ticktext=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        )
    )

    st.plotly_chart(fig, use_container_width=True)