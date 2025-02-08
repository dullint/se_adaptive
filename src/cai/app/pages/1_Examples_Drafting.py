import streamlit as st
from cai.app.components.prompt_input import render_prompt_input
from cai.critique_rewrite import run_critique_rewrite_pipeline, add_to_examples
from cai.eval import assert_principle

st.title("Examples Drafting")

# Create two columns for inputs with a small gap
human_prompt, model_answer = render_prompt_input()


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

        # Evaluate adherence to principle
        adherence, first_letters = assert_principle(st.session_state.rewrite)
        bg_color = "#e8f4ea" if adherence else "#fde7e9"  # Green if adheres, red if not

        st.markdown(
            f"""<div style="padding: 1rem; border-radius: 0.5rem; background-color: {bg_color}">
            {st.session_state.rewrite}
            </div>""",
            unsafe_allow_html=True,
        )

        # Add adherence indicator
        if adherence:
            st.success("✅ Response adheres to principle")
        else:
            st.error(f"❌ Response does not adhere to principle: {first_letters}")

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
            if st.button("📚 Add to Examples", use_container_width=True):
                add_to_examples(
                    human_prompt,
                    model_answer,
                    st.session_state.critique,
                    st.session_state.rewrite,
                )
                # Set flag to scroll to bottom of Examples tab
                st.session_state.scroll_to_new_example = True
                # Switch to Examples Visualization page
                st.switch_page("pages/2_Visualisation_&_Versioning.py")
        st.markdown("</div>", unsafe_allow_html=True)
