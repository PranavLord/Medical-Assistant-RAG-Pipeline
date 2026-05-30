# 🏥 MediBot - AI Medical Document Assistant

An intelligent medical assistant powered by RAG (Retrieval-Augmented Generation) that answers questions based on uploaded medical documents using AI embeddings and large language models.

**Live Demo:** https://medical-assistant-rag-pipeline.streamlit.app/

---

## ✨ Features

- 📄 **PDF Document Upload** - Upload multiple medical documents at once
- 🔍 **Semantic Search** - Find relevant information using AI embeddings
- 🤖 **AI-Powered Responses** - Get intelligent answers using Groq LLM
- 💬 **Chat Interface** - User-friendly Streamlit web interface
- 🚀 **Production Ready** - Deployed on Render (Backend) + Streamlit Cloud (Frontend)
- 🔐 **Secure** - Environment variables for API keys (no secrets in code)
- ⚡ **Fast** - Groq LLM provides near-instant responses

---

## 🏗️ Architecture

```
Streamlit Frontend
        ↓
   FastAPI Backend
        ↓
Pinecone Vector DB + Groq LLM + Google Embeddings
```

### Tech Stack

**Backend:**
- FastAPI (REST API)
- LangChain (RAG orchestration)
- Pinecone (Vector database)
- Groq API (LLM - Llama 3.3 70B)
- Google Generative AI (Embeddings)
- PyPDF (PDF processing)

**Frontend:**
- Streamlit (Web UI)
- Python Requests (API client)

