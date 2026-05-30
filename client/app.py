import streamlit as st
from components.upload import render_uploader
from components.chatUI import render_chat
from components.settings import render_settings


st.set_page_config(
    page_title="MediBot - AI Medical Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "### MediBot v1.0\nAI-powered medical document assistant"}
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 12px 16px;
    }
    .st-emotion-cache-1c7y2kd {
        padding: 2rem 1rem;
    }
    .header-title {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 10px;
    }
    .header-subtitle {
        color: #666;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .chat-container {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        padding: 12px;
        border-radius: 4px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([1, 3])
with col1:
    st.empty()
with col2:
    st.markdown("<h1 style='margin-top: 10px;'>🏥 MediBot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; margin-top: -10px;'><b>Your Intelligent Medical Document Assistant</b></p>", unsafe_allow_html=True)

# Divider
st.divider()

# Two column layout
left_col, right_col = st.columns([1, 3.5], gap="large")

with left_col:
    st.subheader("📁 Documents", divider="blue")
    render_uploader()
    st.divider()
    render_settings()

with right_col:
    st.subheader("💬 Conversation", divider="blue")
    render_chat()