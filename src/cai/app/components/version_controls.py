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

    # Save version button
    if st.sidebar.button("💾 Save Current Version", use_container_width=True):
        new_version = save_dev_version()
        st.sidebar.success(f"✨ Saved as version: {new_version}")
        st.rerun()

    # Add reload controls if viewing dev version
    if version == "dev":
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔄 Reload Saved Version to Dev")

        # Version selector for reload
        reload_version = st.sidebar.selectbox(
            "Select version to reload from",
            [v for v in versions if v != "dev"],
            help="Select a version to reload the development examples from",
            key="reload_version",
        )

        # Reload button
        if st.sidebar.button(
            "🔄 Reload from selected version", use_container_width=True
        ):
            reload_dev_from_version(reload_version)
            st.sidebar.success(
                f"✨ Development examples reloaded from {reload_version}"
            )
            st.rerun()

    return version
