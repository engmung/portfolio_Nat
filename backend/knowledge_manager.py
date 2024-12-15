import os
import yaml
import json
from pathlib import Path
from typing import List, Dict, Any
from database import get_db, init_db

KNOWLEDGE_FILES_DIR = Path(__file__).parent / "data" / "knowledge_files"

def ensure_knowledge_dir():
    """Ensure the knowledge files directory exists"""
    KNOWLEDGE_FILES_DIR.mkdir(parents=True, exist_ok=True)

def load_yaml_file(file_path: Path) -> Dict[str, Any]:
    """Load a YAML file and return its contents"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_yaml_file(file_path: Path, data: Dict[str, Any]):
    """Save data to a YAML file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)

def get_all_knowledge_files() -> List[Dict[str, Any]]:
    """Get all knowledge files and their metadata"""
    ensure_knowledge_dir()
    files = []
    for file_path in KNOWLEDGE_FILES_DIR.glob("*.yaml"):
        try:
            data = load_yaml_file(file_path)
            if isinstance(data, dict):  # 유효한 YAML 파일인지 확인
                files.append({
                    'filename': file_path.name,
                    'title': data.get('title', ''),
                    'level': data.get('level', 1),
                    'tags': data.get('tags', []),
                    'summary': data.get('summary', ''),
                    'content': data.get('content', ''),
                    'references': data.get('references', [])
                })
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    return files

def validate_knowledge_content(data):
    """Validate the knowledge file content against the template"""
    required_fields = ['title', 'level', 'tags', 'content', 'summary']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Required field '{field}' is missing")
    
    if not isinstance(data['level'], int) or not 1 <= data['level'] <= 3:
        raise ValueError("Level must be an integer between 1 and 3")
    
    if not isinstance(data['tags'], list):
        raise ValueError("Tags must be a list")
    
    if not data['title'].strip():
        raise ValueError("Title cannot be empty")
    
    if not data['content'].strip():
        raise ValueError("Content cannot be empty")
    
    if not data['summary'].strip():
        raise ValueError("Summary cannot be empty")

def save_knowledge_file(filename: str, file_content: bytes):
    """Save a knowledge file"""
    ensure_knowledge_dir()
    file_path = KNOWLEDGE_FILES_DIR / filename
    
    # Verify it's valid YAML before saving
    try:
        content = file_content.decode('utf-8')
        data = yaml.safe_load(content)
        if not isinstance(data, dict):
            raise ValueError("Invalid YAML format: must be a dictionary")
        
        # Validate content against template
        validate_knowledge_content(data)
        
        # Save the file
        with open(file_path, 'wb') as f:
            f.write(file_content)
            
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML format: {str(e)}")

def get_knowledge_file(filename: str) -> bytes:
    """Get a knowledge file's content"""
    file_path = KNOWLEDGE_FILES_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filename}")
    
    with open(file_path, 'rb') as f:
        return f.read()

def delete_knowledge_file(filename: str):
    """Delete a knowledge file"""
    file_path = KNOWLEDGE_FILES_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filename}")
    
    file_path.unlink()

def rebuild_database():
    """Rebuild the SQLite database from YAML files"""
    ensure_knowledge_dir()
    
    # Reset database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM knowledge")
    
    # Load all YAML files and insert into database
    for file_path in KNOWLEDGE_FILES_DIR.glob("*.yaml"):
        try:
            data = load_yaml_file(file_path)
            if isinstance(data, dict):  # 유효한 YAML 파일인지 확인
                cursor.execute("""
                    INSERT INTO knowledge (title, level, tags, content, summary)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    data.get('title', ''),
                    data.get('level', 1),
                    json.dumps(data.get('tags', []), ensure_ascii=False),
                    data.get('content', ''),
                    data.get('summary', '')
                ))
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    conn.commit()
