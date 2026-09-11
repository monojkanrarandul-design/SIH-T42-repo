import streamlit as st
from scenario_engine import render_scenario_calculator
from ai_advisor import render_ai_advisor
from ml_analytics import render_ml_insights
from command_center import render_live_ticker
from global_routing import render_3d_map
from report_genrerator import render_pdf_report
from agentic_drafter import render_agentic_drafter
from route_analyzer import render_route_risk_analyzer
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- Page Configuration ---
st.set_page_config(page_title="OptiFreight Dashboard", layout="wide")
st.title("🚢 OptiFreight - Predictive Maritime Intelligence")
st.markdown("Optimization of Vessel Chartering & Bulk Cargo Procurement")

# --- Mock Data Generation (Simulating BDI & Forecasts) ---
@st.cache_data
def load_data():
    dates = pd.date_range(start="2026-01-01", periods=100)
    historical_prices = np.linspace(1500, 2000, 100) + np.random.normal(0, 50, 100)
    
    future_dates = pd.date_range(start=dates[-1] + timedelta(days=1), periods=30)
    # Simulate a price drop for the forecast
    forecast_prices = np.linspace(historical_prices[-1], 1700, 30) + np.random.normal(0, 40, 30)
    
    return dates, historical_prices, future_dates, forecast_prices

dates, hist_prices, fut_dates, fore_prices = load_data()

# --- Top Metric Cards ---
col1, col2, col3 = st.columns(3)
current_rate = hist_prices[-1]
projected_low = min(fore_prices)
col1.metric("Current Freight Rate (USD/ton)", f"${current_rate:.2f}", "+1.2%")
col2.metric("30-Day Projected Low", f"${projected_low:.2f}", "-12.5%")
col3.metric("Estimated Savings (per voyage)", "$142,500", "High Confidence")

# --- Chartering Recommendation Engine ---
st.subheader("Actionable Intelligence")
if projected_low < current_rate:
    st.success("🟢 **RECOMMENDATION: WAIT.** Freight rates are projected to drop by ~12% over the next 14 days due to easing port congestion in Singapore. Delay chartering.")
else:
    st.error("🔴 **RECOMMENDATION: CHARTER NOW.** Geopolitical risk metrics indicate imminent rate hikes. Lock in contracts immediately.")

# --- Predictive Charting (Plotly) ---
st.subheader("Freight Rate Forecast (LSTM Model Simulation)")

fig = go.Figure()
# Historical Data
fig.add_trace(go.Scatter(x=dates, y=hist_prices, mode='lines', name='Historical Rate', line=dict(color='blue')))
# Predicted Data
fig.add_trace(go.Scatter(x=fut_dates, y=fore_prices, mode='lines', name='AI Forecast (30-Day)', line=dict(color='orange', dash='dash')))

fig.update_layout(title="Baltic Dry Index (BDI) Simulation & Prediction",
                  xaxis_title="Date",
                  yaxis_title="Freight Rate (USD)")
st.plotly_chart(fig, use_container_width=True)

# --- Real-Time Risk Factors ---
st.subheader("Live Geopolitical & Weather Risk Metrics")
risk_cols = st.columns(4)
risk_cols[0].metric("Suez Canal Congestion", "High", "Delay: +2 days")
risk_cols[1].metric("Typhoon Risk (South China Sea)", "Moderate", "Rerouting Advised")
risk_cols[2].metric("Global Fuel (VLSFO) Price", "$610/mt", "-0.8%")
risk_cols[3].metric("Port of Shanghai Wait Time", "36 Hours", "Improving")
render_scenario_calculator(current_rate, projected_low)
render_ai_advisor(current_rate,projected_low)
render_ml_insights(dates,hist_prices,fut_dates,fore_prices)
st.title("🚢 OptiFreight - Predictive Maritime Intelligence")
st.markdown("Optimization of Vessel Chartering & Bulk Cargo Procurement")
render_live_ticker()
render_3d_map()
render_pdf_report(current_rate,projected_low)
render_agentic_drafter(projected_low,75000)
render_route_risk_analyzer()