import streamlit as st
from cai.app.components.example_display import render_example
from cai.auto_generate import analyze_failures, generate_improvement_examples
from cai.critique_rewrite import run_critique_rewrite_pipeline
from cai.eval import assert_principle, load_eval_data
from cai.models import EvaluationResult
from cai.versioning import add_to_dev_examples

st.title("🤖 Auto-Generate")

eval_data = load_eval_data("validation")
st.markdown(f"Testing {len(eval_data)} examples from the validation set")

if st.button("🤖 Auto-Generate Examples", type="primary", use_container_width=True):
    progress_bar = st.progress(0)
    results: list[EvaluationResult] = []

    # Process each example
    for idx, example in enumerate(eval_data):
        # Run critique and rewrite
        with st.spinner("Running critique and rewrite..."):
            critique, rewrite = run_critique_rewrite_pipeline(
                example.human_prompt, example.assistant_answer, version="dev"
            )
            # Check adherence
            adherence, first_letters = assert_principle(rewrite)

            # Store result
            result = EvaluationResult(
                human_prompt=example.human_prompt,
                assistant_answer=example.assistant_answer,
                critique=critique,
                rewrite=rewrite,
                follows_principle=adherence,
                first_letters=first_letters,
            )
            results.append(result)

        # Display example using component
        render_example(
            index=idx + 1,
            human_prompt=example.human_prompt,
            assistant_answer=example.assistant_answer,
            critique=critique,
            rewrite=rewrite,
            show_adherence=True,
            on_delete=None,  # No delete functionality in evaluation
        )

        # Update progress
        progress_bar.progress((idx + 1) / len(eval_data))

    # Show analysis
    st.subheader("🔍 Failure Analysis")
    analysis = analyze_failures(results)
    failures = [r for r in results if not r.follows_principle]
    if len(failures) == 0:
        st.info("No failures found. No improvements to generate.")
    else:
        st.markdown(analysis)

        # Show generated examples
        st.subheader("✨ Generated Examples")
        new_examples = generate_improvement_examples(results, analysis)
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

        # Add button to save examples
        if st.button("💾 Add Examples to Dev", use_container_width=True):
            for example in new_examples:
                add_to_dev_examples(
                    example.human_prompt,
                    example.assistant_answer,
                    example.critique,
                    example.rewrite,
                )
            st.success("✨ Added generated examples to development version")
            st.rerun()
else:
    st.info(
        "Click the button above to analyze the current examples and auto-generate improvements."
    )
