import streamlit as st
from cai.app.components.version_controls import render_version_controls
from cai.critique_rewrite import delete_example
from cai.versioning import load_examples
from cai.app.components.example_display import render_example

st.title("Examples Visualization")

version = render_version_controls()

# Load examples from selected version
examples = load_examples(version)

# Display version info
st.subheader(f"Currently visualizing version {version} " f"({len(examples)} examples)")

# If we just added a new example, show success message
if st.session_state.get("scroll_to_new_example", False):
    st.success("✨ Example successfully added to the examples!")
    st.session_state.scroll_to_new_example = False

st.markdown("<hr>", unsafe_allow_html=True)

# Create container for examples
examples_container = st.container()

with examples_container:
    # Display each example
    for i, example in enumerate(examples, 1):
        render_example(
            index=i,
            human_prompt=example.human_prompt,
            assistant_answer=example.assistant_answer,
            critique=example.critique,
            rewrite=example.rewrite,
            show_adherence=False,
            on_delete=lambda: delete_example(i - 1, version) and st.rerun(),
        )

# Add empty space at the bottom to ensure the last example is fully visible
st.markdown("<br><br><br>", unsafe_allow_html=True)
