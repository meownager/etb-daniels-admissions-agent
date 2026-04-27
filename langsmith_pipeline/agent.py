"""
agent.py
--------
The LangChain RAG agent. This is the "brain" of the observability pipeline.

Pipeline:
  user query -> retrieve top-3 KB chunks -> Claude Haiku w/ system prompt -> response

Every step gets traced automatically by LangSmith because LANGSMITH_TRACING=true
in your .env file.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

CHROMA_DIR = Path(__file__).parent / "chroma_db"
SYSTEM_PROMPT_PATH = Path(__file__).parent.parent / "system_prompt.txt"


def load_system_prompt() -> str:
    """Read the agent's system prompt from disk."""
    if not SYSTEM_PROMPT_PATH.exists():
        raise FileNotFoundError(
            f"System prompt not found at {SYSTEM_PROMPT_PATH}. "
            f"Copy SYSTEM_PROMPT.txt from your project folder to "
            f"the project root as 'system_prompt.txt'."
        )
    with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def format_docs(docs) -> str:
    """Format retrieved chunks into a labeled string for the LLM."""
    return "\n\n---\n\n".join(
        f"[Source: {d.metadata.get('source', 'unknown')}]\n{d.page_content}"
        for d in docs
    )


def build_agent():
    """Build and return the runnable RAG chain."""

    # 1. Vector store retriever (uses the Chroma DB built by ingest.py)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 2. The LLM — Claude Haiku 4.5 (matches Voiceflow config: low temp, capped tokens)
    llm = ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        temperature=0.3,
        max_tokens=400,
    )

    # 3. Prompt template — system prompt + retrieved KB context + user question
    system_prompt = load_system_prompt()
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            system_prompt
            + "\n\n--- RETRIEVED KB CHUNKS (use these to answer) ---\n{context}",
        ),
        ("human", "{question}"),
    ])

    # 4. Wire it all together as a LangChain Runnable
    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


def query(question: str) -> str:
    """Convenience helper: build and invoke the agent in one call."""
    chain = build_agent()
    return chain.invoke(question)


# Quick sanity check — run this file directly to test a single query
if __name__ == "__main__":
    test_q = "I'm thinking about going back to school."
    print(f"Q: {test_q}\n")
    print(f"A: {query(test_q)}")
