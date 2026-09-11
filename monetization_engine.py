import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render_monetization_engine():
    """
    Renders the B2B SaaS business model, pricing tiers, and Monthly Recurring Revenue (MRR) projections.
    """
    st.markdown("---")
    st.subheader("💳 OptiFreight B2B SaaS Monetization Engine")
    st.caption("Live subscription tiering, API token tracking, and projected platform revenue.")

    # 1. B2B SaaS Pricing Tiers
    st.markdown("##### 📦 Enterprise Subscription Tiers")
    t1, t2, t3 = st.columns(3)
    
    with t1:
        st.markdown("""
        <div style="background-color: #161B22; padding: 20px; border-radius: 10px; border-top: 4px solid #A0AAB4;">
            <h3 style="margin-top: 0;">Data Tier</h3>
            <h2 style="color: #A0AAB4;">$999<span style="font-size: 14px;">/mo</span></h2>
            <ul style="color: #A0AAB4; font-size: 14px; padding-left: 20px;">
                <li>Live Market Spot Rates</li>
                <li>30-Day LSTM Forecasts</li>
                <li>Standard Support</li>
                <li>5 API Calls / Day</li>
            </ul>
            <button style="width: 100%; padding: 8px; background-color: #21262D; color: white; border: none; border-radius: 5px;">Active Plan</button>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown("""
        <div style="background-color: #161B22; padding: 20px; border-radius: 10px; border-top: 4px solid #00D2FF; box-shadow: 0 0 15px rgba(0, 210, 255, 0.2);">
            <h3 style="margin-top: 0; color: #00D2FF;">Pro Tier (Most Popular)</h3>
            <h2 style="color: #00D2FF;">$4,999<span style="font-size: 14px;">/mo</span></h2>
            <ul style="color: #A0AAB4; font-size: 14px; padding-left: 20px;">
                <li>Everything in Data Tier</li>
                <li>AI Strategic Copilot (Unlimited)</li>
                <li>Route Risk & Chokepoint Engine</li>
                <li>Automated PDF Board Reports</li>
            </ul>
            <button style="width: 100%; padding: 8px; background-color: #00D2FF; color: black; border: none; border-radius: 5px; font-weight: bold;">Upgrade to Pro</button>
        </div>
        """, unsafe_allow_html=True)

    with t3:
        st.markdown("""
        <div style="background-color: #161B22; padding: 20px; border-radius: 10px; border-top: 4px solid #39FF14;">
            <h3 style="margin-top: 0; color: #39FF14;">Enterprise Tier</h3>
            <h2 style="color: #39FF14;">Custom<span style="font-size: 14px;"> + 1% Rev Share</span></h2>
            <ul style="color: #A0AAB4; font-size: 14px; padding-left: 20px;">
                <li>Everything in Pro Tier</li>
                <li>Agentic Auto-Drafting Engine</li>
                <li>Dedicated Llama-3 Node</li>
                <li>White-Glove Integration</li>
            </ul>
            <button style="width: 100%; padding: 8px; background-color: #21262D; color: white; border: none; border-radius: 5px;">Contact Sales</button>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # 2. Platform Revenue Projection (The Investor Flex)
    st.markdown("##### 📈 Projected MRR (Monthly Recurring Revenue) Scaling")
    
    # Mock data showing platform growth over 12 months based on client acquisition
    months = ['Month 1', 'Month 3', 'Month 6', 'Month 9', 'Month 12']
    clients = [2, 8, 25, 55, 120]
    mrr = [c * 4999 for c in clients] # Assuming average Pro Tier subscription

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, 
        y=mrr, 
        mode='lines+markers+text',
        text=[f"${m/1000:.0f}k" for m in mrr],
        textposition="top left",
        line=dict(color='#39FF14', width=3),
        marker=dict(size=10, color='#00D2FF'),
        fill='tozeroy',
        fillcolor='rgba(57, 255, 20, 0.1)'
    ))

    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, t=30, b=0),
        height=300,
        xaxis_title="Platform Timeline",
        yaxis_title="Projected Monthly Revenue ($)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    st.plotly_chart(fig, use_container_width=True)