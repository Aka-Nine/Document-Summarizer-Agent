"""
Enterprise Document Intelligence Processor with RAG
Production-ready document processing with retrieval augmented generation
"""
import time
from typing import List, Dict, Any, Optional
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
# LangChain chains - using direct LLM calls instead
# from langchain.chains.summarize import load_summarize_chain
# from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain_core.documents import Document as LangchainDocument
from langchain_core.prompts import PromptTemplate
import structlog

from app.config.settings import settings
from app.core.rag_processor import RAGProcessor

logger = structlog.get_logger()


class EnterpriseDocumentProcessor:
    """Enterprise-grade document processor with RAG capabilities"""
    
    def __init__(self, document_id: Optional[str] = None):
        self.document_id = document_id
        self.llm = self._create_llm()
        self.rag_processor = RAGProcessor() if settings.RAG_ENABLED else None
        self.qa_prompt = self._create_qa_prompt()
    
    def _create_llm(self):
        """Create LLM based on configuration"""
        provider = settings.LLM_PROVIDER.lower()
        
        if provider == "groq":
            if not settings.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is required")
            return ChatGroq(
                api_key=settings.GROQ_API_KEY,
                model=settings.GROQ_MODEL,
                temperature=0.0,
                max_retries=3
            )
        elif provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required")
            return ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model=settings.OPENAI_LLM_MODEL,
                temperature=settings.OPENAI_TEMPERATURE,
                max_retries=3
            )
        elif provider == "anthropic":
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY is required")
            return ChatAnthropic(
                api_key=settings.ANTHROPIC_API_KEY,
                model=settings.ANTHROPIC_MODEL,
                temperature=0.0,
                max_retries=3
            )
        elif provider == "gemini":
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY is required")
            return ChatGoogleGenerativeAI(
                google_api_key=settings.GEMINI_API_KEY,
                model=settings.GEMINI_MODEL,
                temperature=0.0,
                max_retries=3
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    def _create_qa_prompt(self) -> PromptTemplate:
        """Create QA prompt template"""
        template = """You are an expert document analyst. Answer the question based on the provided context.

Context:
{context}

Question: {question}

Answer the question accurately and concisely. If the answer cannot be found in the context, say "I don't have enough information to answer this question."

Answer:"""
        return PromptTemplate(
            input_variables=["context", "question"],
            template=template
        )
    
    def load_document(self, file_path: str) -> List[LangchainDocument]:
        """Load document from file path"""
        try:
            file_ext = file_path.lower().split('.')[-1]
            
            if file_ext == "pdf":
                loader = PyPDFLoader(file_path)
            elif file_ext == "txt":
                loader = TextLoader(file_path)
            elif file_ext in ["docx", "doc"]:
                loader = Docx2txtLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
            
            documents = loader.load()
            logger.info(
                "Document loaded",
                file_path=file_path,
                pages=len(documents),
                document_id=self.document_id
            )
            return documents
        except Exception as e:
            logger.error("Failed to load document", error=str(e), file_path=file_path)
            raise
    
    async def process_document(
        self,
        file_path: str,
        questions: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process document with RAG-enabled intelligence
        
        Args:
            file_path: Path to document file
            questions: Optional list of questions to answer
            metadata: Additional metadata
        
        Returns:
            Processing results with summary, Q&A, and RAG context
        """
        start_time = time.time()
        metadata = metadata or {}
        
        try:
            # Load document
            documents = self.load_document(file_path)
            if not documents:
                raise ValueError("No content extracted from document")
            
            # Chunk document for RAG
            chunks = self.rag_processor.chunk_document(documents) if self.rag_processor else []
            
            # Index in vector database if RAG enabled
            chunks_indexed = 0
            if self.rag_processor and self.document_id:
                chunks_indexed = await self.rag_processor.index_document(
                    document_id=self.document_id,
                    chunks=chunks,
                    metadata={
                        "filename": metadata.get("filename", "unknown"),
                        **metadata
                    }
                )
            
            # Generate summary
            summary = await self._generate_summary(documents)
            
            # Answer questions with RAG
            answers = {}
            if questions:
                answers = await self._answer_questions_with_rag(questions, chunks)
            else:
                # Use default questions
                default_questions = [
                    "What is the main topic or theme of this document?",
                    "What are the key points or arguments presented?",
                    "What are the main conclusions or recommendations?",
                    "Are there any important facts, figures, or statistics mentioned?"
                ]
                answers = await self._answer_questions_with_rag(default_questions, chunks)
            
            processing_time = time.time() - start_time
            
            result = {
                "summary": summary,
                "answers": answers,
                "metadata": {
                    "processing_time": processing_time,
                    "chunks_indexed": chunks_indexed,
                    "total_pages": len(documents),
                    "total_chunks": len(chunks),
                    "rag_enabled": settings.RAG_ENABLED,
                    **metadata
                }
            }
            
            logger.info(
                "Document processing completed",
                document_id=self.document_id,
                processing_time=processing_time,
                chunks_indexed=chunks_indexed
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "Document processing failed",
                error=str(e),
                document_id=self.document_id,
                file_path=file_path
            )
            raise
    
    async def _generate_summary(self, documents: List[LangchainDocument]) -> str:
        """Generate document summary using LLM directly"""
        try:
            # Combine all document content
            full_text = "\n\n".join([doc.page_content for doc in documents])
            
            # Create summary prompt
            summary_prompt = f"""Please provide a comprehensive summary of the following document:

{document}

Summary:"""
            
            # Generate summary using LLM
            from langchain_core.messages import HumanMessage
            messages = [HumanMessage(content=summary_prompt)]
            response = await self.llm.ainvoke(messages)
            
            summary = response.content if hasattr(response, 'content') else str(response)
            logger.info("Summary generated", length=len(summary))
            return summary
        except Exception as e:
            logger.error("Summary generation failed", error=str(e))
            raise
    
    async def _answer_questions_with_rag(
        self,
        questions: List[str],
        chunks: List[LangchainDocument]
    ) -> Dict[str, str]:
        """Answer questions using RAG if enabled, otherwise use summary"""
        answers = {}
        
        for question in questions:
            try:
                if self.rag_processor and self.document_id:
                    # Use RAG retrieval
                    context_results = await self.rag_processor.retrieve_context(
                        query=question,
                        document_id=self.document_id,
                        top_k=settings.TOP_K_RETRIEVAL
                    )
                    
                    if context_results:
                        # Build context from retrieved chunks
                        context_text = "\n\n".join([
                            result["metadata"].get("text", "")
                            for result in context_results
                        ])
                        
                        # Use QA chain with retrieved context
                        qa_chain = load_qa_chain(
                            self.llm,
                            chain_type="stuff",
                            prompt=self.qa_prompt
                        )
                        context_doc = LangchainDocument(page_content=context_text)
                        answer = qa_chain.run(
                            input_documents=[context_doc],
                            question=question
                        )
                    else:
                        # Fallback to summary if no context found
                        answer = await self._answer_from_summary(question, chunks)
                else:
                    # Use summary-based QA
                    answer = await self._answer_from_summary(question, chunks)
                
                answers[question] = answer
                logger.info("Question answered", question=question[:50])
                
            except Exception as e:
                logger.error("Failed to answer question", question=question, error=str(e))
                answers[question] = f"Error processing question: {str(e)}"
        
        return answers
    
    async def _answer_from_summary(
        self,
        question: str,
        chunks: List[LangchainDocument]
    ) -> str:
        """Answer question from document chunks/summary"""
        try:
            # Combine chunks for context
            context_text = "\n\n".join([chunk.page_content for chunk in chunks])
            
            # Use LLM directly with prompt
            prompt_text = self.qa_prompt.format(context=context_text, question=question)
            from langchain_core.messages import HumanMessage
            messages = [HumanMessage(content=prompt_text)]
            response = await self.llm.ainvoke(messages)
            answer = response.content if hasattr(response, 'content') else str(response)
            return answer
        except Exception as e:
            logger.error("Summary-based QA failed", error=str(e))
            raise
    
    async def query_document(
        self,
        query: str,
        document_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Query a specific document using RAG
        
        Args:
            query: Query string
            document_id: Document ID to query
        
        Returns:
            Query results with answer and context
        """
        if not self.rag_processor:
            raise ValueError("RAG is not enabled")
        
        doc_id = document_id or self.document_id
        if not doc_id:
            raise ValueError("Document ID is required")
        
        try:
            # Retrieve relevant context
            context_results = await self.rag_processor.retrieve_context(
                query=query,
                document_id=doc_id,
                top_k=settings.TOP_K_RETRIEVAL
            )
            
            if not context_results:
                return {
                    "answer": "No relevant context found for this query.",
                    "context": [],
                    "sources": []
                }
            
            # Build context for LLM
            context_text = "\n\n".join([
                result["metadata"].get("text", "")
                for result in context_results
            ])
            
            # Generate answer using LLM directly
            prompt_text = self.qa_prompt.format(context=context_text, question=query)
            from langchain_core.messages import HumanMessage
            messages = [HumanMessage(content=prompt_text)]
            response = await self.llm.ainvoke(messages)
            answer = response.content if hasattr(response, 'content') else str(response)
            
            return {
                "answer": answer,
                "context": context_results,
                "sources": [
                    {
                        "chunk_id": r["id"],
                        "score": r["score"],
                        "text": r["metadata"].get("text", "")[:200]
                    }
                    for r in context_results
                ]
            }
            
        except Exception as e:
            logger.error("Document query failed", error=str(e), query=query, document_id=doc_id)
            raise

