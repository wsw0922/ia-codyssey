"""
Pydantic 스키마 모델 정의

API 요청/응답에 사용되는 데이터 모델을 정의합니다.
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class QuestionCreate(BaseModel):
    """질문 생성 요청 모델"""
    subject: str
    content: str


class QuestionUpdate(BaseModel):
    """질문 수정 요청 모델"""
    subject: Optional[str] = None
    content: Optional[str] = None


class QuestionResponse(BaseModel):
    """질문 응답 모델"""
    id: int
    subject: str
    content: str
    create_date: datetime
    
    class Config:
        from_attributes = True


class QuestionListResponse(BaseModel):
    """질문 목록 응답 모델"""
    questions: list[QuestionResponse]
    count: int


class ApiResponse(BaseModel):
    """API 공통 응답 모델"""
    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


# --- 과제 요구사항으로 추가된 스키마 ---
class Question(BaseModel):
    """
    새로 추가된 질문 스키마 (과제 요구사항)
    
    데이터 검증 및 직렬화를 담당합니다.
    """
    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        # ORM 객체(SQLAlchemy 등)를 Pydantic 모델로 변환 허용
        from_attributes = True