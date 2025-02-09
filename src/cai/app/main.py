import streamlit as st
from cai.versioning import init_dev_version


def init_session_state():
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


# Initialize development version
init_dev_version()
init_session_state()

st.set_page_config(
    page_title="CAI - Few-shot Examples Drafting Assistant",
    layout="wide",
)
st.title("Constitutional AI - Critique & Rewrite")

st.markdown("""
CAI is a tool designed to help create and refine critique+rewrite examples for Constitutional AI training, specifically focusing on the critique+rewrite step described in the [Constitutional AI paper](https://arxiv.org/pdf/2212.08073).

### 📖 Current Principle
The current implementation focuses on the following principle:

> The first letter of each sentence in the assistant's response should spell "ADAPTIVE".

### 🔍 Key Features

- **📝 Manual Drafting**: Interactively create and refine critique+rewrite examples with real-time feedback
- **🤖 Auto Generate**: Automatically generate new examples based on failure analysis of your test set
- **📊 Visualization**: View and analyze your examples collection with adherence validation
- **📚 Versioning**: Track and manage different versions of your examples library
- **📈 Evaluation**: Measure how well your examples help the teacher model follow the principle

""")
