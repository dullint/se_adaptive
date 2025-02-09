import streamlit as st


def render_action_buttons(
    rewrite: str, on_use_new=None, add_to_dev_examples=None
) -> None:
    """Renders the action buttons below rewritten response.

    Args:
        rewrite: The rewritten text to use as new answer
        on_use_new: Callback when "Use as New Answer" is clicked
        on_add_to_version: Callback when "Add to Examples" is clicked
    """
    st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("↩️ Run New Eteration", use_container_width=True):
            if on_use_new:
                on_use_new(rewrite)

    with col2:
        if st.button("📚 Add to Dev Examples", use_container_width=True):
            if add_to_dev_examples:
                add_to_dev_examples()

    st.markdown("</div>", unsafe_allow_html=True)