**Deployment:**
- Render (Backend)
- Streamlit Cloud (Frontend)
- GitHub (Version control)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- API Keys:
  - [Google API Key](https://ai.google.dev/) (for embeddings)
  - [Groq API Key](https://console.groq.com/) (for LLM)
  - [Pinecone API Key](https://www.pinecone.io/) (for vector database)

### Local Development

#### 1. Clone Repository
```bash
git clone https://github.com/yourusername/Medical-Assistant.git
cd Medical-Assistant
```

#### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

#### 3. Install Dependencies
```bash
# Backend
cd server
pip install -r requirements.txt
cd ..

# Frontend
cd client
pip install -r requirements.txt
cd ..
```

#### 4. Setup Environment Variables
Create `.env` in the root directory:
```env
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=medicalindex
API_URL=http://127.0.0.1:8000
```

#### 5. Run Locally

**Terminal 1 - Backend:**
```bash
cd server
python main.py
# Backend runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd client
streamlit run app.py
# Frontend runs on http://localhost:8501
```

---

## 📖 How It Works

### 1. Upload Documents
- User uploads PDF files through Streamlit interface
- Files are sent to FastAPI backend
- PDFs are parsed and split into chunks (500 characters)
- Chunks are embedded using Google Generative AI
- Embeddings are stored in Pinecone vector database

### 2. Ask Questions
- User types a question in the chat interface
- Question is embedded using same model
- Pinecone searches for top-3 most similar document chunks
- Retrieved context + question is sent to Groq LLM
- LLM generates answer based on context
- Answer is displayed to user

### 3. Conversation History
- Chat history is maintained in Streamlit session
- Users can download conversation as file

---

## 🔌 API Endpoints

### Upload PDFs
```
POST /upload_pdfs/

Request:
  - files: List of PDF files

Response:
  {
    "messages": "Files processed and vectorstore updated"
  }
```

### Ask Question
```
POST /ask/

Request:
  - question: User question (string)

Response:
  {
    "answer": "Answer based on documents..."
  }
```

### Health Check
```
GET /health

Response:
  {
    "status": "healthy",
    "message": "Medical Assistant API is running"
  }
```

---

## 🌐 Deployment

### Deploy Backend to Render

1. Connect GitHub repository to Render
2. Create Web Service with:
   - **Build Command:** `pip install -r server/requirements.txt`
   - **Start Command:** `cd server && uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Set environment variables: `GOOGLE_API_KEY`, `GROQ_API_KEY`, `PINECONE_API_KEY`, `PINECONE_INDEX_NAME`
4. Deploy

**Backend URL:** `https://medical-assistant-api.onrender.com` (example)

### Deploy Frontend to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Connect GitHub repository
3. Set main file: `client/app.py`
4. Add secret in Settings: `API_URL = https://your-backend-url.onrender.com`
5. Deploy

**Frontend URL:** `https://medical-assistant-rag-pipeline.streamlit.app/`

---

## 📁 Project Structure

```
MEDICALASSISTANT/
├── server/                      # FastAPI Backend
│   ├── main.py                  # App entry point
│   ├── requirements.txt
│   ├── modules/
│   │   ├── llm.py              # LLM chain setup
│   │   ├── load_vectorstore.py # PDF processing & embeddings
│   │   ├── query_handlers.py   # Query processing
│   │   └── pdf_handlers.py
│   ├── routes/
│   │   ├── upload_pdfs.py      # /upload_pdfs/ endpoint
│   │   └── ask_question.py     # /ask/ endpoint
│   ├── middlewares/
│   │   └── exception_handlers.py
│   └── logger.py
│
├── client/                      # Streamlit Frontend
│   ├── app.py                   # Main app
│   ├── config.py                # Configuration
│   ├── requirements.txt
│   ├── components/
│   │   ├── chatUI.py           # Chat interface
│   │   ├── upload.py           # File upload
│   │   ├── settings.py         # Settings panel
│   │   └── history_download.py
│   └── utils/
│       └── api.py              # API client
│
├── .env.example                 # Environment template
├── .gitignore
├── README.md                    # This file
└── PROJECT_DOCUMENTATION.md     # Detailed documentation
```

---

## 🔐 Security

- **API Keys:** Stored in environment variables, never committed to GitHub
- **CORS:** Enabled for frontend-backend communication
- **Input Validation:** Pydantic models validate all inputs
- **.env in .gitignore:** Prevents accidental key exposure

---

## 🐛 Troubleshooting

### Backend Won't Connect
- Verify `API_URL` in `client/config.py`
- Check backend is running
- Ensure CORS is enabled (it is by default)

### Upload Fails
- Check API key validity
- Verify Pinecone index exists
- Check backend logs

### No Responses
- Ensure documents are uploaded
- Check Pinecone has vectors
- Verify Groq API key is valid

For more troubleshooting, see [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

---

## 📚 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Groq API Docs](https://console.groq.com/docs/text-chat)

---

## 📄 Environment Variables

Create `.env` file with these variables:

```env
# Google API for embeddings
GOOGLE_API_KEY=your_key_here

# Groq API for LLM
GROQ_API_KEY=your_key_here

# Pinecone Vector Database
PINECONE_API_KEY=your_key_here
PINECONE_INDEX_NAME=medicalindex

# Backend URL (for frontend)
API_URL=http://127.0.0.1:8000  # Local
# API_URL=https://your-backend.onrender.com  # Production
```

**Never commit .env file to GitHub!**

---

## 📊 Performance

- Upload 10-page PDF: 15-30 seconds
- Query response: 2-5 seconds
- Pinecone free tier: 100k vectors
- Groq: No rate limiting on free tier

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

- **Pranav** - Medical Assistant RAG Pipeline
- GitHub: [yourusername](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- [Google Generative AI](https://ai.google.dev/) for embeddings
- [Groq](https://groq.com/) for fast LLM inference
- [Pinecone](https://www.pinecone.io/) for vector database
- [LangChain](https://www.langchain.com/) for RAG orchestration
- [Streamlit](https://streamlit.io/) for web framework
- [Render](https://render.com/) for hosting

---

## 📞 Support

For issues and questions:
1. Check [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
2. Open an issue on GitHub
3. Contact: [your-email@example.com]

---

**Status:** ✅ Live in Production  
**Last Updated:** May 2026  
**Version:** 1.0.0
