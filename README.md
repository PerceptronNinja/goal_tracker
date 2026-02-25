# 🚀 AI-Powered Goal Tracker Platform

## 📌 Project Overview

AI Goal Tracker is a production-grade habit optimization platform built
with:

-   🐍 Python
-   📊 Streamlit (Multi-page Dashboard)
-   🐘 PostgreSQL (Relational Database)
-   🔐 Secure Authentication (bcrypt)
-   🤖 Machine Learning (Personalized Logistic Regression)
-   🧠 LLaMA Integration (Local LLM using Ollama)
-   🎯 Reinforcement Learning (Q-Learning Habit Optimizer)
-   🐳 Docker-ready Architecture

This system allows users to track goals, monitor streaks, predict streak
breaks, and receive AI-driven behavioral optimization recommendations.

------------------------------------------------------------------------

# 🏗 Architecture Overview

The system follows clean architecture principles:

UI (Streamlit) → Service Layer → Database Layer → PostgreSQL

ML & AI Layer operates independently and integrates into the service
layer.

------------------------------------------------------------------------

# 🔐 Authentication System

Passwords are securely hashed using bcrypt before storing in the
database.

Mathematical form of hashing conceptually:

hashed_password = bcrypt(password + salt)

This ensures even if the database is exposed, original passwords cannot
be recovered.

------------------------------------------------------------------------

# 📊 Machine Learning Components

## 1️⃣ Personalized User-Level Model

Each user gets a custom logistic regression model predicting streak
break probability.

The core logistic model:

P(break \| user) = 1 / (1 + e\^-(β0 + β1x1 + β2x2 + ...))

Where features include:

-   Current streak
-   Best streak
-   Total goals
-   Streak variance

Each model is stored separately inside:

ml_engine/user_models/

------------------------------------------------------------------------

## 2️⃣ Performance Forecast (Linear Regression)

Used for short-term streak trend prediction:

y = β0 + β1x + ε

Forecasts streak performance for upcoming days.

------------------------------------------------------------------------

## 3️⃣ Reinforcement Learning Optimizer

Habit optimization modeled as Markov Decision Process (MDP).

Q-learning update rule:

Q(s,a) = Q(s,a) + α \[ r + γ max Q(s',a') - Q(s,a) \]

Where: - s = user state - a = action (reduce, maintain, increase
difficulty) - r = reward - α = learning rate - γ = discount factor

The system gradually learns optimal habit-adjustment policies.

------------------------------------------------------------------------

# 🧠 LLaMA Integration

Local LLaMA (via Ollama) generates intelligent behavioral explanations.

Flow: User Metrics → ML Prediction → LLaMA Prompt → Personalized Advice

Example prompt:

User streak break probability: 67% Provide behavioral optimization
strategy.

------------------------------------------------------------------------

# 🗂 Project Structure

goal_tracker/

app/ - streamlit_app.py - pages/

backend/ - services/ - models/ - database/

ml_engine/ - personalized models - training scripts - RL optimizer

docker/ - Dockerfile - docker-compose.yml

------------------------------------------------------------------------

# 🐘 PostgreSQL Schema

Tables:

users - id - username - password_hash - created_at

goals - id - user_id - title - repeat_type - reminder_time -
current_streak - best_streak - last_completed_date

completions - id - goal_id - completion_date

------------------------------------------------------------------------

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

git clone `<your_repo_url>`{=html} cd goal_tracker

## 2️⃣ Setup Virtual Environment

python -m venv .venv source .venv/bin/activate

## 3️⃣ Install Dependencies

pip install -r requirements.txt

## 4️⃣ Setup PostgreSQL

createdb goal_tracker_db psql goal_tracker_db \<
backend/database/schema.sql

## 5️⃣ Run Application

streamlit run app/streamlit_app.py

------------------------------------------------------------------------

# 🐳 Docker Deployment (Optional)

Build and run:

docker-compose up --build

------------------------------------------------------------------------

# 🚀 Key Features

-   Multi-user authentication
-   Goal CRUD system
-   Streak tracking engine
-   Analytics dashboard
-   Calendar visualization
-   Streak break prediction
-   Personalized ML per user
-   LLaMA-driven insights
-   Reinforcement learning optimization

------------------------------------------------------------------------

# 🎯 Resume-Ready Project Description

Designed and developed an AI-powered habit optimization platform using
PostgreSQL, Streamlit, personalized machine learning models,
reinforcement learning strategies, and local LLaMA integration.
Implemented secure authentication and clean architecture principles,
making the system scalable and production-ready.

------------------------------------------------------------------------

# 🔮 Future Improvements

-   Async ML retraining
-   Celery background scheduler
-   Email & push notifications
-   Cloud deployment (AWS/Render)
-   SHAP model interpretability
-   Google OAuth login
-   Mobile app integration

------------------------------------------------------------------------

# 👨‍💻 Author

Utkarsh Pal\
AI & ML Enthusiast\
MCA \| Big Data Analytics

------------------------------------------------------------------------

# 📄 License

This project is for educational and portfolio demonstration purposes.
