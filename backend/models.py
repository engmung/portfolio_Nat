from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Knowledge(Base):
    __tablename__ = "knowledge"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    level = Column(Integer)  # 1: 최상위, 2: 중간, 3: 세부, 4: 사례
    tags = Column(JSON)  # ["관련 키워드", "기술 스택", "분야"]
    summary = Column(JSON)  # {"tech_stack": str, "learnings": str, "one_liner": str}
    content = Column(String)  # 상세 내용
    created_at = Column(DateTime, default=datetime.utcnow)
