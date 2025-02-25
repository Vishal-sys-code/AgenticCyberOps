# streamlit_app.py
import streamlit as st
from cybersecurity_pipeline import run_security_pipeline

# Inject custom CSS for styling
st.markdown(
    """
    <style>
    /* Style the report container with a light gray background and black text */
    .report-container {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        color: #000000;
        font-family: sans-serif;
    }
    /* Optionally, adjust sidebar styling */
    .css-1d391kg { 
        background: linear-gradient(135deg, #2e7bcf, #2e7bcf);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Cybersecurity Agent Dashboard")
st.markdown("### Welcome to the Cybersecurity Agent. Run a security scan on your target below!")
st.markdown("---")

# Sidebar configuration
st.sidebar.header("Agent Configuration")
st.sidebar.markdown(
    """
    **Allowed Scope:**  
    The agent will only scan targets within its allowed scope.  
    Currently, the allowed scope is set to:
    - **example.com**
    - **192.168.1.0/24**
    
    Any target outside this scope will not be scanned.
    """
)

# User input for target
target = st.sidebar.text_input("Enter Target (e.g., example.com):", value="example.com")

if st.sidebar.button("Run Security Scan"):
    with st.spinner("Running security scan..."):
        task_description = f"Scan {target} for open ports and directories"
        final_state = run_security_pipeline(task_description)
        # Debug: st.write("DEBUG: Final State", final_state)
        final_report = final_state.get("final_report", "No report generated.")
    st.success("Security scan complete!")
    
    st.subheader("Final Security Audit Report")
    st.markdown(f"<div class='report-container'>{final_report}</div>", unsafe_allow_html=True)
    
    st.subheader("Detailed Execution Logs")
    logs = final_state.get("logs", [])
    st.markdown("<div class='report-container'>" + "<br>".join(logs) + "</div>", unsafe_allow_html=True)