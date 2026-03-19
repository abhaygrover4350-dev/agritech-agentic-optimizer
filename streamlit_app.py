import streamlit as st
from agritech_crew import run_optimization

st.set_page_config(page_title="Gangakoshi Optimizer", layout="wide")
st.title("🌾 Gangakoshi Agritech Agentic Supply Chain Optimizer")

st.subheader("Scenario")
scenario_input = st.text_area(
    "Type any weather scenario (or keep default):",
    value="A monsoon is hitting Punjab in 3 days; optimize the wheat supply chain.",
    height=100
)

if st.button("🚀 Run Full Agentic Optimization", type="primary", use_container_width=True):
    with st.spinner("3 AI agents working... (30-45 seconds)"):
        report_text, pdf_file, used_scenario = run_optimization(scenario_input)
        
        st.success(f"✅ Optimization complete for: **{used_scenario}**")
        st.markdown(report_text)
        
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📥 Download Professional PDF Report",
                data=f,
                file_name=pdf_file,
                mime="application/pdf"
            )

st.caption("Pro tip: Try different scenarios like 'severe drought in Haryana' for interviews!")