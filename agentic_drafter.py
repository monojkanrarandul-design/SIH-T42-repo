import streamlit as st
from groq import Groq

# Reuse the cached Groq client
@st.cache_resource
def get_groq_client():
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        return Groq(api_key=api_key)
    except KeyError:
        return None

def render_agentic_drafter(projected_low: float, cargo_volume: int = 75000):
    st.markdown("---")
    st.subheader("⚡ Agentic Execution: Auto-Draft Fixture Recap")
    st.caption("Translate predictive analytics directly into executable commercial contracts.")

    if st.button("Generate Binding Term Sheet (Email Draft)", type="secondary"):
        client = get_groq_client()
        if not client:
            st.error("Groq API Key not found. Please check your Streamlit Secrets.")
            return

        with st.spinner("AI Agent is drafting the commercial terms..."):
            # Prompting the LLM to act as a broker using real maritime terminology
            prompt = f"""
            Act as an expert maritime chartering broker. Draft a short, highly professional 'Fixture Recap' email to a shipowner offering to fix a Panamax vessel.
            Target Freight Rate: ${projected_low:.2f} per Metric Ton.
            Cargo Quantity: {cargo_volume} MT Bulk.
            Include standard maritime abbreviations like FIOST (Free In, Out, Stowed, and Trimmed) and SHINC (Sundays and Holidays Included).
            Do not include pleasantries. Keep it under 150 words.
            """
            
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="openai/gpt-oss-20b", 
                    temperature=0.2,
                )
                
                draft = chat_completion.choices[0].message.content
                
                st.text_area("📋 Copy/Paste to Email Client:", value=draft, height=250)
                st.success("Draft generated and ready for dispatch.")
                
            except Exception as e:
                st.error(f"Agent Execution Error: {str(e)}")