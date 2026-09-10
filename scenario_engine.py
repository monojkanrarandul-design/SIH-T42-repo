import streamlit as st

def render_scenario_calculator(current_rate: float, projected_low: float):
    """
    Renders an interactive Enterprise ROI & What-If Scenario Simulator.
    Allows judges/clients to calculate exact dollar savings for bulk cargo shipments.
    """
    st.markdown("---")
    st.subheader("💼 Enterprise ROI & What-If Scenario Simulator")
    st.caption("Adjust bulk cargo volume and benchmark vessel classes to simulate capital savings.")

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("##### ⚙️ Procurement Parameters")
        
        vessel_class = st.selectbox(
            "Vessel Benchmark Class",
            [
                "Panamax (65,000 - 85,000 DWT) - Coal / Grain",
                "Capesize (120,000 - 200,000 DWT) - Iron Ore",
                "Supramax (50,000 - 60,000 DWT) - General Bulk"
            ],
            index=0
        )
        
        # Default cargo tonnage based on vessel class selection
        default_tonnage = 75000 if "Panamax" in vessel_class else (160000 if "Capesize" in vessel_class else 55000)
        
        cargo_volume = st.slider(
            "Total Cargo Volume (Metric Tons)",
            min_value=10000,
            max_value=250000,
            value=default_tonnage,
            step=5000,
            help="Drag to simulate custom shipment sizes."
        )

        fuel_contingency = st.slider(
            "Bunker Fuel Fluctuation Offset (%)",
            min_value=-15,
            max_value=15,
            value=0,
            step=1,
            help="Simulate changes in global bunker fuel prices."
        )

    with col2:
        # Dynamic calculations
        baseline_cost = cargo_volume * current_rate
        adjusted_forecast_rate = projected_low * (1 + (fuel_contingency / 100))
        optimized_cost = cargo_volume * adjusted_forecast_rate
        net_savings = baseline_cost - optimized_cost
        savings_percentage = (net_savings / baseline_cost) * 100

        st.markdown("##### 📈 Projected Financial Balance Sheet")
        
        metric_col1, metric_col2 = st.columns(2)
        metric_col1.metric("Spot Rate Outlay", f"${baseline_cost:,.0f}")
        metric_col2.metric("Optimized Outlay", f"${optimized_cost:,.0f}", f"-{savings_percentage:.1f}%")

        st.metric(
            label="🎯 Projected Capital Savings (Per Voyage)",
            value=f"${net_savings:,.0f}",
            delta=f"{savings_percentage:.1f}% Bottom-line Gain"
        )

        if net_savings > 0:
            st.success(
                f"**Procurement Recommendation:** By timing the charter window for **{cargo_volume:,} MT**, "
                f"the enterprise saves approximately **${net_savings:,.0f}**. "
                "This single decision pays for an enterprise SaaS subscription for multiple quarters."
            )
        else:
            st.warning("**Hedging Advisory:** Volatility spike detected. Lock in spot rate charter to minimize risk exposure.")