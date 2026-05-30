import streamlit as st
from utils.api import ask_question
from datetime import datetime


def render_chat():
    # Initialize session state for user info
    if "user_name" not in st.session_state:
        st.session_state.user_name = None
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "message_timestamps" not in st.session_state:
        st.session_state.message_timestamps = []

    # User name input section
    if not st.session_state.user_name:
        st.info("👤 Please enter your name to start chatting", icon="ℹ️")
        user_name = st.text_input(
            "Your Name",
            placeholder="Enter your full name",
            help="Your name will be used to personalize responses and name exported files"
        )
        
        if user_name:
            if st.button("✅ Start Chat", use_container_width=True, type="primary"):
                st.session_state.user_name = user_name
                st.toast(f"👋 Welcome, {user_name}!", icon="👋")
                st.rerun()
        return
    
    # Display user name
    st.caption(f"👤 **Logged in as:** {st.session_state.user_name}")
    st.divider()

    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history with improved styling
        if st.session_state.messages:
            for i, msg in enumerate(st.session_state.messages):
                if msg["role"] == "user":
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(f"**You**")
                        st.markdown(msg["content"])
                        if i < len(st.session_state.message_timestamps):
                            st.caption(f"_{st.session_state.message_timestamps[i]}_")
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(f"**MediBot**")
                        st.markdown(msg["content"])
                        if i < len(st.session_state.message_timestamps):
                            st.caption(f"_{st.session_state.message_timestamps[i]}_")
        else:
            # Welcome message
            st.info(
                f"""
                👋 **Welcome {st.session_state.user_name}!**
                
                I'm your AI medical assistant. Ask me questions about your medical documents 
                and I'll help you understand the content better.
                
                **Tips:**
                - Upload medical documents (PDFs) in the left panel
                - Ask specific questions about your documents
                - I'll provide accurate answers based on the document content
                """,
                icon="ℹ️"
            )

    # Input section with improved styling
    st.divider()
    
    col1, col2 = st.columns([0.85, 0.15])
    
    with col1:
        user_input = st.chat_input(
            "Ask me anything about your medical documents...",
            key="chat_input"
        )
    
    with col2:
        clear_chat = st.button("🗑️ Clear Chat", use_container_width=True)
    
    if clear_chat:
        # Backup messages before clearing for export
        st.session_state.exported_messages = st.session_state.messages.copy()
        st.session_state.exported_timestamps = st.session_state.message_timestamps.copy()
        # Clear current display
        st.session_state.messages = []
        st.session_state.message_timestamps = []
        st.toast("✅ Chat cleared!", icon="✅")
        st.rerun()

    # Process user input
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        timestamp = datetime.now().strftime("%I:%M %p")
        st.session_state.message_timestamps.append(timestamp)
        
        # Display user message
        with chat_container:
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"**You**")
                st.markdown(user_input)
                st.caption(f"_{timestamp}_")
        
        # Get response with loading indicator
        with st.spinner("🔍 Analyzing your question..."):
            try:
                response = ask_question(user_input)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    
                    # Add assistant message
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    timestamp = datetime.now().strftime("%I:%M %p")
                    st.session_state.message_timestamps.append(timestamp)
                    
                    # Display assistant message
                    with chat_container:
                        with st.chat_message("assistant", avatar="🤖"):
                            st.markdown(f"**MediBot**")
                            st.markdown(answer)
                            st.caption(f"_{timestamp}_")
                    
                    st.toast("✅ Response generated successfully!", icon="✅")
                else:
                    st.error(f"❌ Error: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
    
    # Initialize session state for tracking exports
    if "exported_messages" not in st.session_state:
        st.session_state.exported_messages = []

    # Export and user options - at the bottom
    st.divider()
    
    user_name = st.session_state.get("user_name", "user")
    has_messages = st.session_state.get("messages") and len(st.session_state.messages) > 0
    
    if has_messages or st.session_state.exported_messages:
        st.markdown("**📥 Export Chat**")
        
        # Use current messages if available, otherwise use exported messages
        messages_to_export = st.session_state.messages if has_messages else st.session_state.exported_messages
        timestamps_to_export = st.session_state.message_timestamps if has_messages else st.session_state.get("exported_timestamps", [])
        
        # Format chat history with timestamps
        chat_text = f"MEDICAL ASSISTANT CHAT HISTORY\n"
        chat_text += f"User: {user_name}\n"
        chat_text += f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        chat_text += "=" * 50 + "\n\n"
        
        for i, msg in enumerate(messages_to_export):
            role = "YOU" if msg["role"] == "user" else "MEDIBOT"
            timestamp = timestamps_to_export[i] if i < len(timestamps_to_export) else "N/A"
            chat_text += f"[{timestamp}] {role}:\n"
            chat_text += f"{msg['content']}\n"
            chat_text += "-" * 50 + "\n\n"
        
        # Generate filename with user name and date
        filename = f"{user_name}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        st.download_button(
            label="📥 Download Report",
            data=chat_text,
            file_name=filename,
            mime="text/plain",
            use_container_width=True,
            type="secondary"
        )
        
        st.divider()
        
        # Confirmation before switching user
        st.warning("⚠️ Changing user will clear all chat history!")
        col1, col2 = st.columns(2)
        with col1:
            confirm_download = st.checkbox("✅ I've downloaded my report", value=False, key=f"confirm_{user_name}")
        
        if confirm_download:
            with col2:
                if st.button("🔄 Change User", use_container_width=True, type="secondary"):
                    st.session_state.user_name = None
                    st.session_state.messages = []
                    st.session_state.message_timestamps = []
                    st.session_state.exported_messages = []
                    st.session_state.exported_timestamps = []
                    st.session_state.uploaded_file_info = []
                    st.session_state.file_uploader_key = 0
                    st.toast("✅ User changed! Please enter your name again.", icon="✅")
                    st.rerun()
    else:
        # No messages - let them change user freely
        if st.button("🔄 Change User", use_container_width=True, type="secondary"):
            st.session_state.user_name = None
            st.session_state.messages = []
            st.session_state.message_timestamps = []
            st.session_state.uploaded_file_info = []
            st.session_state.file_uploader_key = 0
            st.toast("✅ User changed! Please enter your name again.", icon="✅")
            st.rerun()