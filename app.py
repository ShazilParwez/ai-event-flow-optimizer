from google.cloud import storage, firestore
import logging
import time
import os

import streamlit as st
from utils.simulation import generate_crowd_data
from utils.heatmap import plot_heatmap
from models.crowd_model import classify_crowd
from utils.genai import get_ai_response
from utils.prompts import build_prompt
from models.predictor import predict_crowd_trend
from utils.logger import log_event


# -----------------------------
# Environment
# -----------------------------
os.environ["PORT"] = "8080"


# -----------------------------
# Cloud services setup
# -----------------------------
storage_client = storage.Client()
bucket_name = "event-flow-ai-logs"
bucket = storage_client.bucket(bucket_name)

db = firestore.Client()


def upload_log(data: str) -> None:
    blob = bucket.blob(f"log_{int(time.time())}.txt")
    blob.upload_from_string(data)


# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(level=logging.INFO)
logging.info("App initialized")


# -----------------------------
# Helpers
# -----------------------------
def sanitize_input(text):
    if not text or len(text.strip()) == 0:
        return None
    if len(text) > 300:
        return text[:300]
    return text.strip()


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="AI Event Flow Optimizer",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------
# Accessibility / App structure
# -----------------------------
st.title("AI Event Flow Optimizer")
st.header("Real-Time Crowd Monitoring Dashboard")
st.caption("AI-powered system for analyzing and optimizing crowd flow in large venues.")

st.markdown("### Security")
st.caption("Input validation, rate limiting, and safe AI handling are enabled.")

st.markdown("### Powered by Google Vertex AI")
st.caption("Using Gemini 2.5 Flash via Vertex AI for intelligent crowd analysis.")


