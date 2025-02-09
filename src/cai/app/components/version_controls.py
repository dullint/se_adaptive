import streamlit as st
from cai.versioning import (
    list_examples_versions,
    save_dev_version,
    reload_dev_from_version,
)


def render_version_controls() -> str:
    """Renders the version control UI in the sidebar.

    Returns:
        str: Currently selected version
    """
    st.sidebar.subheader("📚 Examples Versions")

    versions = list_examples_versions()
    version = st.sidebar.selectbox(
        "Select Version",
        versions,
        help="Select a saved version or view current development version",
    )

    # Show appropriate action button based on selected version
    if version == "dev":
        if st.sidebar.button("💾 Save Current Version", use_container_width=True):
            new_version = save_dev_version()
            st.sidebar.success(f"✨ Saved as version: {new_version}")
            st.rerun()
    else:
        if st.sidebar.button("🔄 Reload to Dev", use_container_width=True):
            reload_dev_from_version(version)
            st.sidebar.success(f"✨ Development examples reloaded from {version}")
            st.rerun()

    return version
