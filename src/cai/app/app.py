import streamlit as st
from cai.app.tabs.example_drafting import render_example_drafting
from cai.app.tabs.evaluation import render_evaluation


def main():
    """Main function for the Streamlit app."""
    # Make the layout wide
    st.set_page_config(layout="wide")

    st.title("Constitutional AI - Critique & Rewrite")

    st.markdown("""
    This tool helps create and test critique+rewrite examples for Constitutional AI.

    **Current principle**: The first letter of each sentence should spell 'ADAPTIVE'
    """)

    # Initialize session state
    if "model_answer" not in st.session_state:
        st.session_state.model_answer = ""
    if "critique" not in st.session_state:
        st.session_state.critique = ""
    if "rewrite" not in st.session_state:
        st.session_state.rewrite = ""

    # Create tabs
    tab1, tab2 = st.tabs(["Example Drafting", "Evaluation"])

    # Render content based on selected tab
    with tab1:
        render_example_drafting()

    with tab2:
        render_evaluation()


if __name__ == "__main__":
    main()
