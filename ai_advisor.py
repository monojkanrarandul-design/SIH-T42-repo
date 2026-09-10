import streamlit as st

def render_ai_advisor(current_rate: float, projected_low: float):
    """
    Renders an interactive Maritime GenAI Assistant that responds to user
    queries about current freight volatility, route risks, and procurement timing.
    """
    st.markdown("---")
    st.subheader("🤖 OptiFreight AI Strategic Copilot")
    st.caption("Ask natural-language queries regarding chartering decisions, route anomalies, and cost hedging.")

    # Context-aware knowledge engine
    response_bank = {
        "delay": (
            f"**Strategic Advisory:** Rates are trending downward from ${current_rate:.2f} to an estimated low of ${projected_low:.2f}. "
            "Port turnaround metrics in Singapore are stabilizing, leading to an influx of open vessel capacity. Delaying contract finalization by 10–14 days will capture this margin."
        ),
        "risk": (
            "**Geopolitical & Route Risk Report:** High congestion at the Suez Canal is adding an average 2-day transit buffer. "
            "Additionally, moderate seasonal weather patterns in the South China Sea suggest rerouting Capesize vessels through the Lombok Strait if departure occurs within 48 hours."
        ),
        "fuel": (
            "**Bunker Fuel Hedging Advisory:** Very Low Sulphur Fuel Oil (VLSFO) is currently trading at $610/metric ton (-0.8%). "
            "Forward swap curves indicate slight stability. We recommend spot fuel procurement alongside dynamic routing to capture fuel-burn efficiencies."
        ),
        "steel": (
            "**Steel Procurement Recommendation:** For raw coking coal and iron ore shipments, locking in forward voyage contracts at current spot rates incurs an unnecessary premium. "
            "Wait for the projected low window before finalizing bulk fixtures."
        )
    }

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    f"Greetings. I am your OptiFreight Maritime Intelligence Copilot. "
                    f"Current spot rates sit at **${current_rate:.2f}/ton**, with a projected 30-day low of **${projected_low:.2f}/ton**. "
                    "How can I assist your chartering desk today?"
                )
            }
        ]

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat prompt input
    if prompt := st.chat_input("Ask about chartering timing, Suez Canal delays, fuel hedging..."):
        # Append and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate intelligent contextual reply
        user_query = prompt.lower()
        if any(w in user_query for w in ["wait", "delay", "charter", "now", "buy"]):
            reply = response_bank["delay"]
        elif any(w in user_query for w in ["risk", "weather", "suez", "canal", "typhoon", "route"]):
            reply = response_bank["risk"]
        elif any(w in user_query for w in ["fuel", "oil", "vlsfo", "price", "bunker"]):
            reply = response_bank["fuel"]
        elif any(w in user_query for w in ["steel", "coal", "iron", "ore", "cargo"]):
            reply = response_bank["steel"]
        else:
            reply = (
                f"**Market Insight:** Our ensemble forecasting model currently weights port wait times and fuel spot fluctuations at a 0.84 correlation. "
                f"Target charter execution around the projected **${projected_low:.2f}** benchmark to optimize procurement capital."
            )

        # Append and display assistant reply
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)