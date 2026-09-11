import streamlit as st
from fpdf import FPDF

def render_pdf_report(current_rate: float, projected_low: float):
    st.markdown("---")
    st.subheader("💼 Executive Board Report")
    st.caption("Generate a downloadable PDF summarizing the current maritime intelligence and procurement strategy.")

    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", size=16, style="B")
        pdf.cell(200, 10, txt="OptiFreight Strategic Chartering Report", ln=True, align="C")
        pdf.ln(10)
        
        # Market Data
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Current Market Spot Rate: ${current_rate:.2f} / Ton", ln=True)
        pdf.cell(200, 10, txt=f"Projected 30-Day Low: ${projected_low:.2f} / Ton", ln=True)
        pdf.ln(10)
        
        # AI Recommendation Summary
        pdf.set_font("Arial", size=12, style="B")
        pdf.cell(200, 10, txt="AI Copilot Recommendation:", ln=True)
        pdf.set_font("Arial", size=12)
        
        recommendation = (
            "Delay contract finalization by 10-14 days. Spot rates are trending downward. "
            "High congestion at the Suez Canal adds a 2-day transit buffer. "
            "Targeting the projected low window will maximize capital efficiency and offset VLSFO fuel price volatility."
        )
        pdf.multi_cell(0, 10, txt=recommendation)
        
        # Footer
        pdf.ln(15)
        pdf.set_font("Arial", size=10, style="I")
        pdf.cell(200, 10, txt="Generated automatically by the OptiFreight Intelligence Engine.", ln=True)
        
        # Return as raw bytes for the Streamlit download button
        return pdf.output(dest='S').encode('latin-1')

    # Generate the PDF byte data
    pdf_bytes = create_pdf()

    # Streamlit native download button
    st.download_button(
        label="📄 Download Executive Strategy PDF",
        data=pdf_bytes,
        file_name="OptiFreight_Board_Report.pdf",
        mime="application/pdf",
        type="primary"
    )