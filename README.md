# LearnPulse – AI Powered Education Analytics Platform

## Overview

**LearnPulse** is a full-stack analytics platform that identifies students at risk of poor academic performance using machine learning. Faculty can upload student data through CSV files, and the system analyzes the data to compute risk scores and visualize insights through an interactive dashboard.

The platform helps educators detect early warning signs, understand learning behavior, and take timely intervention actions.

---

## Key Features

### Student Risk Prediction

* Predicts student performance levels using a trained machine learning model.
* Classifies students into risk categories based on academic and engagement data.

### CSV Data Import

* Upload student datasets in CSV format.
* Automatically maps raw columns to the required schema.
* Performs feature engineering and preprocessing automatically.

### Analytics Dashboard

* Visualizes risk distribution across students.
* Shows department-level performance insights.
* Displays attendance and engagement statistics.

### Faculty Dashboard

* View total students and at-risk students.
* Monitor performance trends.
* Manage intervention actions for struggling students.

### Explainable AI

* Uses **SHAP (SHapley Additive Explanations)** to explain model predictions and highlight important features influencing student risk.

---

## Project Architecture

The platform follows a data analytics pipeline:

```
CSV Dataset
      ↓
Data Cleaning & Preprocessing
      ↓
Feature Engineering
      ↓
Machine Learning Model
      ↓
Risk Prediction
      ↓
Dashboard Visualization
```

This architecture enables real-time analytics and predictive insights for student performance monitoring.

---

## Tech Stack

### Frontend

* Next.js (React)
* TypeScript
* Tailwind CSS
* Recharts (Data Visualization)
* Zustand (State Management)
* Axios (API communication)

### Backend

* FastAPI
* Python
* SQLAlchemy ORM
* JWT Authentication
* Loguru logging

### Machine Learning

* Scikit-learn
* RandomForestClassifier
* SHAP Explainable AI
* Pandas & NumPy

### Database

* MySQL / SQLite

### DevOps

* Docker & Docker Compose
* Pytest for backend testing

---

## Machine Learning Model

The platform uses a **RandomForestClassifier** trained on student academic features.

Model features include:

* Attendance Rate
* LMS Engagement Score
* Assignment Performance
* Quiz Scores
* Academic Performance Index
* Semester Performance Trend

The model predicts student risk levels and helps faculty identify students needing support.

---

## CSV Dataset Format

A refined CSV should contain the following columns:

| Column                     | Description                |
| -------------------------- | -------------------------- |
| id                         | Student ID                 |
| name                       | Student name               |
| department                 | Department code            |
| attendance_rate            | Attendance percentage      |
| engagement_score           | LMS engagement score       |
| academic_performance_index | Academic performance index |
| login_gap_days             | Days since last login      |
| failure_ratio              | Failed courses ratio       |
| financial_risk_flag        | Financial risk indicator   |
| commute_risk_score         | Commute difficulty score   |
| semester_performance_trend | Performance trend          |

Raw CSV files can also be uploaded; the system automatically maps them to the required format.

---

## Project Structure

```
LearnPulse
│
├── backend
│   ├── app
│   │   ├── routes
│   │   ├── services
│   │   ├── models
│   │   ├── schemas
│   │   └── main.py
│   │
│   ├── ml_models
│   └── requirements.txt
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── pages
│   │   ├── services
│   │   └── store
│
├── docker
├── docker-compose.yml
└── README.md
```

---

## Installation

### Prerequisites

* Node.js (v18 or higher)
* Python (3.9+)
* Docker (optional)

---

### Backend Setup

Navigate to backend directory:

```
cd backend
```

Install dependencies:

```
pip install -r requirements.txt
```

Run backend server:

```
uvicorn app.main:app --reload --port 3001
```

API documentation:

```
http://localhost:3001/docs
```

---

### Frontend Setup

Navigate to frontend directory:

```
cd frontend
```

Install dependencies:

```
npm install
```

Start development server:

```
npm run dev
```

Open the application:

```
http://localhost:3000
```

---

## Usage

1. Login as faculty.
2. Upload a student CSV dataset.
3. The system processes the data and computes risk scores.
4. View analytics and risk distribution on the dashboard.
5. Identify students requiring intervention.

---

## Future Enhancements

* Personalized learning recommendations
* Early dropout prediction alerts
* Integration with Learning Management Systems (LMS)
* Advanced predictive analytics
* Automated academic intervention suggestions

---

## Conclusion

LearnPulse demonstrates how **AI and data analytics can improve educational outcomes**. By identifying students at risk early, educators can take proactive steps to improve student success and reduce dropout rates.

---

## Author

**Anusha Palaparthi**

GitHub: https://github.com/Anusha-2005
