"""
질문(Question) 라우터 정의

질문 목록 조회 API 엔드포인트를 정의합니다.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import ApiResponse, Question  # Question 스키마 추가 임포트
from domain.question.service import get_questions

router = APIRouter(prefix='/api/question')


@router.get('/list', response_model=ApiResponse)
def question_list(
    skip: int = 0,
    limit: int = 100,
    # get_db는 contextmanager로 정의되었으므로 의존성 주입 시 컨텍스트 관리자 객체가 주입됨
    db_context = Depends(get_db)
) -> ApiResponse:
    """
    질문 목록을 조회합니다.
    
    Args:
        skip: 건너뛸 레코드 수
        limit: 최대 조회할 레코드 수
        db_context: 데이터베이스 세션 컨텍스트 매니저 (의존성 주입)
        
    Returns:
        질문 목록을 포함한 응답
    """
    # with 구문을 사용하여 DB 세션 연결 및 자동 종료 보장
    with db_context as db:
        questions = get_questions(db, skip=skip, limit=limit)
        
        # Pydantic 모델(Question)을 사용하여 ORM 객체를 스키마 데이터로 변환
        # from_attributes=True 설정 덕분에 model_validate 사용 가능
        question_data_list = [
            Question.model_validate(q) for q in questions
        ]
        
        return ApiResponse(
            status='success',
            data={
                # 변환된 Pydantic 모델 리스트를 사용
                'questions': question_data_list,
                'count': len(questions)
            }
        )