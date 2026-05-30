import streamlit as st
from utils.api import upload_pdfs_api


def render_uploader():
    # Initialize session state for tracking uploaded files
    if "uploaded_file_info" not in st.session_state:
        st.session_state.uploaded_file_info = []
    
    if "file_uploader_key" not in st.session_state:
        st.session_state.file_uploader_key = 0
    
    # Display already uploaded files
    if st.session_state.uploaded_file_info:
        st.markdown("**📋 Uploaded Documents:**")
        for file_info in st.session_state.uploaded_file_info:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.caption(f"✅ {file_info['name']} ({file_info['size']} KB)")
            with col2:
                st.caption(f"Ready")
        
        st.divider()
        
        # Clear uploaded documents button
        if st.button("🗑️ Clear Uploaded Documents", use_container_width=True, type="secondary"):
            st.session_state.uploaded_file_info = []
            st.session_state.file_uploader_key += 1
            st.toast("✅ Uploaded documents cleared!", icon="✅")
            st.rerun()
        
        st.divider()
        st.markdown("**📤 Upload More Documents:**")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "📄 Select PDF Documents",
        type="pdf",
        accept_multiple_files=True,
        help="Upload one or multiple medical documents in PDF format",
        key=f"file_uploader_{st.session_state.file_uploader_key}"
    )
    
    if uploaded_files:
        st.write(f"**{len(uploaded_files)} file(s) selected:**")
        for file in uploaded_files:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.caption(f"📋 {file.name} ({file.size / 1024:.1f} KB)")
            with col2:
                st.caption(f"✓")
        
        col1, col2 = st.columns(2)
        with col1:
            upload_btn = st.button("📤 Upload to DB", use_container_width=True, type="primary")
        with col2:
            clear_btn = st.button("❌ Clear", use_container_width=True)
        
        if clear_btn:
            st.session_state.file_uploader_key += 1
            st.toast("✅ Files cleared!", icon="✅")
            st.rerun()
        
        if upload_btn:
            with st.spinner("📤 Uploading and processing documents..."):
                try:
                    response = upload_pdfs_api(uploaded_files)
                    if response.status_code == 200:
                        # Store file info for display
                        for file in uploaded_files:
                            st.session_state.uploaded_file_info.append({
                                "name": file.name,
                                "size": f"{file.size / 1024:.1f}"
                            })
                        
                        st.toast("✅ Documents uploaded and indexed successfully!", icon="✅")
                        st.toast("Your documents are now ready for queries!", icon="ℹ️")
                        # Clear after successful upload
                        st.session_state.file_uploader_key += 1
                        st.rerun()
                    else:
                        st.error(f"❌ Upload failed: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    elif not st.session_state.uploaded_file_info:
        st.info("👆 Upload PDF documents to get started")