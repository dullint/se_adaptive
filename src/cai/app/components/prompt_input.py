import streamlit as st
from cai.llm import run_model


def render_prompt_input() -> tuple[str, str]:
    """Renders the prompt and model answer input fields.

    Args:
        on_generate: Optional callback when generate button is clicked

    Returns:
        Tuple of (human_prompt, model_answer)
    """
    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.subheader("👤 Human Prompt")
        human_prompt = st.text_area(
            "Enter your prompt:",
            value=st.session_state.human_prompt,
            height=200,
            placeholder="Type your prompt here...",
            label_visibility="collapsed",
            key="human_prompt_input",
        )
        st.session_state.human_prompt = human_prompt
    with col2:
        st.subheader("🤖 Model Answer")
        model_answer = st.text_area(
            "Model answer:",
            value=st.session_state.model_answer,
            height=200,
            placeholder="Type or generate model answer...",
            label_visibility="collapsed",
            key="model_answer_input",
        )
        st.session_state.model_answer = model_answer

        button_text = (
            "🤖 Generating..."
            if "generating" in st.session_state and st.session_state.generating
            else "🤖 Generate Answer"
        )
        if st.button(
            button_text,
            use_container_width=True,
            disabled="generating" in st.session_state and st.session_state.generating,
        ):
            if human_prompt:
                st.session_state.generating = True
                st.rerun()
            else:
                st.error("Please enter a prompt first.")

        if "generating" in st.session_state and st.session_state.generating:
            model_answer = run_model(human_prompt)
            st.session_state.model_answer = model_answer
            st.session_state.generating = False
            st.rerun()

    return human_prompt, model_answer
