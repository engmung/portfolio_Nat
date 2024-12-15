import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sqlite3
import json
import asyncio
from knowledge_manager import (
    get_all_knowledge_files,
    load_yaml_file,
    save_yaml_file,
    get_knowledge_file,
    delete_knowledge_file,
    rebuild_database
)
from openai import AsyncOpenAI
from database import get_db

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Configure OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not found in environment variables")

client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.openai.com/v1"
)

async def get_embedding(text: str) -> list[float]:
    """Get embedding for text using OpenAI's API."""
    try:
        response = await client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return []

async def get_ai_summary(content: str) -> str:
    """Generate an AI summary of the content using RAG with GPT-4o-mini."""
    if not OPENAI_API_KEY:
        return "AI 요약을 위해서는 .env 파일에 OPENAI_API_KEY를 설정해주세요."
        
    try:
        # Get embedding for the current content
        content_embedding = await get_embedding(content)
        
        # Get related knowledge from database using embedding similarity
        knowledge_content = get_knowledge_content()
        
        # Generate summary using GPT-4o-mini with retrieved context
        prompt = f"""관련 지식:
{knowledge_content}

현재 내용:
{content}

위 내용을 분석하고 한 문장으로 핵심을 요약해주세요. 기술적인 측면과 주요 학습 포인트에 초점을 맞춰주세요."""

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 기술 문서를 이해하고 핵심을 정확하게 요약하는 AI 어시스턴트입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI 요약 생성 중 오류 발생: {e}")
        return "현재 AI 요약을 생성할 수 없습니다. 나중에 다시 시도해주세요."

def get_knowledge_content():
    """지식 데이터베이스의 모든 내용을 가져옴"""
    return get_all_knowledge_files()

def calculate_relevance_scores(query: str, documents: list) -> list:
    """Calculate relevance scores between query and documents using TF-IDF."""
    if not documents:
        return []
    
    # Prepare documents for TF-IDF
    doc_texts = [query] + [f"{doc['title']} {' '.join(doc['tags'])} {doc['content']}" for doc in documents]
    
    # Calculate TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(doc_texts)
    
    # Calculate cosine similarity between query and each document
    query_vector = tfidf_matrix[0:1]
    similarities = cosine_similarity(query_vector, tfidf_matrix[1:]).flatten()
    
    # Sort documents by similarity score
    scored_docs = list(zip(documents, similarities))
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    
    return scored_docs

def find_related_knowledge(knowledge_item, all_knowledge: list) -> list:
    """Find related knowledge items based on content similarity."""
    if not all_knowledge:
        return []
    
    # Create query from the knowledge item
    query_text = f"{knowledge_item.title} {' '.join(knowledge_item.tags)} {knowledge_item.content}"
    
    # Filter out the current knowledge item
    other_knowledge = [k for k in all_knowledge if k.id != knowledge_item.id]
    
    # Calculate relevance scores
    scored_docs = calculate_relevance_scores(query_text, other_knowledge)
    
    # Return top related items (with score > threshold)
    threshold = 0.1
    related_items = [doc for doc, score in scored_docs if score > threshold]
    
    return related_items[:5]  # Return top 5 related items

async def query_knowledge(query: str) -> str:
    """Query the knowledge base using OpenAI's API"""
    try:
        # Get all knowledge from database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT title, content FROM knowledge")
        rows = cursor.fetchall()
        
        # Prepare context from knowledge base
        context = "\n\n".join([f"# {title}\n{content}" for title, content in rows])
        
        # Prepare the prompt
        prompt = f"""다음은 우리의 지식 베이스 내용입니다:

{context}

사용자 질문: {query}

위의 지식 베이스 내용을 바탕으로 자세한 답변을 제공해주세요.
지식 베이스에 관련 정보가 없다면 그렇다고 말씀해 주세요.
답변은 반드시 한국어로 작성해주세요.
"""

        # Call OpenAI API
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 한국어로 답변하는 친절한 지식 도우미입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error in query_knowledge: {e}")
        return f"Error processing your query: {str(e)}"
