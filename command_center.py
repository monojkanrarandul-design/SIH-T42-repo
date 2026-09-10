import streamlit as st

def render_live_ticker():
    """
    Renders a scrolling, stock-ticker style marquee at the top of the dashboard 
    to simulate a live maritime intelligence command center.
    """
    # The simulated live intelligence feed
    ticker_text = (
        "🚨 LIVE MARITIME INTEL: "
        "&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; ⚠️ SUEZ CANAL: Congestion up 14% (Delay: +2 days) "
        "&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; 🟢 SOUTH CHINA SEA: Typhoon risk downgraded. Normal routing resumed. "
        "&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; 📉 VLSFO BUNKER: Spot price dropped to $610/mt in Singapore Hub "
        "&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; 🚢 BALTIC DRY INDEX: Down 1.2% in the last 24hrs "
        "&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; ⚠️ PORT OF SHANGHAI: Wait times stabilizing at 36 hours."
    )
    
    # HTML/CSS wrapper for the scrolling marquee
    html_string = f"""
    <div style="background-color: #0E1117; padding: 12px; border-radius: 8px; border: 1px solid #333; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
        <marquee direction="left" scrollamount="6" style="color: #00D2FF; font-family: 'Courier New', monospace; font-size: 15px; font-weight: bold; letter-spacing: 1px;">
            {ticker_text}
        </marquee>
    </div>
    """
    
    # Inject into Streamlit
    st.markdown(html_string, unsafe_allow_html=True)