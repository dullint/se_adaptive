import streamlit as st
from cai.app.components.prompt_input import render_prompt_input
from cai.critique_rewrite import (
    run_critique_rewrite_pipeline,
    run_rewrite_pipeline,
    run_critique_refinement,
)
from cai.versioning import add_to_dev_examples
from cai.eval import assert_principle
from cai.app.components.example_display import render_example

st.title("📝 Manual Drafting")


def on_text_change(new_value, key):
    st.session_state[key] = new_value


# Initialize history in session state if not exists
if "iteration_history" not in st.session_state:
    st.session_state.iteration_history = []

# Display previous iterations if they exist
if st.session_state.iteration_history:
    st.subheader("Previous Iterations")
    for i, iteration in enumerate(st.session_state.iteration_history, 1):
        render_example(
            index=i,
            human_prompt=iteration["human_prompt"],
            assistant_answer=iteration["assistant_answer"],
            critique=iteration["critique"],
            rewrite=iteration["rewrite"],
            show_adherence=True,
            on_delete=None,
        )
    st.subheader("Current Iteration")

# Full width prompt input
human_prompt, model_answer = render_prompt_input()

# Critique & Rewrite button
if st.button("✨ Critique & Rewrite", use_container_width=True, type="primary"):
    if human_prompt and model_answer:
        with st.spinner("Running critique and rewrite..."):
            critique, rewrite = run_critique_rewrite_pipeline(
                human_prompt, model_answer, version="dev"
            )
            st.session_state.critique = critique
            st.session_state.rewrite = rewrite
    else:
        st.error("Please provide both a prompt and a model answer.")

# Display results if they exist
if st.session_state.get("critique") or st.session_state.get("rewrite"):
    st.markdown("<br>", unsafe_allow_html=True)

    # Editable critique section with refinement
    st.subheader("🔍 Critique")

    # Original critique display
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

    # Critique refinement section
    with st.expander("✨ Refine Critique", expanded=False):
        refinement_prompt = st.text_area(
            "Refinement Instructions",
            placeholder="Explain how you want to refine the critique...",
            help="Describe what aspects of the critique need to be changed or improved",
            key="refinement_prompt",
        )

        if st.button("✨Regenerate Critique", use_container_width=True):
            if refinement_prompt:
                with st.spinner("Refining critique..."):
                    refined_critique = run_critique_refinement(
                        human_prompt,
                        model_answer,
                        critique,
                        refinement_prompt,
                    )
                    st.session_state.critique = refined_critique
                    st.rerun()
            else:
                st.error("Please provide refinement instructions.")

    # Add regenerate rewrite button after critique
    if st.button("🔄 Regenerate Rewrite", use_container_width=True):
        with st.spinner("Regenerating rewrite based on the critique..."):
            rewrite = run_rewrite_pipeline(
                human_prompt, model_answer, st.session_state.critique, version="dev"
            )
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

    # Action buttons for critique/rewrite results
    st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("↩️ Run New Iteration", use_container_width=True):
            # Save current iteration to history before starting new one
            st.session_state.iteration_history.append(
                {
                    "human_prompt": human_prompt,
                    "assistant_answer": model_answer,
                    "critique": st.session_state.critique,
                    "rewrite": st.session_state.rewrite,
                }
            )
            # Set up new iteration with rewrite as the model answer
            st.session_state.model_answer = st.session_state.rewrite
            st.session_state.critique = ""
            st.session_state.rewrite = ""
            st.rerun()

    with col2:
        if st.button("📚 Add to Examples", use_container_width=True):
            add_to_dev_examples(
                human_prompt,
                model_answer,
                st.session_state.critique,
                st.session_state.rewrite,
            )
            st.session_state.scroll_to_new_example = True
            st.switch_page("pages/3_Visualisation_&_Versioning.py")
    st.markdown("</div>", unsafe_allow_html=True)

# Always show reset button at bottom of page
if st.button(
    "🔄 Reset All",
    use_container_width=True,
    type="secondary",
    help="Clear all inputs and history to start fresh",
):
    # Clear all state variables including history
    st.session_state.human_prompt = ""
    st.session_state.model_answer = ""
    st.session_state.critique = ""
    st.session_state.rewrite = ""
    st.session_state.iteration_history = []
    st.rerun()
