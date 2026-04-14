# AI Event Flow Optimizer

Smart crowd management powered by Machine Learning and Google Vertex AI (Gemini)

---

## Live Demo
https://event-flow-ai-57448112377.us-central1.run.app/

---

## Overview

AI Event Flow Optimizer is a real-time intelligent system designed to monitor, analyze, and optimize crowd movement in large venues.

It combines data simulation, machine learning, and generative AI to deliver actionable insights for safer and more efficient event management.

---

## Problem

Large-scale events often face:
- Crowd congestion  
- Long waiting times  
- Poor crowd flow management  

These issues lead to safety risks and poor user experience.

---

## Solution

The system provides:

- Real-time crowd density visualization using heatmaps  
- GenAI assistant (Gemini via Vertex AI) for intelligent queries  
- Crowd trend prediction for proactive decision-making  
- Automated alerts and recommendations for congestion control  

---

## Features

- Interactive crowd density heatmap (Plotly)  
- AI assistant for natural language queries  
- Zone-based crowd classification (Low / Medium / High)  
- Predictive analytics for crowd movement  
- Input validation and rate limiting (security)  
- Deployed on Google Cloud Run  

---

## Google Cloud Integration

- Vertex AI (Gemini 2.5 Flash) for intelligent responses  
- Cloud Run for scalable deployment  
- Logging for monitoring and debugging  

---

## Testing

Implemented using pytest:

- Crowd classification logic  
- Prediction pipeline  
- Edge cases (empty input, small datasets)  
- Functional validation  

---

## Security

- Input sanitization  
- Rate limiting for API requests  
- Safe error handling  
- Environment-based configuration  

---

## Tech Stack

- Python, Streamlit  
- Pandas, NumPy, Scikit-learn  
- Plotly  
- Google Vertex AI (Gemini)  
- Google Cloud Run  

---

## Deployment

Deployed on Google Cloud Run for:
- Scalability  
- High availability  
- Real-time access  

---

## Impact

- Improves crowd safety  
- Reduces congestion and waiting time  
- Enables data-driven decision making  
- Enhances overall event experience  

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
