import streamlit as st
from groq import Groq

# Cache the client so it stays open
@st.cache_resource
def get_groq_client():
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        return Groq(api_key=api_key)
    except KeyError:
        return None

def render_ai_advisor(current_rate: float, projected_low: float):
    st.markdown("---")
    st.subheader("🤖 OptiFreight AI Strategic Copilot")
    st.caption("Powered by Llama 3 via Groq. Ask natural-language queries regarding chartering decisions or route risks.")

    client = get_groq_client()
    
    if not client:
        st.error("GROQ_API_KEY not found in Streamlit Secrets.")
        return

    # Initialize chat history
    if "messages" not in st.session_state:
        # The system prompt ensures it stays in character but allows it to gracefully deflect off-topic stuff
        st.session_state.system_prompt = {
            "role": "system",
            "content": (
                "You are the OptiFreight Maritime AI. You advise on bulk cargo chartering. "
                f"Current spot rate: ${current_rate:.2f}. Projected 30-day low: ${projected_low:.2f}. "
                "Recommend waiting if the projection is lower. "
                "If the user asks an off-topic question (like politics, weather, or jokes), politely say that you only have data regarding global maritime logistics."
            )
        }
        st.session_state.messages = [
            {"role": "assistant", "content": f"Greetings. I am your OptiFreight Copilot. Current rates sit at **${current_rate:.2f}**. How can I assist your chartering desk today?"}
        ]

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle Input
    if prompt := st.chat_input("Ask about chartering timing, Suez Canal delays, fuel hedging..."):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Build the message array with the system prompt first
                api_messages = [st.session_state.system_prompt] + [
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ]
                
                # Call a verified open source model runs on groq
                chat_completion = client.chat.completions.create(
                    messages=api_messages,
                    model="openai/gpt-oss-20b",
                    temperature=0.2,
                )
                
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"Groq API Error: {str(e)}")