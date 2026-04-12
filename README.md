# AI Event Flow Optimizer

An AI-powered system for real-time crowd management and event optimization.

---

## Problem

Large-scale events often face:
- Crowd congestion
- Long waiting times
- Poor coordination

This leads to safety risks and bad user experience.

---

## Solution

AI Event Flow Optimizer provides:

- Live crowd density visualization (heatmap)
- GenAI-powered assistant (Gemini via Vertex AI)
- Future crowd movement prediction
- Smart recommendations for crowd flow

---

## Demo Features

- Real-time crowd simulation
- Interactive density heatmap
- AI assistant answering queries like:
  - "Which entry is least crowded?"
- Automated insights & alerts

---

## Tech Stack

- Python
- Streamlit
- Plotly
- Scikit-learn
- Google Vertex AI (Gemini)
- Google Cloud Run (Deployment)

---

## Deployment

Deployed on **Google Cloud Run** for scalability and real-time access.

---

## Impact

- Improves crowd safety
- Reduces waiting time
- Enables proactive decision-making
- Enhances event experience

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py