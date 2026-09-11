import streamlit as st
import plotly.graph_objects as go

# Database of key bulk maritime trade routes, waypoints, and risk profiles
TRADE_LANES = {
    "Dampier (Australia) ➔ Qingdao (China) [Iron Ore]": {
        "origin": {"name": "Dampier", "lat": -20.66, "lon": 116.71},
        "dest": {"name": "Qingdao", "lat": 36.06, "lon": 120.38},
        "waypoints": [(-8.5, 115.5), (0.5, 119.5), (14.0, 120.0), (25.0, 122.5)],
        "distance_nm": 3650,
        "base_days": 13,
        "risks": [
            {"category": "Weather Hazard", "level": "Medium", "desc": "Seasonal typhoon alley in the Philippine Sea; monitor tropical storm forecasts."},
            {"category": "Chokepoint Congestion", "level": "Low", "desc": "Lombok Strait transit is clear with negligible delay buffers."},
            {"category": "Destination Bottleneck", "level": "High", "desc": "Average 48-72 hr discharge anchorage wait times at Qingdao bulk terminal."}
        ]
    },
    "Ras Tanura (Saudi Arabia) ➔ Paradip (India) [Crude/Energy]": {
        "origin": {"name": "Ras Tanura", "lat": 26.64, "lon": 50.16},
        "dest": {"name": "Paradip", "lat": 20.26, "lon": 86.67},
        "waypoints": [(26.0, 56.5), (23.5, 59.0), (15.0, 68.0), (6.0, 79.5), (12.0, 84.0)],
        "distance_nm": 2850,
        "base_days": 10,
        "risks": [
            {"category": "Geopolitical Chokepoint", "level": "Medium", "desc": "Strait of Hormuz transit requires enhanced AIS monitoring and naval escort protocols."},
            {"category": "Metocean Conditions", "level": "Low", "desc": "Arabian Sea conditions stable; minimal swell resistance."},
            {"category": "Port Berth Allocation", "level": "Medium", "desc": "Moderate turnaround delays at Paradip SPM berths."}
        ]
    },
    "Rotterdam (Netherlands) ➔ Singapore [Container/General] via Suez": {
        "origin": {"name": "Rotterdam", "lat": 51.92, "lon": 4.47},
        "dest": {"name": "Singapore", "lat": 1.29, "lon": 103.85},
        "waypoints": [(36.0, -5.5), (37.0, 11.5), (31.5, 32.3), (12.5, 43.5), (6.0, 80.0), (5.5, 95.0)],
        "distance_nm": 8280,
        "base_days": 26,
        "risks": [
            {"category": "Security & Chokepoint", "level": "Critical", "desc": "Bab-el-Mandeb & Red Sea security alerts; insurance surcharges and rerouting via Cape of Good Hope add 10-12 days."},
            {"category": "Suez Canal Transit", "level": "High", "desc": "Convoy scheduling delays averaging 36-48 hours."},
            {"category": "Fuel Burn Variance", "level": "High", "desc": "Extended voyages increase bunker consumption by ~320 MT VLSFO."}
        ]
    },
    "Richards Bay (South Africa) ➔ Paradip (India) [Thermal Coal]": {
        "origin": {"name": "Richards Bay", "lat": -28.78, "lon": 32.04},
        "dest": {"name": "Paradip", "lat": 20.26, "lon": 86.67},
        "waypoints": [(-20.0, 45.0), (-5.0, 60.0), (5.0, 75.0), (12.0, 82.0)],
        "distance_nm": 4600,
        "base_days": 16,
        "risks": [
            {"category": "Weather Hazard", "level": "Medium", "desc": "South Indian Ocean cyclone season can induce 3.5m+ significant wave heights."},
            {"category": "Chokepoint Congestion", "level": "Low", "desc": "Open-ocean trajectory bypasses restricted international canals."},
            {"category": "Destination Demurrage", "level": "High", "desc": "High coal stockpiles at East Coast Indian ports cause prolonged berthing queues."}
        ]
    }
}

