from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
from typing import List
from knowledge_manager import KnowledgeManager

router = APIRouter()
knowledge_manager = KnowledgeManager(
    db_path="/app/data/knowledge.db",
    knowledge_dir="/app/data/knowledge_files"
)

@router.post("/upload")
async def upload_knowledge(file: UploadFile = File(...)):
    """지식 YAML 파일 업로드"""
    if not file.filename.endswith('.yaml'):
        raise HTTPException(status_code=400, detail="Only YAML files are allowed")
    
    file_path = os.path.join(knowledge_manager.knowledge_dir, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        knowledge_manager.add_knowledge(file.filename)
        return {"message": "File uploaded successfully"}
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/files")
async def list_files() -> List[dict]:
    """업로드된 지식 파일 목록 조회"""
    return knowledge_manager.list_knowledge_files()

@router.get("/download/{filename}")
async def download_file(filename: str):
    """지식 파일 다운로드"""
    file_path = os.path.join(knowledge_manager.knowledge_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)

@router.delete("/files/{filename}")
async def delete_file(filename: str):
    """지식 파일 삭제"""
    try:
        knowledge_manager.remove_knowledge(filename)
        return {"message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/rebuild")
async def rebuild_database():
    """데이터베이스 재구축"""
    try:
        knowledge_manager.rebuild_database()
        return {"message": "Database rebuilt successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
