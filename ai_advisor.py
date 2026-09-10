import streamlit as st
from google import genai
from google.genai import types

def render_ai_advisor(current_rate: float, projected_low: float):
    st.markdown("---")
    st.subheader("🤖 OptiFreight AI Strategic Copilot")
    st.caption("Powered by Gemini. Ask natural-language queries regarding chartering decisions, route risks, and cost hedging.")

    # 1. Initialize Gemini Client securely using Streamlit Secrets
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)
    except KeyError:
        st.error("API Key not found. Please add GEMINI_API_KEY to your Streamlit secrets.")
        return

    # 2. Define the System Persona and Rules
    system_instruction = (
        "You are the OptiFreight Maritime AI Copilot. You advise enterprise procurement officers on bulk cargo and vessel chartering. "
        f"The current spot rate is ${current_rate:.2f}/ton. "
        f"The projected 30-day low is ${projected_low:.2f}/ton. "
        "Recommend waiting to charter if the projection is lower. Keep answers concise, professional, and business-focused. "
        "You must politely refuse to answer any questions unrelated to maritime logistics, shipping, or the provided data."
    )

    # 3. Initialize the chat session in Streamlit state
    if "chat_session" not in st.session_state:
        # Create a stateful chat session
        st.session_state.chat_session = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2, # Low temperature for consistent, factual answers
            )
        )
        # Initialize UI message history
        st.session_state.messages = [
            {"role": "assistant", "content": f"Greetings. I am your OptiFreight Copilot. Current rates sit at **${current_rate:.2f}**. How can I assist your chartering desk today?"}
        ]

    # 4. Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 5. Handle Live User Input
    if prompt := st.chat_input("Ask about chartering timing, Suez Canal delays, fuel hedging..."):
        
        # Display user prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display Gemini response
        with st.chat_message("assistant"):
            # Send message to the active chat session
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
            
            # Save assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response.text})