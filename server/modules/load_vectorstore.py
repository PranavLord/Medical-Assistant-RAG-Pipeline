import os
import time
from pathlib import Path

from dotenv import load_dotenv
from tqdm.auto import tqdm

from pinecone import Pinecone, ServerlessSpec

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# ENV VARIABLES
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = "medicalindex"

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# CHECK API KEYS
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found in .env")

# INITIALIZE PINECONE
pc = Pinecone(api_key=PINECONE_API_KEY)

spec = ServerlessSpec(
    cloud="aws",
    region=PINECONE_ENV
)

# CURRENT SDK STYLE
existing_indexes = pc.list_indexes().names()

# text-embedding-004 returns 3072 dimensions
EMBEDDING_DIMENSION = 3072

# CREATE INDEX IF NOT EXISTS
if PINECONE_INDEX_NAME not in existing_indexes:

    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=EMBEDDING_DIMENSION,
        metric="cosine",
        spec=spec
    )

    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

# CONNECT TO INDEX
index = pc.Index(PINECONE_INDEX_NAME)


def load_vectorstore(uploaded_files):

    # IMPORTANT:
    # Use model WITHOUT "models/"
    embed_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY
    )

    file_paths = []

    # SAVE FILES
    for file in uploaded_files:

        save_path = Path(UPLOAD_DIR) / file.filename

        with open(save_path, "wb") as f:
            f.write(file.file.read())

        file_paths.append(str(save_path))

    # PROCESS FILES
    for file_path in file_paths:

        print(f"\n📄 Processing: {file_path}")

        # LOAD PDF
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # SPLIT TEXT
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(documents)

        if not chunks:
            print("⚠️ No chunks found")
            continue

        texts = [chunk.page_content for chunk in chunks]

        metadatas = []

        for chunk in chunks:
            metadata = chunk.metadata

            # Ensure metadata is JSON serializable
            cleaned_metadata = {
                k: str(v) for k, v in metadata.items()
            }

            metadatas.append(cleaned_metadata)

        ids = [
            f"{Path(file_path).stem}-{i}"
            for i in range(len(chunks))
        ]

        print(f"🔍 Creating embeddings for {len(texts)} chunks...")

        # EMBEDDINGS
        embeddings = embed_model.embed_documents(texts)

        print("📤 Uploading vectors to Pinecone...")

        vectors = []

        for i in range(len(ids)):
            vectors.append({
                "id": ids[i],
                "values": embeddings[i],
                "metadata": metadatas[i]
            })

        # UPSERT
        with tqdm(total=len(vectors), desc="Uploading") as progress:

            index.upsert(vectors=vectors)

            progress.update(len(vectors))

        print(f"✅ Upload complete: {file_path}")