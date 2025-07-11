# core/document_processor.py
import asyncio
import time
from typing import List, Dict, Any, TypedDict

from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document as LangchainDocument
from langgraph.graph import StateGraph, END

import structlog

logger = structlog.get_logger()

class DocumentProcessorState(TypedDict):
    docs: List[LangchainDocument]
    summary: str
    answers: Dict[str, str]
    metadata: Dict[str, Any]

class DocumentProcessor:
    def __init__(self, api_key: str, model: str = "llama3-8b-8192"):
        self.llm = ChatGroq(
            api_key=api_key,
            model=model,
            max_retries=0  # Prevent infinite retries on 429 errors
        )
        self.graph = self._build_processing_graph()

    def _build_processing_graph(self) -> StateGraph:
        builder = StateGraph(DocumentProcessorState)
        builder.add_node("load", self._load_document)
        builder.add_node("chunk", self._chunk_document)
        builder.add_node("summarize", self._summarize_document)
        builder.add_node("qa", self._qa_from_summary)
        builder.set_entry_point("load")
        builder.add_edge("load", "chunk")
        builder.add_edge("chunk", "summarize")
        builder.add_edge("summarize", "qa")
        builder.add_edge("qa", END)
        return builder.compile()

    def _load_document(self, state: DocumentProcessorState) -> Dict[str, Any]:
        file_path = state.get("metadata", {}).get("file_path")
        if not file_path:
            raise ValueError("File path not provided")

        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")

        docs = loader.load()
        logger.info("Document loaded", file_path=file_path, num_pages=len(docs))
        return {"docs": docs, "metadata": state.get("metadata", {})}

    def _chunk_document(self, state: DocumentProcessorState) -> Dict[str, Any]:
        docs = state["docs"]
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )
        chunked_docs = splitter.split_documents(docs)
        logger.info("Document chunked", num_chunks=len(chunked_docs))
        return {"docs": chunked_docs, "metadata": state.get("metadata", {})}

    def _summarize_document(self, state: DocumentProcessorState) -> Dict[str, Any]:
        docs = state["docs"]
        chain_type = "map_reduce" if len(docs) > 10 else "stuff"
        summarize_chain = load_summarize_chain(self.llm, chain_type=chain_type, verbose=False)
        summary = summarize_chain.run(docs)
        logger.info("Document summarized", summary_length=len(summary))
        return {"summary": summary, "metadata": state.get("metadata", {})}

    def _qa_from_summary(self, state: DocumentProcessorState) -> Dict[str, Any]:
        summary = state["summary"]
        default_questions = [
            "What is the main topic or theme of this document?",
            "What are the key points or arguments presented?",
            "What are the main conclusions or recommendations?",
            "Are there any important facts, figures, or statistics mentioned?"
        ]
        custom_questions = state.get("metadata", {}).get("questions", [])
        all_questions = custom_questions if custom_questions else default_questions

        qa_chain = load_qa_chain(self.llm, chain_type="stuff")
        summary_doc = LangchainDocument(page_content=summary)

        answers = {}
        for question in all_questions:
            try:
                answer = qa_chain.run(input_documents=[summary_doc], question=question)
                answers[question] = answer
                logger.info("QA answer generated", question=question)
            except Exception as e:
                logger.error("QA failed", question=question, error=str(e))
                answers[question] = f"Error processing question: {str(e)}"

        logger.info("QA completed", num_questions=len(answers))
        return {"summary": summary, "answers": answers, "metadata": state.get("metadata", {})}

    def process_document(self, file_path: str, questions: List[str] = None) -> Dict[str, Any]:
        start_time = time.time()
        initial_state = {
            "metadata": {
                "file_path": file_path,
                "questions": questions or [],
                "start_time": start_time
            }
        }
        try:
            result = self.graph.invoke(initial_state)
            result["metadata"]["processing_time"] = time.time() - start_time
            logger.info("Document processing completed", file_path=file_path)
            return result
        except Exception as e:
            logger.error("Synchronous document processing failed", file_path=file_path, error=str(e))
            raise
