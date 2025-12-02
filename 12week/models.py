"""
ORM 모델 정의 모듈

이 모듈은 SQLAlchemy의 선언적 베이스를 사용하여 데이터베이스 테이블을 Python 클래스로 정의합니다.
프로젝트의 모델 계층 초기화 단계에서 실행됩니다.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# 동작: SQLAlchemy의 선언적 베이스를 생성합니다.
# 이 Base는 모든 모델 클래스가 상속받을 기본 클래스입니다.
# Base.metadata는 모든 모델의 스키마 정보를 담고 있습니다.
Base = declarative_base()

class Question(Base):
    """
    질문(Question) 모델 클래스
    
    동작 흐름:
    1. Base를 상속받아 ORM 모델로 정의
    2. __tablename__으로 데이터베이스 테이블 이름 지정
    3. 각 컬럼을 Column으로 정의하여 스키마 정보 제공
    4. Alembic이 이 모델을 읽어서 마이그레이션 스크립트 자동 생성
    
    테이블 구조:
    - id: 질문의 고유 번호 (Primary Key, 자동 증가)
    - subject: 질문 제목 (필수 입력)
    - content: 질문 내용 (필수 입력)
    - create_date: 질문 작성일시 (자동으로 현재 시간 설정)
    """
    __tablename__ = 'question'
    
    # 동작: Primary Key로 설정되어 자동으로 고유 번호가 할당됩니다.
    id = Column(Integer, primary_key=True)
    
    # 동작: nullable=False로 설정되어 반드시 값이 입력되어야 합니다.
    subject = Column(String, nullable=False)
    
    # 동작: nullable=False로 설정되어 반드시 값이 입력되어야 합니다.
    content = Column(String, nullable=False)
    
    # 동작: default=datetime.now로 설정되어 레코드 생성 시 자동으로 현재 시간이 저장됩니다.
    create_date = Column(DateTime, nullable=False, default=datetime.now)

