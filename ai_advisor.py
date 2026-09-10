import streamlit as st
from google import genai
from google.genai import types

# Cache the client so Python doesn't close the connection between chat messages
@st.cache_resource
def get_gemini_client():
    api_key = st.secrets["GEMINI_API_KEY"]
    return genai.Client(api_key=api_key)

def render_ai_advisor(current_rate: float, projected_low: float):
    st.markdown("---")
    st.subheader("🤖 OptiFreight AI Strategic Copilot")
    st.caption("Powered by Gemini. Ask natural-language queries regarding chartering decisions, route risks, and cost hedging.")

    # 1. Initialize Gemini Client securely and keep it open
    try:
        client = get_gemini_client()
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
        st.session_state.chat_session = client.chats.create(
            model="gemini-3.7-flash",
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

    # 5. Handle Live User Input
    if prompt := st.chat_input("Ask about chartering timing, Suez Canal delays, fuel hedging..."):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Google API Error: {str(e)}")