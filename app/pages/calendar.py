import streamlit as st
from backend.database.db import get_connection
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

USER_ID = st.session_state.user_id

st.title("🗓 Activity Calendar")

conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT completion_date
    FROM completions c
    JOIN goals g ON c.goal_id = g.id
    WHERE g.user_id = %s
""", (USER_ID,))

rows = cur.fetchall()
cur.close()
conn.close()

if not rows:
    st.info("No completion history.")
    st.stop()

dates = [row[0] for row in rows]

today = datetime.now().date()
start_date = today - timedelta(days=60)

date_range = pd.date_range(start=start_date, end=today)
df = pd.DataFrame(date_range, columns=["date"])
df["date"] = df["date"].dt.date
df["completed"] = df["date"].isin(dates).astype(int)

df["week"] = df["date"].apply(lambda x: x.isocalendar()[1])
df["weekday"] = df["date"].apply(lambda x: x.weekday())

fig = px.density_heatmap(
    df,
    x="week",
    y="weekday",
    z="completed",
    color_continuous_scale="greens"
)

st.plotly_chart(fig, use_container_width=True)