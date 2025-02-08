import streamlit as st
from cai.versioning import init_dev_version

# Initialize development version
init_dev_version()


st.set_page_config(
    page_title="CAI - Few-shot Examples Drafting Assistant",
    layout="wide",
)

# Main content
st.title("Constitutional AI - Critique & Rewrite")

st.markdown("""
This tool helps create and test critique+rewrite examples for Constitutional AI.

**Current principle**: The first letter of each sentence should spell 'ADAPTIVE'
""")

# Initialize session state
if "human_prompt" not in st.session_state:
    st.session_state.human_prompt = ""
if "model_answer" not in st.session_state:
    st.session_state.model_answer = ""
if "critique" not in st.session_state:
    st.session_state.critique = ""
if "rewrite" not in st.session_state:
    st.session_state.rewrite = ""
if "selected_version" not in st.session_state:
    st.session_state.selected_version = "dev"
