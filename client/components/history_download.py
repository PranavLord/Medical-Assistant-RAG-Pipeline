import streamlit as st
from datetime import datetime


def render_history_download():
    st.markdown("**📥 Export**")
    
    if st.session_state.get("messages") and len(st.session_state.messages) > 0:
        user_name = st.session_state.get("user_name", "user")
        
        # Format chat history with timestamps
        chat_text = f"MEDICAL ASSISTANT CHAT HISTORY\n"
        chat_text += f"User: {user_name}\n"
        chat_text += f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        chat_text += "=" * 50 + "\n\n"
        
        for i, msg in enumerate(st.session_state.messages):
            role = "YOU" if msg["role"] == "user" else "MEDIBOT"
            timestamp = st.session_state.message_timestamps[i] if i < len(st.session_state.message_timestamps) else "N/A"
            chat_text += f"[{timestamp}] {role}:\n"
            chat_text += f"{msg['content']}\n"
            chat_text += "-" * 50 + "\n\n"
        
        # Generate filename with user name and date
        filename = f"{user_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        st.download_button(
            label="📥 Download Chat History",
            data=chat_text,
            file_name=filename,
            mime="text/plain",
            use_container_width=True,
            type="secondary"
        )
    else:
        st.caption("💬 No chat history to export yet")
    
    # Logout button to change user
    if st.button("🔄 Change User", use_container_width=True):
        st.session_state.user_name = None
        st.session_state.messages = []
        st.session_state.message_timestamps = []
        st.toast("✅ User changed! Please enter your name again.", icon="✅")
        st.rerun()