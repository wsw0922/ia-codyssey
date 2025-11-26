"""
프로젝트 실행 진입점

이 파일은 FastAPI 애플리케이션의 메인 실행 파일입니다.
프로젝트 실행 시 FastAPI 서버를 시작하고 API 라우터를 등록합니다.

실행 방법: python main.py

API 문서 (자동 생성):
  - Swagger UI: http://localhost:8000/docs
  - ReDoc: http://localhost:8000/redoc
  - OpenAPI 스키마: http://localhost:8000/openapi.json

테스트 명령어:
  - 질문 생성
    curl -X POST http://localhost:8000/questions -H "Content-Type: application/json" -d '{"subject": "질문 제목", "content": "질문 내용"}'
  - 질문 목록 조회
    curl -X GET http://localhost:8000/questions
  - 질문 개별 조회
    curl -X GET http://localhost:8000/questions/1
  - 질문 수정
    curl -X PUT http://localhost:8000/questions/1 -H "Content-Type: application/json" -d '{"subject": "수정된 제목", "content": "수정된 내용"}'
  - 질문 삭제
    curl -X DELETE http://localhost:8000/questions/1
"""
from fastapi import FastAPI
import uvicorn
from database import engine
from models import Base
from api import router

# 동작: FastAPI 애플리케이션 인스턴스를 생성합니다.
# FastAPI는 자동으로 Swagger UI와 ReDoc을 제공합니다:
# - Swagger UI: http://localhost:8000/docs (대화형 API 문서)
# - ReDoc: http://localhost:8000/redoc (대안 문서 UI)
# - OpenAPI 스키마: http://localhost:8000/openapi.json (JSON 형식)
# title, description, version은 Swagger UI에 표시됩니다.
app = FastAPI(
    title='게시판 API',
    description='질문(Question) CRUD API',
    version='1.0.0'
)

# 동작: API 라우터를 애플리케이션에 등록합니다.
# 이렇게 하면 /questions로 시작하는 모든 엔드포인트가 활성화됩니다.
app.include_router(router)


@app.on_event('startup')
async def startup_event():
    """
    애플리케이션 시작 시 실행되는 이벤트 핸들러
    
    동작 흐름:
    1. 데이터베이스 테이블이 존재하는지 확인
    2. 없으면 생성 (Alembic 마이그레이션이 이미 실행되었다면 스킵됨)
    """
    # 동작: models.py에 정의된 모든 모델의 테이블을 데이터베이스에 생성합니다.
    # 이미 테이블이 존재하는 경우 아무 작업도 수행하지 않습니다.
    # 주의: Alembic을 사용하는 경우 마이그레이션으로 테이블을 관리하는 것이 권장됩니다.
    Base.metadata.create_all(bind=engine)
    print('데이터베이스 테이블이 준비되었습니다.')


if __name__ == '__main__':
    """
    메인 실행 흐름:
    
    1. 모듈 import 단계
       - FastAPI, uvicorn import
       - database.py에서 engine import
       - models.py에서 Base import
       - api.py에서 router import
    
    2. FastAPI 앱 생성 및 라우터 등록
       - FastAPI 인스턴스 생성
       - API 라우터 등록
    
    3. 서버 시작
       - uvicorn을 사용하여 서버 실행
       - 기본 포트: 8000
    """
    # 동작: uvicorn을 사용하여 FastAPI 애플리케이션을 실행합니다.
    # host='0.0.0.0': 모든 네트워크 인터페이스에서 접근 가능
    # port=8000: 기본 포트 번호
    uvicorn.run(app, host='0.0.0.0', port=8000)
