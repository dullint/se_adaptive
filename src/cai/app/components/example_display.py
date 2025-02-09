import streamlit as st
from cai.eval import assert_principle


def render_example(
    index: int,
    human_prompt: str,
    assistant_answer: str,
    critique: str,
    rewrite: str,
    show_adherence: bool,
    on_delete=None,
) -> None:
    """Renders a single example with all its components.

    Args:
        index: Example number
        human_prompt: The human prompt text
        assistant_answer: The assistant's answer
        critique: The critique text
        rewrite: The rewritten answer
        on_delete: Optional callback function when delete button is clicked
    """
    # Create a row for the example header and delete button
    header_col1, header_col2 = st.columns([6, 1])
    with header_col1:
        st.subheader(f"Example {index}")
    with header_col2:
        if on_delete and st.button(
            "🗑️", key=f"delete_{index}", help="Delete this example"
        ):
            on_delete()
            st.rerun()

    # Display human prompt
    st.markdown("**Human Prompt:**")
    st.markdown(f"```\n{human_prompt}\n```")

    # Display original answer
    st.markdown("**Original Answer:**")
    st.markdown(f"```\n{assistant_answer}\n```")

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

    bg_color = "#f0f2f6"  # Default grey background
    if show_adherence:
        adherence, first_letters = assert_principle(rewrite)
        bg_color = "#e8f4ea" if adherence else "#fde7e9"  # Green if adheres, red if not
        if adherence:
            rewrite += "<br><br>✅ Response adheres to principle"
        else:
            rewrite += (
                f"<br><br>❌ Response does not adhere to principle: {first_letters}"
            )

    st.markdown(
        f"""<div style="padding: 1rem; border-radius: 0.5rem; background-color: {bg_color}">
        {rewrite}
        </div>""",
        unsafe_allow_html=True,
    )

    # Add spacing between examples
    st.markdown("<hr>", unsafe_allow_html=True)
