import streamlit as st
from google import genai
from google.genai import types

def render_ai_advisor(current_rate: float, projected_low: float):
    st.markdown("---")
    st.subheader("🤖 OptiFreight AI Strategic Copilot")
    st.caption("Powered by Gemini. Ask natural-language queries regarding chartering decisions, route risks, and cost hedging.")

    # 1. Initialize Gemini Client
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)
    except KeyError:
        st.error("API Key not found. Please check your Streamlit Secrets.")
        return

    # 2. Define the System Persona
    system_instruction = (
        "You are the OptiFreight Maritime AI Copilot. You advise enterprise procurement officers on bulk cargo and vessel chartering. "
        f"The current spot rate is ${current_rate:.2f}/ton. "
        f"The projected 30-day low is ${projected_low:.2f}/ton. "
        "Recommend waiting to charter if the projection is lower. Keep answers concise, professional, and business-focused."
    )

    # 3. Initialize the chat session
    if "chat_session" not in st.session_state:
        # Switched to the universally available 1.5-flash model
        st.session_state.chat_session = client.chats.create(
            model="gemini-1.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2, 
            )
        )
        st.session_state.messages = [
            {"role": "assistant", "content": f"Greetings. I am your OptiFreight Copilot. Current rates sit at **${current_rate:.2f}**. How can I assist your chartering desk today?"}
        ]

    # 4. Display history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 5. Handle Live User Input with Error Catching
    if prompt := st.chat_input("Ask about chartering timing, Suez Canal delays, fuel hedging..."):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Attempt to get the AI response
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # If it fails, print the exact error safely without crashing
                st.error(f"Google API Error: {str(e)}")
                st.info("Double-check that your API key in Streamlit Secrets has no extra spaces and is wrapped in quotes like this: `GEMINI_API_KEY = \"AIza...\"`")