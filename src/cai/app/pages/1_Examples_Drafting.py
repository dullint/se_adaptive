import streamlit as st
from cai.critique_rewrite import run_critique_rewrite_pipeline, add_to_examples
from cai.llm import run_model

st.title("Examples Drafting")

# Create two columns for inputs with a small gap
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("👤 Human Prompt")
    human_prompt = st.text_area(
        "Enter your prompt:",
        height=200,
        placeholder="Type your prompt here...",
        label_visibility="collapsed",
    )

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


# Wrap the button in a div for centering and sizing
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
st.markdown("</div>", unsafe_allow_html=True)

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

        # Add margin above the action buttons
        st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("↩️ Use as New Answer", use_container_width=True):
                st.session_state.model_answer = st.session_state.rewrite
                # Clear the critique and rewrite to avoid confusion
                st.session_state.critique = ""
                st.session_state.rewrite = ""
                st.rerun()

        with col2:
            if st.button("📚 Add to Example Library", use_container_width=True):
                add_to_examples(
                    human_prompt,
                    model_answer,
                    st.session_state.critique,
                    st.session_state.rewrite,
                )
                # Set flag to scroll to bottom of Examples tab
                st.session_state.scroll_to_new_example = True
                # Switch to Examples Library page
                st.switch_page("pages/2_Examples_Library.py")
        st.markdown("</div>", unsafe_allow_html=True)
