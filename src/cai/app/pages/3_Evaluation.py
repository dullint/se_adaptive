import streamlit as st
from cai.entities import CritiqueRewriteExample
from cai.eval import load_eval_data, assert_principle, run_critique_rewrite_pipeline
from cai.versioning import list_examples_versions
from cai.app.components.example_display import render_example

st.title("Evaluation")

# Add version selector to evaluation page
st.sidebar.subheader("📚 Examples Version")
versions = list_examples_versions()
version = st.sidebar.selectbox(
    "Select Version",
    versions,
    help="Select which version to use for few-shot examples",
)

# Load evaluation data
eval_data = load_eval_data()

st.subheader("Evaluation Results")
st.markdown(f"Testing {len(eval_data)} examples from the eval set")

# Add a button to run evaluation
if st.button("🚀 Run Evaluation", type="primary", use_container_width=True):
    # Show progress bar
    progress_bar = st.progress(0)
    results = []

    # Process each example
    for idx, example in enumerate(eval_data):
        # Run critique and rewrite
        with st.spinner("Running critique and rewrite..."):
            critique, rewrite = run_critique_rewrite_pipeline(
                example["human_prompt"], example["assistant_answer"]
            )
            results.append(
                CritiqueRewriteExample(
                    human_prompt=example["human_prompt"],
                    assistant_answer=example["assistant_answer"],
                    critique=critique,
                    rewrite=rewrite,
                )
            )

        # Display example using component
        render_example(
            index=idx + 1,
            human_prompt=example["human_prompt"],
            assistant_answer=example["assistant_answer"],
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
    success_rate = sum(1 for ex in results if assert_principle(ex.rewrite)[0]) / len(
        results
    )
    st.metric(
        "Success Rate",
        f"{success_rate:.1%}",
        help="Percentage of rewrites that follow the ADAPTIVE principle",
    )

else:
    st.info("Click the button above to start the evaluation process.")
