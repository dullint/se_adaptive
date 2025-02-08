import streamlit as st
from cai.domain import CritiqueRewriteExample
from cai.eval import load_eval_data, assert_principle, run_critique_rewrite_pipeline


def render_evaluation():
    """Render the evaluation tab content."""

    # Load evaluation data
    eval_data = load_eval_data()

    st.subheader("Evaluation Results")
    st.markdown(f"Testing {len(eval_data)} examples from the dev set")

    # Add a button to run evaluation
    if st.button("🚀 Run Evaluation", type="primary", use_container_width=True):
        # Show progress bar
        progress_bar = st.progress(0)
        results = []

        # Process each example
        for idx, example in enumerate(eval_data):
            st.markdown("---")

            # Create columns for the example number and validation result
            header_col1, header_col2 = st.columns([4, 1])
            with header_col1:
                st.subheader(f"Example {idx + 1}")

            # Display human prompt
            st.markdown("**Human Prompt:**")
            st.markdown(f"```\n{example.human_prompt}\n```")

            # Display original answer
            st.markdown("**Original Answer:**")
            st.markdown(f"```\n{example.assistant_answer}\n```")

            # Run critique and rewrite
            with st.spinner("Running critique and rewrite..."):
                critique, rewrite = run_critique_rewrite_pipeline(
                    example.human_prompt, example.assistant_answer
                )
                results.append(
                    CritiqueRewriteExample(
                        human_prompt=example.human_prompt,
                        assistant_answer=example.assistant_answer,
                        critique=critique,
                        rewrite=rewrite,
                    )
                )

            # Display critique
            st.markdown("**Critique:**")
            st.markdown(
                f"""<div style="padding: 1rem; border-radius: 0.5rem; background-color: #f0f2f6">
                {critique}
                </div>""",
                unsafe_allow_html=True,
            )

            # Display rewrite and validation
            st.markdown("**Rewritten Response:**")
            follows_principle = assert_principle(rewrite)

            # Use different colors based on validation result
            bg_color = "#e7f5ea" if follows_principle else "#ffe6e6"
            status_icon = "✅" if follows_principle else "❌"

            st.markdown(
                f"""<div style="padding: 1rem; border-radius: 0.5rem; background-color: {bg_color}">
                {rewrite}
                </div>""",
                unsafe_allow_html=True,
            )

            # Display validation result
            with header_col2:
                st.markdown(
                    f"<h3 style='text-align: right'>{status_icon}</h3>",
                    unsafe_allow_html=True,
                )

            # Update progress
            progress_bar.progress((idx + 1) / len(eval_data))

        # Show final statistics
        st.markdown("---")
        st.subheader("📊 Evaluation Summary")
        success_rate = sum(1 for ex in results if assert_principle(ex.rewrite)) / len(
            results
        )
        st.metric(
            "Success Rate",
            f"{success_rate:.1%}",
            help="Percentage of rewrites that follow the ADAPTIVE principle",
        )

    else:
        st.info("Click the button above to start the evaluation process.")
