import os
os.environ["PORT"] = "8080"
import streamlit as st  
from utils.simulation import generate_crowd_data  
from utils.heatmap import plot_heatmap  
from models.crowd_model import classify_crowd  
from utils.genai import get_ai_response  
from utils.prompts import build_prompt  
from models.predictor import predict_crowd_trend  

st.set_page_config(
    page_title="AI Event Flow Optimizer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Dark UI
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Complete Black Breathing Background offset to a separate hardware layer */
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
    
    /* Elegant headers */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
    /* Glassmorphism Metrics styling */
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
    
    /* Inputs */
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
    
    /* Block container padding */
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

# Header Section: Glassmorphism banner
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
            Smart crowd management powered by Machine Learning & GenAI
        </h3>
        <p style="color: #94a3b8; margin: 0; font-size: 1.05rem;">
            Visually tracking and optimizing live crowd movement across large venues.
        </p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Generate data
data = generate_crowd_data()

# Apply ML
data = classify_crowd(data)

# KPI Section
st.markdown("#### 📊 Live Venue Analytics")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_people = data["density"].sum() * 10
high_risk_zones = len(data[data["zone_label"] == "High Density / Congested"])

area_density = data.groupby("area_name")["density"].mean().sort_values()
least_crowded_area = area_density.idxmin()
most_crowded_area = area_density.idxmax()

kpi1.metric("Est. Total Visitors", f"{total_people:,}")
kpi2.metric("Tracked Hotspots", len(data))
kpi3.metric(
    "Congested Areas",
    high_risk_zones,
    delta="Needs Attention" if high_risk_zones > 0 else "Safe",
    delta_color="inverse",
)
kpi4.metric(
    "Venue Status",
    (
        "Critical"
        if high_risk_zones > 150
        else ("Warning" if high_risk_zones > 50 else "Normal")
    ),
)

st.markdown("<br>", unsafe_allow_html=True)

# Main Layout
col1, col2 = st.columns([6.5, 3.5])

with col1:
    # st.subheader("Live Tracking Heatmap")
    fig = plot_heatmap(data)
    # The heatmap title takes care of the header
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### 🤖 GenAI Operations Assistant")
    st.markdown(
        "<span style='color:#8b949e; font-size: 0.9em;'>Ask natural language queries regarding the current venue situation:</span>",
        unsafe_allow_html=True,
    )
    user_query = st.text_input(
        "Ask Query",
        placeholder="e.g. 'Which exit is least crowded?'",
        label_visibility="collapsed",
    )
    ask = st.button("Ask AI")

    if ask and user_query:
        with st.spinner("Analyzing live telemetry..."):
            high_density = len(data[data["zone_label"] == "High Density / Congested"])

            summary = f"""
- Most crowded area: {most_crowded_area}
- Least crowded area: {least_crowded_area}
- High density zones: {high_density}
- Total crowd points: {len(data)}
"""

            prompt = build_prompt(user_query, summary)
            response = get_ai_response(prompt)

            st.success("AI Response:")
            st.write(response)

    if not user_query:
        st.info("💡 Try asking: 'Which exit is least crowded?'")

    st.markdown("---")
    st.markdown(
        "<span style='color:#8b949e; font-size: 0.9em; font-weight: 600;'>AUTOMATED INSIGHTS</span>",
        unsafe_allow_html=True,
    )

    # Get names of crowded areas
    congested_areas = (
        data[data["zone_label"] == "High Density / Congested"]["area_name"]
        .unique()
        .tolist()
    )

    if high_risk_zones > 0 and congested_areas:
        st.error(f"⚠️ **High density detected in:** {', '.join(congested_areas)}.")
        st.warning("Dispatching staff recommended to these specific locations.")
    elif high_risk_zones > 0:
        st.error(
            f"⚠️ **{high_risk_zones} high density zones detected.** Dispatching staff recommended."
        )
    else:
        st.success("✅ **All critical venue areas are operating at safe capacity.**")

    st.success("✅ **Main Entrance and primary exit routes are currently clear.**")

    st.info(f"Least crowded area: {least_crowded_area}")
    st.error(f"Most crowded area: {most_crowded_area}")

    prediction = predict_crowd_trend(area_density[most_crowded_area])
    st.warning(f"🔮 Forecast: {most_crowded_area} → {prediction}")

st.divider()
st.caption("Built with 💙 by Shazil Parwez | AI Event Flow Optimizer v2.0")
