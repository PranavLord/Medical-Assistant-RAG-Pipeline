# MediBot - Medical Assistant RAG Pipeline
## Complete Project Documentation

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Core Components](#core-components)
6. [How It Works](#how-it-works)
7. [Setup Instructions](#setup-instructions)
8. [Deployment Guide](#deployment-guide)
9. [API Reference](#api-reference)
10. [Environment Variables](#environment-variables)
11. [Future Projects Checklist](#future-projects-checklist)
12. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

**MediBot** is an AI-powered medical document assistant that:
- Takes PDF documents as input
- Extracts and embeds text using Google Generative AI
- Stores embeddings in Pinecone vector database
- Answers questions based on document content using RAG (Retrieval-Augmented Generation)
- Uses Groq LLM for intelligent response generation

**Current Deployment:**
- Backend: Render (FastAPI)
- Frontend: Streamlit Cloud

**Live URL:** https://medical-assistant-rag-pipeline.streamlit.app/

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                       │
│         (medical-assistant-rag-pipeline.streamlit.app)      │
│                                                               │
│  ┌─────────────┬──────────────────────────┬──────────────┐  │
│  │   Upload    │     Chat Interface       │  Settings    │  │
│  │   PDFs      │  (Ask Questions)         │  (History)   │  │
│  └──────┬──────┴──────────┬───────────────┴──────────────┘  │
│         │                 │                                   │
└─────────┼─────────────────┼───────────────────────────────────┘
          │                 │
          │ HTTP Requests   │
          ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│              (Render Web Service)                           │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │          /upload_pdfs/    (POST)                      │  │
│  │  • Receives PDF files                                 │  │
│  │  • Splits text into chunks                            │  │
│  │  • Creates embeddings                                 │  │
│  │  • Stores in Pinecone                                 │  │
│  └─────────────────────┬─────────────────────────────────┘  │
│                        │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │          /ask/    (POST)                             │  │
│  │  • Receives user question                            │  │
│  │  • Embeds question                                   │  │
│  │  • Searches Pinecone (top-k=3)                        │  │
│  │  • Passes context to LLM                              │  │
│  │  • Returns answer                                     │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
└──────┬─────────────────────────────────────────────────────┬─┘
       │                                                       │
       ▼                                                       ▼
┌─────────────────────────────┐               ┌──────────────────────┐
│   Pinecone Vector Store     │               │  Groq API            │
│   (Serverless, AWS)         │               │  (LLM: llama-3.3)    │
│   Index: medicalindex       │               │  70B Versatile Model │
│   Dimension: 3072           │               │                      │
│   Metric: Cosine            │               └──────────────────────┘
└─────────────────────────────┘
       ▲                                            ▲
       │                                            │
       └────────────────────┬──────────────────────┘
                            │
                   Google Generative AI
                   (Embeddings API)
                   models/gemini-embedding-001
```

---

## 🛠️ Tech Stack

### Backend
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | FastAPI | REST API server |
| **Server** | Uvicorn | ASGI server |
| **PDF Processing** | PyPDF | PDF loading & parsing |
| **Text Splitting** | LangChain | Chunk documents into manageable pieces |
| **Embeddings** | Google Generative AI | Convert text to vectors |
| **Vector DB** | Pinecone | Store & retrieve embeddings |
| **LLM** | Groq (Llama 3.3 70B) | Generate intelligent responses |
| **Chain Orchestration** | LangChain | RAG chain management |
| **Logging** | Loguru | Structured logging |
| **Config** | Python-dotenv | Environment variable management |

### Frontend
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Streamlit | Web interface |
| **HTTP Client** | Requests | API communication |

### Deployment
| Component | Platform | Purpose |
|-----------|----------|---------|
| **Backend** | Render Web Service | API hosting |
| **Frontend** | Streamlit Cloud | Web UI hosting |
| **Vectorstore** | Pinecone Serverless | Vector storage |
| **Version Control** | GitHub | Code repository |

---

## 📁 Project Structure

```
MEDICALASSISTANT/
│
├── server/                          # Backend API
│   ├── main.py                      # FastAPI app entry point
│   ├── requirements.txt              # Backend dependencies
│   │
│   ├── modules/
│   │   ├── llm.py                   # LLM chain setup (Groq)
│   │   ├── load_vectorstore.py      # PDF processing & embedding
│   │   ├── pdf_handlers.py          # PDF utilities
│   │   └── query_handlers.py        # Query processing
│   │
│   ├── routes/
│   │   ├── upload_pdfs.py           # /upload_pdfs/ endpoint
│   │   └── ask_question.py          # /ask/ endpoint
│   │
│   ├── middlewares/
│   │   └── exception_handlers.py    # Error handling
│   │
│   ├── uploaded_docs/               # Temporary PDF storage
│   ├── logger.py                    # Logging configuration
│   └── test.py                      # Testing
│
├── client/                          # Frontend UI
│   ├── app.py                       # Streamlit main app
│   ├── config.py                    # API endpoint configuration
│   ├── requirements.txt             # Frontend dependencies
│   │
│   ├── components/
│   │   ├── chatUI.py                # Chat interface
│   │   ├── upload.py                # File upload component
│   │   ├── history_download.py      # Chat history download
│   │   └── settings.py              # Settings panel
│   │
│   └── utils/
│       └── api.py                   # API communication functions
│
├── .env                             # Environment variables (gitignored)
├── .gitignore                       # Git ignore rules
├── main.py                          # Root entry point
├── pyproject.toml                   # Project metadata
└── README.md                        # Documentation
```

---

## 🔧 Core Components Explained

### 1. **Backend - server/main.py**
```python
# FastAPI app initialization
app = FastAPI(title="Medical Assistant API")

# CORS setup - allows frontend to communicate
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Route registration
app.include_router(upload_router)  # /upload_pdfs/
app.include_router(ask_router)      # /ask/
```

**Why it matters:** This is your API server that processes requests from the Streamlit frontend.

---

### 2. **Vector Store Setup - server/modules/load_vectorstore.py**

**Flow:**
```
User uploads PDF
    ↓
PyPDF loads and extracts text
    ↓
RecursiveCharacterTextSplitter chunks text (500 chars, 50 overlap)
    ↓
GoogleGenerativeAIEmbeddings converts chunks to vectors (3072 dimensions)
    ↓
Pinecone stores vectors with metadata
```

**Key Code:**
```python
# 1. Split documents into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# 2. Create embeddings
embeddings = embed_model.embed_documents(texts)

# 3. Store in Pinecone
index.upsert(vectors=vectors)
```

---

### 3. **Question Answering - server/routes/ask_question.py**

**RAG Flow:**
```
User question
    ↓
Embed question using same model (Google Generative AI)
    ↓
Search Pinecone for top-3 similar chunks
    ↓
Build context from retrieved chunks
    ↓
Pass context + question to Groq LLM
    ↓
LLM generates answer
    ↓
Return answer to frontend
```

**Key Code:**
```python
# 1. Embed query
embedded_query = embed_model.embed_query(question)

# 2. Search Pinecone
results = index.query(vector=embedded_query, top_k=3)

# 3. Build retriever with results
retriever = SimpleRetriever(docs=docs)

# 4. Generate answer
chain = get_llm_chain(retriever)
result = query_chain(chain, question)
```

---

### 4. **LLM Setup - server/modules/llm.py**

```python
def get_llm_chain(retriever):
    # Initialize Groq LLM
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile"
    )
    
    # Define prompt template
    prompt = PromptTemplate(
        template="You are MediBot. Answer based on context only..."
    )
    
    # Create RAG chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )
    return chain
```

**Why Groq:** Extremely fast inference (~100 tokens/second) - important for real-time responses.

---

### 5. **Frontend - client/app.py**

Uses Streamlit to create UI with three components:
- **Upload Panel:** Send PDFs to backend
- **Chat Interface:** Ask questions and display answers
- **Settings:** Additional options

**Key Features:**
- Custom CSS styling
- Session state management
- Real-time API communication

---

## 🚀 How It Works (Complete Flow)

### Scenario: User uploads PDF and asks a question

#### Step 1: Upload PDF
```
User clicks "Upload PDF" button
    ↓
Streamlit reads file: components/upload.py
    ↓
Sends POST request to /upload_pdfs/
    POST https://backend-url.onrender.com/upload_pdfs/
    ↓
Backend processes (server/routes/upload_pdfs.py):
  • Receives file
  • Saves temporarily
  • Loads PDF
  • Chunks text
  • Creates embeddings
  • Stores in Pinecone
    ↓
Response: {"message": "Files processed"}
    ↓
Streamlit shows "Upload complete"
```

#### Step 2: Ask Question
```
User types question: "What is the treatment?"
    ↓
Streamlit sends POST request (client/utils/api.py)
    POST https://backend-url.onrender.com/ask/
    with data: {"question": "What is the treatment?"}
    ↓
Backend processes (server/routes/ask_question.py):
  • Embeds question using Google API
  • Searches Pinecone for similar chunks
  • Retrieves top-3 chunks as context
  • Passes to Groq LLM
  • LLM generates answer
    ↓
Response: {"answer": "The treatment is..."}
    ↓
Streamlit displays answer in chat
```

---

## 💻 Setup Instructions

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
Create `.env` file in root:
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
# or
uvicorn main:app --reload
# Runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd client
streamlit run app.py
# Runs on http://localhost:8501
```

**Test Endpoints:**
```bash
# Health check
curl http://localhost:8000/health

# Upload PDF
curl -X POST http://localhost:8000/upload_pdfs/ -F "files=@document.pdf"

# Ask question
curl -X POST http://localhost:8000/ask/ -d "question=What is this?"
```

---

## 🌐 Deployment Guide

### A. Deploy Backend to Render

#### Step 1: Create Render Web Service
1. Go to [render.com](https://render.com/)
2. Click **New +** → **Web Service**
3. Connect GitHub repository
4. Configure:
   - **Name:** medical-assistant-api
   - **Runtime:** Python 3.12
   - **Build Command:** `pip install -r server/requirements.txt`
   - **Start Command:** `cd server && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Standard (paid) or Free

#### Step 2: Add Environment Variables
In Render dashboard → Service → Environment:
```
GOOGLE_API_KEY=your_key
GROQ_API_KEY=your_key
PINECONE_API_KEY=your_key
PINECONE_INDEX_NAME=medicalindex
```

#### Step 3: Deploy
Click **Create Web Service**. Render deploys automatically.

**Note Backend URL:** e.g., `https://medical-assistant-api.onrender.com`

---

### B. Deploy Frontend to Streamlit Cloud

#### Step 1: Prepare Repository
Ensure `.env` is in `.gitignore`:
```bash
git add .gitignore
git commit -m "Ensure .env is ignored"
git push
```

#### Step 2: Connect Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click **New app**
3. Connect GitHub
4. Select repository
5. Set:
   - **Main file path:** `client/app.py`
   - **Python version:** 3.12

#### Step 3: Add Secrets
In Streamlit Cloud → Settings → Secrets:
```toml
API_URL = "https://medical-assistant-api.onrender.com"
```

#### Step 4: Deploy
Click **Deploy**. Streamlit Cloud handles everything.

**Live URL:** e.g., `https://medical-assistant-rag-pipeline.streamlit.app/`

---

## 📡 API Reference

### 1. Upload PDFs
```
POST /upload_pdfs/

Request:
  Files (form data): PDF files

Response:
  {
    "messages": "Files processed and vectorstore updated"
  }

Example:
  curl -X POST http://localhost:8000/upload_pdfs/ \
    -F "files=@document.pdf"
```

### 2. Ask Question
```
POST /ask/

Request:
  Form data: question (string)

Response:
  {
    "answer": "Answer based on documents..."
  }

Example:
  curl -X POST http://localhost:8000/ask/ \
    -d "question=What is the treatment?"
```

### 3. Health Check
```
GET /health

Response:
  {
    "status": "healthy",
    "message": "Medical Assistant API is running"
  }

Example:
  curl http://localhost:8000/health
```

### 4. Root Endpoint
```
GET /

Response:
  {
    "message": "Medical Assistant API",
    "version": "1.0.0"
  }
```

---

## 🔐 Environment Variables

| Variable | Purpose | Where to Set | Required |
|----------|---------|--------------|----------|
| `GOOGLE_API_KEY` | Google Generative AI embeddings | Render/Streamlit Cloud | Yes |
| `GROQ_API_KEY` | Groq LLM API key | Render | Yes |
| `PINECONE_API_KEY` | Pinecone vector database | Render | Yes |
| `PINECONE_INDEX_NAME` | Pinecone index name | Render | Yes |
| `API_URL` | Backend URL for frontend | Streamlit Cloud | Yes |
| `PORT` | Server port (auto by Render) | Auto-set | No |

### Local Development (.env)
```env
GOOGLE_API_KEY=AIza...
GROQ_API_KEY=gsk_...
PINECONE_API_KEY=pcsk_...
PINECONE_INDEX_NAME=medicalindex
API_URL=http://127.0.0.1:8000
```

### Production (Render)
Set in Render dashboard. **DO NOT commit .env to GitHub.**

---

## ✅ Future Projects Checklist

When creating similar RAG/LLM projects, follow this checklist:

### Pre-Development
- [ ] Define your use case (medical, legal, general knowledge, etc.)
- [ ] Choose your vectorstore (Pinecone, Chroma, Weaviate, etc.)
- [ ] Choose your embedding model (Google, OpenAI, local, etc.)
- [ ] Choose your LLM (Groq, OpenAI, Anthropic, local, etc.)
- [ ] Identify your data source (PDFs, docs, web, database, etc.)

### Backend Setup
- [ ] Initialize FastAPI project
- [ ] Add CORS middleware
- [ ] Create requirements.txt with:
  - [ ] Web framework (fastapi, uvicorn)
  - [ ] Document loading library (PyPDF, python-docx, etc.)
  - [ ] Text splitter (langchain_text_splitters)
  - [ ] Embeddings library (langchain-google-genai, etc.)
  - [ ] Vectorstore library (pinecone, chromadb, etc.)
  - [ ] LLM library (langchain-groq, openai, etc.)
  - [ ] Utilities (python-dotenv, pydantic, requests)

### Frontend Setup
- [ ] Choose UI framework (Streamlit, React, Vue, etc.)
- [ ] Create requirements.txt
- [ ] Build API client functions
- [ ] Design UI components

### Environment Variables
- [ ] Create .env template (never commit actual keys)
- [ ] Document all required variables
- [ ] Use os.getenv() for reading variables

### Local Testing
- [ ] Test upload functionality
- [ ] Test query functionality
- [ ] Check error handling
- [ ] Verify logging

### Deployment Setup
- [ ] Choose backend host (Render, Railway, Heroku, AWS, etc.)
- [ ] Choose frontend host (Streamlit Cloud, Vercel, Netlify, etc.)
- [ ] Create deployment configuration
- [ ] Setup environment variables on platform
- [ ] Test deployed version

### Documentation
- [ ] API documentation
- [ ] Setup instructions
- [ ] Troubleshooting guide
- [ ] Deployment guide

### Git & Version Control
- [ ] Initialize git repository
- [ ] Create .gitignore (include .env, venv, __pycache__)
- [ ] Commit initial code
- [ ] Push to GitHub
- [ ] Setup branch protection rules

---

## 🐛 Troubleshooting

### Backend Issues

#### "ModuleNotFoundError: No module named..."
**Cause:** Dependencies not installed
**Solution:**
```bash
cd server
pip install -r requirements.txt
```

#### "GOOGLE_API_KEY not found in .env"
**Cause:** Missing API key in .env
**Solution:**
```bash
# Create .env file with:
GOOGLE_API_KEY=your_actual_key
```

#### "Pinecone index not found"
**Cause:** Index doesn't exist or wrong name
**Solution:**
1. Check `PINECONE_INDEX_NAME` in .env
2. Verify Pinecone dashboard
3. Auto-creates on first upload

#### Port already in use
**Cause:** Another service using port 8000
**Solution:**
```bash
# Use different port
uvicorn server.main:app --port 8001
```

#### CORS errors in frontend
**Cause:** Frontend can't reach backend
**Solution:**
1. Verify `API_URL` in client/config.py
2. Check backend is running
3. CORS is enabled in main.py

---

### Frontend Issues

#### "Failed to connect to API"
**Cause:** Wrong API URL
**Solution:**
```python
# client/config.py
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
# Check this matches your backend URL
```

#### "Upload fails silently"
**Cause:** Backend error not shown
**Solution:**
1. Check server logs: `python server/main.py`
2. Check API endpoint: `/upload_pdfs/`
3. Verify file size

#### Streamlit keeps reloading
**Cause:** File changes trigger reload
**Solution:**
```bash
# Run without auto-reload in production
streamlit run app.py --logger.level=error
```

---

### Deployment Issues

#### Backend deployment fails on Render
**Cause:** Build command error
**Solution:**
1. Check build log in Render dashboard
2. Verify Python version (3.12)
3. Verify `pip install -r server/requirements.txt` works locally

#### Frontend can't reach backend on production
**Cause:** Wrong API URL
**Solution:**
1. Set `API_URL` in Streamlit Cloud Secrets
2. Use full URL: `https://backend.onrender.com`
3. No trailing slash

#### Files lost after restart
**Cause:** Render has ephemeral filesystem
**Solution:**
1. Use Pinecone as primary storage (recommended)
2. Don't rely on uploaded_docs/ folder
3. Consider AWS S3 for file persistence

---

### API Issues

#### "Query returned no results"
**Cause:** No documents uploaded or no match
**Solution:**
1. Upload PDFs first
2. Check Pinecone has vectors
3. Try clearer questions

#### "LLM rate limit exceeded"
**Cause:** Too many requests to Groq
**Solution:**
1. Add rate limiting middleware
2. Implement request queuing
3. Upgrade Groq plan

#### "Embedding dimension mismatch"
**Cause:** Using different embedding models
**Solution:**
- Must use same model for both:
  - Upload: `models/gemini-embedding-001`
  - Query: `models/gemini-embedding-001`

---

## 📊 Key Metrics & Performance

### Typical Performance
- **Upload 10-page PDF:** 15-30 seconds
- **Average query response:** 2-5 seconds
- **Context retrieval:** <500ms
- **LLM generation:** 1-4 seconds

### Scalability
- **Pinecone Free Tier:** 100k vectors
- **Pinecone Pro:** Unlimited vectors
- **Groq:** 100+ req/sec
- **Render Free:** Limited hours/month

---

## 📚 Additional Resources

### Official Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [LangChain Docs](https://python.langchain.com/)
- [Pinecone Docs](https://docs.pinecone.io/)
- [Groq API Docs](https://console.groq.com/docs/text-chat)
- [Google API Docs](https://ai.google.dev/)

### Related Concepts
- **RAG (Retrieval-Augmented Generation):** Combining retrieved documents with LLM
- **Vector Embeddings:** Converting text to high-dimensional vectors
- **Semantic Search:** Finding similar content using embeddings
- **LLM Prompting:** Crafting effective prompts for models

---

## 🎓 Learning Path for Future Projects

1. **Understand RAG Basics**
   - What are embeddings?
   - How does vector search work?
   - What is retrieval-augmented generation?

2. **Learn LangChain**
   - Document loaders
   - Text splitters
   - Retrievers
   - Chains and agents

3. **Explore Different Vectorstores**
   - Pinecone (cloud, serverless)
   - Chroma (open-source, embedded)
   - Weaviate (enterprise)
   - Milvus (self-hosted)

4. **Experiment with LLMs**
   - Groq (fast, free tier)
   - OpenAI (powerful, paid)
   - Anthropic (claude, reliable)
   - Open-source (Llama, Mistral)

5. **Advanced Topics**
   - Multi-modal retrieval (text + images)
   - Hybrid search (keyword + semantic)
   - Re-ranking results
   - Memory & conversation history
   - Agent design with tools

---

## 📝 Notes for Future You

### What Worked Well
✅ Using Groq for fast LLM responses  
✅ Pinecone serverless for easy scaling  
✅ Streamlit for rapid frontend development  
✅ Render for simple backend deployment  
✅ Environment variables for security  

### Potential Improvements
⚠️ Add conversation memory for multi-turn interactions  
⚠️ Implement result re-ranking for better relevance  
⚠️ Add authentication/authorization  
⚠️ Use persistent file storage (S3) instead of ephemeral  
⚠️ Add query caching to reduce API calls  
⚠️ Implement request rate limiting  
⚠️ Add monitoring and analytics  

### Next Features to Consider
- [ ] Multi-language support
- [ ] Conversation history persistence
- [ ] Advanced filters (date range, source)
- [ ] Export answers as PDF
- [ ] User authentication
- [ ] Admin dashboard
- [ ] Advanced analytics
- [ ] Custom system prompts

---

## 🚀 Summary

**What This Project Does:**
- Takes medical PDFs → Extracts text → Creates embeddings → Stores in vector DB → Uses LLM to answer questions

**Tech Stack:**
- Backend: FastAPI + Groq LLM + Pinecone vectors
- Frontend: Streamlit
- Deployment: Render + Streamlit Cloud

**Key Learnings:**
1. Environment variables keep secrets safe (set on platform, not in code)
2. RAG pipelines combine retrieval with generation for accurate answers
3. Embeddings enable semantic search
4. Vectorstores make similarity search fast and scalable
5. LLMs generate human-like responses

**For Next Projects:**
1. Follow the checklist provided
2. Start with this structure as template
3. Adapt to your specific use case
4. Keep environment variables separate
5. Document your architecture
6. Plan deployment from start

---

**Created:** May 2026  
**Project:** MediBot - Medical Assistant RAG Pipeline  
**Status:** ✅ Live on Render + Streamlit Cloud  
**Next Maintainer:** [Pranav Kashyap]

