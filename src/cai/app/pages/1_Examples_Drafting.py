import streamlit as st
from cai.app.components.prompt_input import render_prompt_input
from cai.critique_rewrite import (
    run_critique_rewrite_pipeline,
    add_to_examples,
    run_rewrite_pipeline,
)
from cai.eval import assert_principle

st.title("Examples Drafting")


def on_text_change(new_value, key):
    st.session_state[key] = new_value


# Full width prompt input
human_prompt, model_answer = render_prompt_input()

# Critique & Rewrite button
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
if st.session_state.get("critique") or st.session_state.get("rewrite"):
    st.markdown("<br>", unsafe_allow_html=True)

    # Editable critique
    st.subheader("🔍 Critique")
    critique = st.text_area(
        "Critique:",
        value=st.session_state.get("critique", ""),
        height=200,
        key="critique_input",
        label_visibility="collapsed",
        on_change=on_text_change,
        args=(st.session_state.critique, "critique"),
    )
    st.session_state.critique = critique

    # Add regenerate button after critique
    if st.button("🔄 Regenerate Rewrite", use_container_width=True):
        with st.spinner("Regenerating rewrite based on the newcritique..."):
            # Here we'll need to add a function to generate just the rewrite
            rewrite = run_rewrite_pipeline(human_prompt, model_answer, critique)
            st.session_state.rewrite = rewrite
            st.rerun()

    # Editable rewrite with adherence check
    st.subheader("✏️ Rewritten Response")
    rewrite = st.text_area(
        "Rewrite:",
        value=st.session_state.get("rewrite", ""),
        height=200,
        key="rewrite_input",
        label_visibility="collapsed",
        on_change=on_text_change,
        args=(st.session_state.rewrite, "rewrite"),
    )
    st.session_state.rewrite = rewrite

    # Check adherence if there's a rewrite
    if rewrite:
        adherence, first_letters = assert_principle(rewrite)
        bg_color = "#e8f4ea" if adherence else "#fde7e9"

        # Show adherence status
        if adherence:
            st.success("✅ Response adheres to principle")
        else:
            st.error(f"❌ Response does not adhere to principle: {first_letters}")

    # Action buttons
    st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("↩️ Run New Iteration", use_container_width=True):
            st.session_state.model_answer = rewrite
            st.session_state.critique = ""
            st.session_state.rewrite = ""
            st.rerun()

    with col2:
        if st.button("📚 Add to Examples", use_container_width=True):
            add_to_examples(
                human_prompt,
                model_answer,
                critique,
                rewrite,
            )
            st.session_state.scroll_to_new_example = True
            st.switch_page("pages/2_Visualisation_&_Versioning.py")

    with col3:
        if st.button(
            "🔄 Reset",
            use_container_width=True,
            type="secondary",
            help="Clear all inputs and start fresh",
        ):
            st.session_state.human_prompt = ""
            st.session_state.model_answer = ""
            st.session_state.critique = ""
            st.session_state.rewrite = ""
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
