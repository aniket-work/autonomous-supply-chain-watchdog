import streamlit as st
from supply_chain_watchdog.agent import get_supply_chain_agent
import sys
import os

# Adust path to ensure imports work if running from root or subfolder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(
    page_title="Autonomous Supply Chain Watchdog",
    page_icon="📦",
    layout="wide"
)

# Custom CSS for a better look
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

st.title("📦 Autonomous Supply Chain Watchdog")
st.markdown("### AI-Powered Supply Chain Risk Analysis & Monitoring")

with st.sidebar:
    st.header("Configuration")
    model_choice = st.selectbox("Select Model", ["gpt-4o", "gpt-3.5-turbo"], index=0)
    st.info("This agent uses DuckDuckGo Search to find real-time supply chain news.")

query_input = st.text_input("Enter a commodity, company, or sector to analyze:", placeholder="e.g., Lithium, TSMC, Automotive Chips")

if st.button("Analyze Risks", type="primary"):
    if query_input:
        with st.status("🔍 Agent is working...", expanded=True) as status:
            st.write("Initializing Agent...")
            agent = get_supply_chain_agent(model_id=model_choice)
            
            st.write(f"Searching for news on '{query_input}'...")
            # We capture the output to show the reasoning steps if possible, 
            # but Phidata stream/print is mainly console. 
            # We will just get the final response for the UI.
            
            try:
                response = agent.run(f"Analyze the supply chain risks regarding: {query_input}")
                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                
                st.divider()
                st.markdown("## 🛡️ Risk Analysis Report")
                st.markdown(response.content)
                
            except Exception as e:
                status.update(label="❌ Error occurred", state="error")
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a topic to analyze.")

st.markdown("---")
st.caption("Experimental PoC | Powered by Phidata & OpenAI")