def render_route_risk_analyzer():
    st.markdown("---")
    st.subheader("🧭 Voyage Trajectory & Chokepoint Risk Engine")
    st.caption("Select origin-destination corridors to evaluate transit trajectories, chokepoint delays, and oceanic risks.")

    # 1. Route Selector
    selected_lane_key = st.selectbox(
        "Select Active Commercial Shipping Corridor:",
        list(TRADE_LANES.keys()),
        index=0
    )
    lane = TRADE_LANES[selected_lane_key]

    # 2. Voyage Metrics Bar
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nautical Distance", f"{lane['distance_nm']:,} NM")
    col2.metric("Estimated Steaming Time", f"{lane['base_days']} Days", "@ 12.5 kts")
    col3.metric("Key Chokepoints", f"{len(lane['waypoints'])} Corridors")
    
    # Calculate overall risk status
    critical_count = sum(1 for r in lane['risks'] if r['level'] == 'Critical')
    high_count = sum(1 for r in lane['risks'] if r['level'] == 'High')
    risk_summary = "CRITICAL" if critical_count > 0 else ("ELEVATED" if high_count > 0 else "NORMAL")
    col4.metric("Voyage Risk Rating", risk_summary, delta="-High Surcharges" if critical_count > 0 else "Optimal", delta_color="inverse")

    # 3. Route Plotting on Map
    # Assemble ordered path: Origin -> Waypoints -> Destination
    lats = [lane['origin']['lat']] + [wp[0] for wp in lane['waypoints']] + [lane['dest']['lat']]
    lons = [lane['origin']['lon']] + [wp[1] for wp in lane['waypoints']] + [lane['dest']['lon']]

    fig = go.Figure()

    # Draw navigation corridor line
    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        mode='lines+markers',
        line=dict(width=3, color='#00D2FF'),
        marker=dict(size=6, color='#FFA500'),
        name='Planned Voyage Path'
    ))

    # Mark Origin
    fig.add_trace(go.Scattergeo(
        lon=[lane['origin']['lon']],
        lat=[lane['origin']['lat']],
        mode='markers+text',
        text=[f"Origin: {lane['origin']['name']}"],
        textposition="top center",
        marker=dict(size=10, color='#39FF14', symbol='star'),
        name='Origin Port'
    ))

    # Mark Destination
    fig.add_trace(go.Scattergeo(
        lon=[lane['dest']['lon']],
        lat=[lane['dest']['lat']],
        mode='markers+text',
        text=[f"Dest: {lane['dest']['name']}"],
        textposition="top center",
        marker=dict(size=10, color='#FF3131', symbol='diamond'),
        name='Destination Port'
    ))

    fig.update_geos(
        projection_type="natural earth",
        showcoastlines=True,
        coastlinecolor="#2A2A2A",
        showland=True,
        landcolor="#161B22",
        showocean=True,
        oceancolor="#090C10",
        showcountries=True,
        countrycolor="#1F242C",
        fitbounds="locations"
    )

    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, t=20, b=10),
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # 4. Route Risk Assessment Matrix
    st.markdown("##### ⚠️ Route Hazards & Chokepoint Delays")
    r_cols = st.columns(len(lane['risks']))
    for idx, risk in enumerate(lane['risks']):
        with r_cols[idx]:
            border_color = "#FF3131" if risk['level'] == "Critical" else ("#FFA500" if risk['level'] == "High" else "#00D2FF")
            st.markdown(
                f"""
                <div style="background-color: #161B22; border-left: 4px solid {border_color}; padding: 10px 14px; border-radius: 6px; min-height: 120px;">
                    <span style="font-size: 11px; font-weight: bold; color: {border_color}; text-transform: uppercase;">[{risk['level']} Risk]</span><br>
                    <strong style="color: #FFF; font-size: 14px;">{risk['category']}</strong>
                    <p style="color: #A0AAB4; font-size: 12px; margin-top: 6px; line-height: 1.3;">{risk['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )