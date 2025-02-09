import streamlit as st
from cai.models import EvaluationResult
from cai.eval import (
    load_eval_data,
    assert_principle,
    save_eval_report,
)
from cai.critique_rewrite import run_critique_rewrite_pipeline
from cai.versioning import save_dev_version, list_examples_versions
from cai.app.components.example_display import render_example


st.title("📈 Evaluation")

# Add version selector to evaluation page
st.sidebar.subheader("📚 Examples Version")
versions = list_examples_versions()
version = st.sidebar.selectbox(
    "Select Version",
    versions,
    help="Select which version to use for few-shot examples",
)

# Load evaluation data
eval_data = load_eval_data("test")

st.subheader("Evaluation Results")
st.markdown(f"Testing {len(eval_data)} examples from the test set")

# Add a button to run evaluation
if st.button("🚀 Run Evaluation", type="primary", use_container_width=True):
    # First save current dev as new version
    if version == "dev":
        version = save_dev_version()
        st.info(f"✨ Created new version: {version}")

    # Show progress bar
    progress_bar = st.progress(0)
    results: list[EvaluationResult] = []

    # Process each example
    for idx, example in enumerate(eval_data):
        # Run critique and rewrite
        with st.spinner("Running critique and rewrite..."):
            critique, rewrite = run_critique_rewrite_pipeline(
                example.human_prompt, example.assistant_answer, version
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

    # Show final statistics
    st.markdown("---")
    st.subheader("📊 Evaluation Summary")
    success_rate = sum(1 for r in results if r.follows_principle) / len(results)
    st.metric(
        "Success Rate",
        f"{success_rate:.1%}",
        help="Percentage of rewrites that follow the ADAPTIVE principle",
    )

    # Save evaluation report
    report_path = save_eval_report(results, version, success_rate)
    st.success(f"Evaluation report saved to: {report_path}")

else:
    st.info("Click the button above to start the evaluation process.")
