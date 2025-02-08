import streamlit as st
from cai.critique_rewrite import (
    load_example_library,
    delete_example,
)
from cai.library_versions import list_library_versions, save_dev_version

st.title("Example Library Visualization")
# Version selector in sidebar
st.sidebar.subheader("📚 Library Versions")

versions = list_library_versions()
version = st.sidebar.selectbox(
    "Select Version",
    versions,
    help="Select a saved version or view current development version",
)

# Save version button
if st.sidebar.button("💾 Save Current Version", use_container_width=True):
    new_version = save_dev_version()
    st.sidebar.success(f"✨ Saved as version: {new_version}")
    st.rerun()

# Load examples from selected version
examples = load_example_library(None if version == "Dev" else version)

# Display library info
st.subheader(
    f"Currently visualizing: {'Development Version' if version == 'Dev' else version} "
    f"({len(examples)} examples)"
)

# If we just added a new example, show success message
if st.session_state.get("scroll_to_new_example", False):
    st.success("✨ Example successfully added to the library!")
    st.session_state.scroll_to_new_example = False

# Create container for examples
examples_container = st.container()

with examples_container:
    # Display each example
    for i, example in enumerate(examples, 1):
        # Create a row for the example header and delete button
        header_col1, header_col2 = st.columns([6, 1])
        with header_col1:
            st.subheader(f"Example {i}")
        with header_col2:
            if st.button("🗑️", key=f"delete_{i}", help="Delete this example"):
                delete_example(i - 1)
                st.success("Example deleted successfully!")
                st.rerun()

        # Create two columns for prompt and response
        col1, col2 = st.columns([1, 1], gap="medium")

        with col1:
            st.subheader("👤 Human Prompt")
            st.markdown(
                f"""<div style="padding: 1rem; border-radius: 0.5rem; background-color: #f0f2f6">
                {example.human_prompt}
                </div>""",
                unsafe_allow_html=True,
            )

        with col2:
            st.subheader("🤖 Model Answer")
            st.markdown(
                f"""<div style="padding: 1rem; border-radius: 0.5rem; background-color: #f0f2f6">
                {example.assistant_answer}
                </div>""",
                unsafe_allow_html=True,
            )

        # Show critique and rewrite
        st.markdown("<br>", unsafe_allow_html=True)
        res_col1, res_col2 = st.columns([1, 1], gap="medium")

        with res_col1:
            st.subheader("🔍 Critique")
            st.markdown(
                f"""<div style="padding: 1rem; border-radius: 0.5rem; background-color: #f0f2f6">
                {example.critique}
                </div>""",
                unsafe_allow_html=True,
            )

        with res_col2:
            st.subheader("✏️ Rewritten Response")
            st.markdown(
                f"""<div style="padding: 1rem; border-radius: 0.5rem; background-color: #f0f2f6">
                {example.rewrite}
                </div>""",
                unsafe_allow_html=True,
            )

        # Add spacing between examples
        st.markdown("<br><hr><br>", unsafe_allow_html=True)

# Add empty space at the bottom to ensure the last example is fully visible
st.markdown("<br><br><br>", unsafe_allow_html=True)