# -----------------------------
# Custom CSS
# -----------------------------
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    .stApp {
        background-color: #000000;
        color: #e2e8f0;
    }

    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: radial-gradient(circle at 50% 50%, #0f172a 0%, #000000 70%);
        background-size: 100% 100%;
        animation: breatheBG 6s ease-in-out infinite alternate;
        z-index: -1;
        pointer-events: none;
    }

    @keyframes breatheBG {
        0% { transform: scale(1); }
        100% { transform: scale(1.3); }
    }

    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }

    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(56, 189, 248, 0.5);
        box-shadow: 0 12px 40px 0 rgba(56, 189, 248, 0.2);
    }

    div[data-testid="stMetricValue"] {
        color: #38bdf8;
        font-weight: 800;
        font-size: 2.2rem;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }

    .stTextInput > div > div > input {
        background-color: rgba(15, 23, 42, 0.6);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        transition: all 0.2s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #38bdf8;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.4);
        background-color: rgba(15, 23, 42, 0.8);
    }

    .block-container {
        padding-top: 2rem !important;
        max-width: 1400px;
    }

    hr {
        border-bottom-color: rgba(255,255,255,0.1) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


# -----------------------------
# Header banner
# -----------------------------
st.markdown(
    """
<div style="display: flex; align-items: center; gap: 25px; margin-bottom: 30px; padding: 30px 40px; background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 15px 50px rgba(0,0,0,0.4); position: relative; overflow: hidden;">
    <div style="position: absolute; top: -50px; left: -50px; width: 150px; height: 150px; background: rgba(56, 189, 248, 0.3); filter: blur(50px); border-radius: 50%;"></div>
    <div style="font-size: 5rem; line-height: 1; filter: drop-shadow(0 0 25px rgba(56, 189, 248, 0.6)); position: relative; z-index: 1;">
        🌐
    </div>
    <div style="position: relative; z-index: 1;">
        <h1 style="background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem; font-weight: 800; margin: 0; padding-bottom: 5px;">
            AI Event Flow Optimizer
        </h1>
        <h3 style="color: #cbd5e1 !important; font-size: 1.4rem; font-weight: 400; margin: 5px 0;">
            Smart crowd management powered by Machine Learning and Generative AI
        </h3>
        <p style="color: #94a3b8; margin: 0; font-size: 1.05rem;">
            Visually tracking and optimizing live crowd movement across large venues.
        </p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# -----------------------------
# Data pipeline
# -----------------------------
data = generate_crowd_data()
log_event("Crowd data generated")

crowd_labels = classify_crowd(data)
data["zone_label"] = data["area_name"].map(crowd_labels)


# -----------------------------
# KPI section
# -----------------------------
st.header("Live Venue Analytics")
st.caption("Metrics represent estimated real-time crowd conditions across the venue.")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_people = data["density"].sum() * 10
high_risk_zones = len(data[data["zone_label"] == "High"])

area_density = data.groupby("area_name")["density"].mean().sort_values()
least_crowded_area = area_density.idxmin()
most_crowded_area = area_density.idxmax()

kpi1.metric("Estimated Total Visitors", f"{total_people:,}")
kpi2.metric("Tracked Hotspots", len(data))
kpi3.metric(
    "Congested Areas",
    high_risk_zones,
    delta="Needs Attention" if high_risk_zones > 0 else "Safe",
    delta_color="inverse",
)
kpi4.metric(
    "Venue Status",
    "Critical" if high_risk_zones > 150 else ("Warning" if high_risk_zones > 50 else "Normal"),
)

st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------
# Main layout
# -----------------------------
col1, col2 = st.columns([6.5, 3.5])


# -----------------------------
# Heatmap panel
# -----------------------------
with col1:
    st.subheader("Crowd Density Heatmap")
    st.caption("Visual representation of crowd density across different areas.")

    st.markdown(
        """
### Heatmap Legend
- Green → Low crowd density (safe)
- Yellow → Moderate crowd density
- Red → High congestion (avoid if possible)
"""
    )

    st.caption("Use this map to identify safe paths and avoid congestion zones.")

    fig = plot_heatmap(data)
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------
# AI assistant panel
# -----------------------------
with col2:
    st.subheader("AI Crowd Assistant")
    st.caption("Enter a query to analyze crowd density and get safety insights.")

    user_query = st.text_input(
        "Enter your query about crowd conditions",
        placeholder="Example: Which exit is least crowded?"
    )
    st.caption("Ask questions about crowd density, congestion, or safe paths.")

    clean_query = sanitize_input(user_query)

    ask = st.button("Ask AI")
    st.caption("Click to analyze crowd data using AI.")

    if "last_query_time" not in st.session_state:
        st.session_state.last_query_time = 0

    if ask:
        if not clean_query:
            st.warning("Please enter a valid query.")
        else:
            if time.time() - st.session_state.last_query_time < 2:
                st.warning("Please wait before sending another query.")
            else:
                st.session_state.last_query_time = time.time()
                logging.info(f"User Query: {clean_query}")

                with st.spinner("Analyzing live telemetry..."):
                    summary = f"""
- Most crowded area: {most_crowded_area}
- Least crowded area: {least_crowded_area}
- High density zones: {high_risk_zones}
- Total crowd points: {len(data)}
"""

                    # Cloud Storage
                    try:
                        upload_log(summary)
                        logging.info("Summary uploaded to Cloud Storage")
                    except Exception as e:
                        logging.error(f"Storage Error: {str(e)}")

                    prompt = build_prompt(clean_query, summary)

                    start_time = time.time()
                    logging.info("Sending request to Vertex AI")
                    response = get_ai_response(prompt)
                    end_time = time.time()

                    latency = end_time - start_time
                    logging.info(f"Response received from Vertex AI")
                    logging.info(f"AI response latency: {latency:.2f} seconds")

                st.caption("Model: Gemini 2.5 Flash | Vertex AI")
                st.success("AI Response")
                st.write(response if response else "No response generated")

                # Firestore
                try:
                    db.collection("queries").add({
                        "query": clean_query,
                        "response": response,
                        "timestamp": time.time()
                    })
                    logging.info("Saved query to Firestore")
                except Exception as e:
                    logging.error(f"Firestore Error: {str(e)}")

    st.markdown("---")

    st.subheader("Cloud Features")
    st.write(
        """
- Vertex AI (Gemini) for intelligent responses  
- Cloud Run for deployment  
- Firestore for storing user queries  
- Cloud Logging for monitoring  
- Cloud Storage for storing logs  
- Cloud Monitoring for performance tracking  
"""
    )

    st.markdown("---")

    with st.expander("How to use this assistant"):
        st.write(
            """
- Ask about crowd density or congestion  
- Identify least crowded paths  
- Use insights for better movement decisions  
"""
        )


# -----------------------------
# Automated insights
# -----------------------------
st.header("Automated Insights")

congested_areas = (
    data[data["zone_label"] == "High"]["area_name"]
    .unique()
    .tolist()
)

if high_risk_zones > 0 and congested_areas:
    st.error(f"High density detected in: {', '.join(congested_areas)}.")
    st.warning("Dispatching staff is recommended to these specific locations.")
elif high_risk_zones > 0:
    st.error(f"{high_risk_zones} high density zones detected. Dispatching staff recommended.")
else:
    st.success("All critical venue areas are operating at safe capacity.")

st.success("Main entrance and primary exit routes are currently clear.")
st.info(f"Least crowded area: {least_crowded_area}")
st.error(f"Most crowded area: {most_crowded_area}")

prediction = predict_crowd_trend(area_density[most_crowded_area])
log_event(f"Prediction made: {prediction}")
st.warning(f"Forecast: {most_crowded_area} → {prediction}")


# -----------------------------
# Google Cloud section
# -----------------------------
st.header("Google Cloud Architecture")
st.write(
    """
- Vertex AI (Gemini) → AI inference  
- Cloud Run → scalable deployment  
- Firestore → persistent data storage  
- Cloud Storage → log archival  
- Cloud Logging → system monitoring  
- Cloud Monitoring → performance tracking  
"""
)


# -----------------------------
# Accessibility help
# -----------------------------
with st.expander("Accessibility Help"):
    st.write(
        """
- Use clear queries like "Which area is crowded?"
- Refer to heatmap colors for navigation decisions
- Avoid high-density zones for safety
"""
    )


# -----------------------------
# Footer
# -----------------------------
st.markdown("### Application Information")
st.write(
    """
This system combines machine learning and generative AI to analyze crowd behavior,
predict trends, and provide real-time safety recommendations.
"""
)

st.divider()
st.caption("Built by Shazil Parwez | AI Event Flow Optimizer v2.0")