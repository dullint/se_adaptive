import streamlit as st
from cai.auto_generate import analyze_failures, generate_improvement_examples
from cai.app.components.example_display import render_example
from cai.versioning import add_to_dev_examples, load_examples
from cai.eval import load_eval_data, assert_principle
from cai.critique_rewrite import run_critique_rewrite_pipeline
from cai.models import EvaluationResult

st.title("Auto-Generate Improvements")

if st.button("🤖 Auto-Generate Examples", type="primary", use_container_width=True):
    # Initialize session state for results if not exists
    if "auto_gen_results" not in st.session_state:
        st.session_state.auto_gen_results = []

    # Step 1: Load and evaluate examples
    st.subheader("🔄 Evaluating Validation Examples")
    eval_data = load_eval_data("validation")
    current_examples = load_examples("dev")

    # Create containers for live updates
    progress_bar = st.progress(0)
    results_container = st.container()
    stats_container = st.container()

    results = []

    # Process each example and show results in real-time
    for idx, example in enumerate(eval_data):
        with st.spinner(f"Processing example {idx + 1}/{len(eval_data)}..."):
            critique, rewrite = run_critique_rewrite_pipeline(
                example.human_prompt, example.assistant_answer, version="dev"
            )
            adherence, first_letters = assert_principle(rewrite)

            result = EvaluationResult(
                human_prompt=example.human_prompt,
                assistant_answer=example.assistant_answer,
                critique=critique,
                rewrite=rewrite,
                follows_principle=adherence,
                first_letters=first_letters,
            )
            results.append(result)

            # Update progress
            progress_bar.progress((idx + 1) / len(eval_data))

            # Show current example result
            with results_container:
                st.markdown(f"**Example {idx + 1}:**")
                render_example(
                    index=idx + 1,
                    human_prompt=example.human_prompt,
                    assistant_answer=example.assistant_answer,
                    critique=critique,
                    rewrite=rewrite,
                    show_adherence=True,
                    on_delete=None,
                )

    # Step 2: Analyze failures
    st.markdown("---")
    st.subheader("🔍 Failure Analysis")
    with st.spinner("Analyzing failure patterns..."):
        analysis = analyze_failures(results)
        st.markdown(analysis)
        st.success("✅ Analysis complete")

    # Step 3: Generate improvements
    st.markdown("---")
    st.subheader("✨ Generated Examples")
    with st.spinner("Generating improved examples..."):
        new_examples = generate_improvement_examples(results, analysis)

        # Show generated examples as they're created
        for i, example in enumerate(new_examples, 1):
            render_example(
                index=i,
                human_prompt=example.human_prompt,
                assistant_answer=example.assistant_answer,
                critique=example.critique,
                rewrite=example.rewrite,
                show_adherence=True,
                on_delete=None,
            )
        st.success("✅ Examples generated")

    # Add button to save examples
    if st.button("💾 Add Valid Examples to Dev", use_container_width=True):
        valid_examples = [
            example for example in new_examples if assert_principle(example.rewrite)
        ]
        for example in valid_examples:
            add_to_dev_examples(
                example.human_prompt,
                example.assistant_answer,
                example.critique,
                example.rewrite,
            )
        st.success(
            f"✨ Added {len(valid_examples)} valid generated examples to development version"
        )
        st.rerun()

else:
    st.info(
        "Click the button above to analyze the current examples and auto-generate improvements."
    )
