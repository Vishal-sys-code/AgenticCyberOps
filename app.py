import streamlit as st
import html
from cybersecurity_pipeline import run_security_pipeline

st.set_page_config(page_title="Cybersecurity Scanner", layout="wide")

# Inject custom CSS for styling (make sure this string is not indented unexpectedly)
st.markdown(
"""<style>
.big-title { 
    font-size: 36px; 
    font-weight: bold; 
    color: #FF4B4B; 
    text-align: center; 
}
.sub-title { 
    font-size: 24px; 
    font-weight: bold; 
    color: #FFFFFF; 
    background-color: #333; 
    padding: 10px; 
    border-radius: 5px; 
}
.report-box { 
    background-color: #F5F5F5; 
    padding: 10px; 
    border-radius: 5px; 
    border-left: 5px solid #FF4B4B; 
    color: #000000;
    font-family: sans-serif;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🔍 Cybersecurity Agent Dashboard</p>', unsafe_allow_html=True)

st.sidebar.header("Agent Configuration")
st.sidebar.markdown(
    """
    **Allowed Scope:**  
    The agent will only scan targets within its allowed scope.  
    Currently, the allowed scope is set to (Universal links or any link):
    - **example.com**
    - **192.168.1.0/24**
    - **scanme.nmap.org**, etc...
    """
)

target = st.sidebar.text_input("Enter Target (e.g., example.com):", value="example.com")

if st.sidebar.button("Run Security Scan"):
    with st.spinner("Running security scan..."):
        task_description = f"Scan {target} for open ports and directories"
        final_state = run_security_pipeline(task_description)
        final_report = final_state.get("final_report", "No report generated.")
        logs = final_state.get("logs", [])
    
    st.success("Security scan complete!")
    
    st.markdown('<p class="sub-title">Final Security Audit Report</p>', unsafe_allow_html=True)
    # Escape HTML to display it as plain text
    escaped_report = html.escape(final_report)
    st.markdown(f'<div class="report-box"><pre>{escaped_report}</pre></div>', unsafe_allow_html=True)
    
    st.markdown('<p class="sub-title">Detailed Execution Logs</p>', unsafe_allow_html=True)
    st.text_area("Logs", "\n".join(logs), height=300)