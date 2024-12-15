from fastapi import FastAPI, Depends, HTTPException, Body, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import sqlite3
import json
import logging
from pathlib import Path
import yaml

from database import get_db
from knowledge_manager import (
    get_all_knowledge_files,
    save_knowledge_file,
    get_knowledge_file,
    delete_knowledge_file,
    rebuild_database
)
from ai_service import query_knowledge

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 설정
app.mount("/data", StaticFiles(directory="data"), name="data")

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 지식 파일 관리 API
@app.post("/knowledge/upload")
async def upload_knowledge_file(file: UploadFile):
    try:
        if not file.filename.endswith('.yaml'):
            raise HTTPException(status_code=400, detail="Only YAML files are allowed")
        
        content = await file.read()
        save_knowledge_file(file.filename, content)
        return {"message": "File uploaded successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge/files")
async def list_knowledge_files():
    try:
        files = get_all_knowledge_files()
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge/download/{filename}")
async def download_knowledge_file(filename: str):
    try:
        content = get_knowledge_file(filename)
        return Response(
            content=content,
            media_type="application/x-yaml",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/knowledge/files/{filename}")
async def delete_knowledge_file_endpoint(filename: str):
    try:
        delete_knowledge_file(filename)
        return {"message": "File deleted successfully"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/knowledge/rebuild")
async def rebuild_knowledge_database():
    try:
        rebuild_database()
        return {"message": "Database rebuilt successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI 검색 API
@app.post("/ai/query")
async def query_ai(query: dict = Body(...)):
    try:
        response = await query_knowledge(query["query"])
        return {"response": response}
    except Exception as e:
        logger.error(f"Error querying AI: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/knowledge")
async def create_knowledge(knowledge: dict = Body(...), db: sqlite3.Connection = Depends(get_db)):
    try:
        logger.info(f"Creating knowledge: {knowledge}")
        cursor = db.cursor()
        
        # Validate required fields
        required_fields = ['title', 'level', 'tags']
        for field in required_fields:
            if field not in knowledge:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Ensure content and summary are initialized
        content = knowledge.get('content', '')
        summary = knowledge.get('summary', {})
            
        cursor.execute("""
            INSERT INTO knowledge (title, level, tags, content, summary)
            VALUES (?, ?, ?, ?, ?)
        """, (
            knowledge['title'],
            knowledge['level'],
            json.dumps(knowledge['tags']),
            content,
            json.dumps(summary)
        ))
        db.commit()
        
        # Get the ID of the newly created knowledge
        new_id = cursor.lastrowid
        logger.info(f"Knowledge created successfully with ID: {new_id}")
        
        return {
            "message": "Knowledge created successfully",
            "id": new_id
        }
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error creating knowledge: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/knowledge")
async def get_all_knowledge(db: sqlite3.Connection = Depends(get_db)):
    try:
        logger.info("Getting all knowledge")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM knowledge")
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            try:
                # Parse tags from JSON string
                tags = json.loads(row[3]) if isinstance(row[3], str) else row[3]
                if not isinstance(tags, list):
                    tags = []
                    
                # Parse summary if exists
                summary = None
                if row[5]:
                    try:
                        summary = json.loads(row[5]) if isinstance(row[5], str) else row[5]
                    except json.JSONDecodeError:
                        summary = {}
                else:
                    summary = {}
                
                knowledge = {
                    "id": row[0],
                    "title": row[1],
                    "level": row[2],
                    "tags": tags,
                    "content": row[4],
                    "summary": summary
                }
                result.append(knowledge)
                logger.info(f"Processed knowledge item: {knowledge['id']} with tags: {tags}")
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error for row {row}: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"Error processing row {row}: {str(e)}")
                continue
            
        logger.info(f"Retrieved {len(result)} knowledge items")
        return {"items": result}
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error getting knowledge: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/knowledge/{knowledge_id}")
async def get_knowledge(knowledge_id: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        logger.info(f"Getting knowledge with ID: {knowledge_id}")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM knowledge WHERE id = ?", (knowledge_id,))
        row = cursor.fetchone()
        
        if not row:
            logger.error(f"Knowledge not found with ID: {knowledge_id}")
            raise HTTPException(status_code=404, detail="Knowledge not found")
            
        knowledge = {
            "id": row[0],
            "title": row[1],
            "level": row[2],
            "tags": json.loads(row[3]),
            "content": row[4],
            "summary": json.loads(row[5]) if row[5] else {}
        }
        logger.info(f"Retrieved knowledge with ID: {knowledge_id}")
        return knowledge
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error getting knowledge: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/knowledge/{knowledge_id}")
async def delete_knowledge(knowledge_id: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        logger.info(f"Deleting knowledge with ID: {knowledge_id}")
        cursor = db.cursor()
        cursor.execute("SELECT id FROM knowledge WHERE id = ?", (knowledge_id,))
        if not cursor.fetchone():
            logger.error(f"Knowledge not found with ID: {knowledge_id}")
            raise HTTPException(status_code=404, detail="Knowledge not found")
            
        cursor.execute("DELETE FROM knowledge WHERE id = ?", (knowledge_id,))
        db.commit()
        logger.info(f"Knowledge deleted successfully with ID: {knowledge_id}")
        return {"message": "Knowledge deleted successfully"}
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error deleting knowledge: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/knowledge/{knowledge_id}")
async def update_knowledge(knowledge_id: int, knowledge: dict = Body(...), db: sqlite3.Connection = Depends(get_db)):
    try:
        logger.info(f"Updating knowledge {knowledge_id}: {knowledge}")
        cursor = db.cursor()
        
        # Check if knowledge exists
        cursor.execute("SELECT * FROM knowledge WHERE id = ?", (knowledge_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Knowledge not found")
        
        # Validate required fields
        required_fields = ['title', 'level', 'tags']
        for field in required_fields:
            if field not in knowledge:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Ensure content and summary are initialized
        content = knowledge.get('content', '')
        summary = knowledge.get('summary', {})
            
        cursor.execute("""
            UPDATE knowledge 
            SET title = ?, level = ?, tags = ?, content = ?, summary = ?
            WHERE id = ?
        """, (
            knowledge['title'],
            knowledge['level'],
            json.dumps(knowledge['tags']),
            content,
            json.dumps(summary),
            knowledge_id
        ))
        db.commit()
        
        return {"message": "Knowledge updated successfully"}
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error updating knowledge: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/knowledge/{knowledge_id}/related")
async def get_related_knowledge(knowledge_id: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        logger.info(f"Getting related knowledge for ID: {knowledge_id}")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM knowledge WHERE id = ?", (knowledge_id,))
        row = cursor.fetchone()
        
        if not row:
            logger.error(f"Knowledge not found with ID: {knowledge_id}")
            raise HTTPException(status_code=404, detail="Knowledge not found")
        
        knowledge = {
            "id": row[0],
            "title": row[1],
            "level": row[2],
            "tags": json.loads(row[3]),
            "content": row[4],
            "summary": json.loads(row[5]) if row[5] else {}
        }
        
        cursor.execute("SELECT * FROM knowledge")
        rows = cursor.fetchall()
        all_knowledge = []
        for row in rows:
            k = {
                "id": row[0],
                "title": row[1],
                "level": row[2],
                "tags": json.loads(row[3]),
                "content": row[4],
                "summary": json.loads(row[5]) if row[5] else {}
            }
            all_knowledge.append(k)
        
        related_items = find_related_knowledge(knowledge, all_knowledge)
        logger.info(f"Retrieved related knowledge for ID: {knowledge_id}")
        return related_items
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error getting related knowledge: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search")
async def search_knowledge(query: dict = Body(...), db: sqlite3.Connection = Depends(get_db)):
    try:
        logger.info(f"Searching knowledge with query: {query}")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM knowledge")
        rows = cursor.fetchall()
        
        all_knowledge = []
        for row in rows:
            knowledge = {
                "id": row[0],
                "title": row[1],
                "level": row[2],
                "tags": json.loads(row[3]),
                "content": row[4],
                "summary": json.loads(row[5]) if row[5] else {}
            }
            all_knowledge.append(knowledge)
        
        scored_results = calculate_relevance_scores(query['query'], all_knowledge)
        
        search_results = []
        for knowledge, score in scored_results[:10]:  
            result = {
                "knowledge": knowledge,
                "relevance_score": float(score),
                "ai_summary": await get_ai_summary(f"{knowledge['title']}\n{knowledge['content']}")
            }
            search_results.append(result)
        
        logger.info(f"Retrieved search results for query: {query}")
        return search_results
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error searching knowledge: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/knowledge/for-graph")
async def get_knowledge_for_graph(db: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT id, title, level, tags, content, summary, references
            FROM knowledge
        """)
        rows = cursor.fetchall()
        
        items = []
        for row in rows:
            items.append({
                "id": row[0],
                "title": row[1],
                "level": row[2],
                "tags": json.loads(row[3]) if row[3] else [],
                "content": row[4],
                "summary": row[5],
                "references": json.loads(row[6]) if row[6] else []
            })
        
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge/template")
async def get_template():
    """Get the template file content"""
    template_path = Path(__file__).parent / "data" / "template.yaml"
    if not template_path.exists():
        raise HTTPException(status_code=404, detail="Template file not found")
    
    with open(template_path, 'rb') as f:
        content = f.read()
    
    return Response(
        content=content,
        media_type="application/x-yaml",
        headers={
            "Content-Disposition": f"attachment; filename=template.yaml"
        }
    )
