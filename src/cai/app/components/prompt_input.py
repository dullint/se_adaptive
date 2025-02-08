import streamlit as st
from cai.llm import run_model


def on_text_change(new_value, key):
    st.session_state[key] = new_value


def render_prompt_input() -> tuple[str, str]:
    """Renders the prompt and model answer input fields.

    Returns:
        Tuple of (human_prompt, model_answer)
    """
    # Full width human prompt
    st.subheader("👤 Human Prompt")
    human_prompt = st.text_area(
        "Enter your prompt:",
        value=st.session_state.get("human_prompt", ""),
        height=200,
        placeholder="Type your prompt here...",
        label_visibility="collapsed",
        key="human_prompt_input",
        on_change=on_text_change,
        args=(st.session_state.human_prompt, "human_prompt"),
    )
    st.session_state.human_prompt = human_prompt

    # Generate button
    if st.button(
        "🤖 Generate Answer",
        use_container_width=True,
        disabled="generating" in st.session_state and st.session_state.generating,
    ):
        if human_prompt:
            st.session_state.generating = True
            st.rerun()
        else:
            st.error("Please enter a prompt first.")

    # Model answer text area
    st.subheader("🤖 Model Answer")
    model_answer = st.text_area(
        "Model answer:",
        value=st.session_state.get("model_answer", ""),
        height=200,
        placeholder="Click generate or type model answer...",
        label_visibility="collapsed",
        key="model_answer_input",
        on_change=on_text_change,
        args=(st.session_state.model_answer, "model_answer"),
    )
    st.session_state.model_answer = model_answer

    # Handle generation
    if "generating" in st.session_state and st.session_state.generating:
        with st.spinner("Generating response..."):
            model_answer = run_model(human_prompt)
            st.session_state.model_answer = model_answer
            st.session_state.generating = False
            st.rerun()

    return human_prompt, model_answer
