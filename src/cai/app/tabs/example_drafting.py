import streamlit as st
from cai.critique_rewrite import run_critique_rewrite_pipeline
from cai.llm import run_model


def render_example_drafting():
    """Render the example drafting tab content."""
    # Create two columns for inputs with a small gap
    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.subheader("Human Prompt")
        human_prompt = st.text_area(
            "Enter your prompt:",
            height=200,
            placeholder="Type your prompt here...",
            label_visibility="collapsed",
        )

    with col2:
        st.subheader("Model Answer")
        model_answer = st.text_area(
            "Model answer:",
            value=st.session_state.model_answer,
            height=200,
            placeholder="Type or generate model answer...",
            label_visibility="collapsed",
            key="model_answer_input",
        )

        # Update session state when text area changes
        st.session_state.model_answer = model_answer

        # Generate button right under the model answer
        if st.button("🤖 Generate Answer", use_container_width=True):
            if human_prompt:
                with st.spinner("Generating response..."):
                    st.session_state.model_answer = run_model(human_prompt)
                    st.rerun()
            else:
                st.error("Please enter a prompt first.")

    # Add some vertical spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Critique & Rewrite button centered below both columns
    col_button = st.columns([2, 1, 2])[1]  # Create a centered column
    with col_button:
        if st.button("✨ Critique & Rewrite", use_container_width=True, type="primary"):
            if human_prompt and model_answer:
                with st.spinner("Running critique and rewrite..."):
                    critique, rewrite = run_critique_rewrite_pipeline(
                        human_prompt, model_answer
                    )
                    st.session_state.critique = critique
                    st.session_state.rewrite = rewrite
            else:
                st.error("Please provide both a prompt and a model answer.")

    # Display results if they exist
    if st.session_state.critique or st.session_state.rewrite:
        # Add some vertical spacing
        st.markdown("<br>", unsafe_allow_html=True)

        # Results in two columns
        res_col1, res_col2 = st.columns([1, 1], gap="medium")

        with res_col1:
            st.subheader("🔍 Critique")
            st.markdown(
                f"""<div style="padding: 1rem; border-radius: 0.5rem; background-color: #f0f2f6">
                {st.session_state.critique}
                </div>""",
                unsafe_allow_html=True,
            )

        with res_col2:
            st.subheader("✏️ Rewritten Response")
            st.markdown(
                f"""<div style="padding: 1rem; border-radius: 0.5rem; background-color: #f0f2f6">
                {st.session_state.rewrite}
                </div>""",
                unsafe_allow_html=True,
            )
