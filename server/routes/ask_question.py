from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse

from modules.llm import get_llm_chain
from modules.query_handlers import query_chain

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from pinecone import Pinecone

from pydantic import Field
from typing import List, Optional

from logger import logger

import os


router = APIRouter()


@router.post("/ask/")
async def ask_question(question: str = Form(...)):

    try:

        logger.info(f"User query: {question}")

        # -----------------------------
        # Pinecone Setup
        # -----------------------------
        pc = Pinecone(
            api_key=os.environ["PINECONE_API_KEY"]
        )

        index = pc.Index(
            os.environ["PINECONE_INDEX_NAME"]
        )

        # -----------------------------
        # Embedding Model
        # MUST MATCH UPLOAD MODEL
        # -----------------------------
        embed_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=os.environ["GOOGLE_API_KEY"]
        )

        # -----------------------------
        # Embed User Query
        # -----------------------------
        embedded_query = embed_model.embed_query(question)

        # -----------------------------
        # Search Pinecone
        # -----------------------------
        res = index.query(
            vector=embedded_query,
            top_k=3,
            include_metadata=True
        )

        # -----------------------------
        # Convert Matches -> Documents
        # -----------------------------
        docs = []

        for match in res["matches"]:

            metadata = match.get("metadata", {})

            page_content = metadata.get("text", "")

            doc = Document(
                page_content=page_content,
                metadata=metadata
            )

            docs.append(doc)

        # -----------------------------
        # Custom Retriever
        # -----------------------------
        class SimpleRetriever(BaseRetriever):

            docs: List[Document] = Field(default_factory=list)

            tags: Optional[List[str]] = Field(default_factory=list)

            metadata: Optional[dict] = Field(default_factory=dict)

            def _get_relevant_documents(
                self,
                query: str
            ) -> List[Document]:

                return self.docs

        retriever = SimpleRetriever(
            docs=docs
        )

        # -----------------------------
        # LLM Chain
        # -----------------------------
        chain = get_llm_chain(retriever)

        result = query_chain(
            chain,
            question
        )

        logger.info("Query successful")

        return {
            "answer": result
        }

    except Exception as e:

        logger.exception("Error processing question")

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )