import streamlit as st


def render_settings():
    """Render app settings and preferences"""
    
    with st.sidebar:
        st.divider()
        st.subheader("⚙️ Settings", divider="gray")
        
        # App options
        st.markdown("**🔧 Options**")
        
        if st.button("🔄 Rerun", use_container_width=True, key="rerun_btn"):
            st.rerun()
        
        auto_rerun = st.checkbox(
            "♻️ Auto-refresh",
            value=False,
            help="Automatically refresh the page"
        )
        
        if st.button("🗑️ Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.toast("✅ Cache cleared!", icon="✅")
        
        st.divider()
        
        # App info
        st.markdown("**ℹ️ About**")
        st.info(
            """
            **MediBot v1.0**
            
            AI-powered medical document assistant built with:
            - Streamlit
            - FastAPI
            - LangChain
            - Pinecone
            - Google Generative AI
            """,
            icon="ℹ️"
        )
        
        st.caption("Made with ❤️ using Streamlit v1.58.0")
