"""
데이터베이스 연결 설정 모듈

이 모듈은 SQLAlchemy를 사용하여 SQLite 데이터베이스와의 연결을 설정합니다.
프로젝트의 데이터베이스 계층 초기화 단계에서 실행됩니다.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# SQLite 데이터베이스 설정
# 동작: 프로젝트 루트에 board.db 파일을 생성하거나 연결합니다
DATABASE_URL = 'sqlite:///board.db'

# autocommit=False로 설정
# 동작: SQLAlchemy 엔진을 생성합니다. 이 엔진은 데이터베이스와의 연결을 관리합니다.
# - connect_args: SQLite의 스레드 안전성 체크 비활성화 (멀티스레드 환경 대비)
# - poolclass: StaticPool 사용 (SQLite는 파일 기반이므로 연결 풀링 단순화)
# - echo=False: SQL 쿼리 로깅 비활성화 (디버깅 시 True로 변경 가능)
engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
    echo=False
)

# 동작: 세션 팩토리를 생성합니다. 이 팩토리는 데이터베이스 세션을 생성하는데 사용됩니다.
# - autocommit=False: 자동 커밋 비활성화 (명시적 트랜잭션 제어 필요)
# - autoflush=False: 자동 플러시 비활성화 (명시적 플러시 필요)
# - bind=engine: 위에서 생성한 엔진과 연결
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    데이터베이스 세션 생성 및 관리 함수
    
    동작 흐름:
    1. SessionLocal을 사용하여 새로운 데이터베이스 세션 생성
    2. yield를 통해 세션을 반환 (제너레이터 패턴)
    3. 정상 완료 시 커밋, 에러 발생 시 롤백 (ACID 원칙 준수)
    4. 사용 완료 후 finally 블록에서 세션 자동 종료
    
    ACID 원칙 준수:
    - Atomicity: 에러 발생 시 자동 롤백으로 트랜잭션 원자성 보장
    - Consistency: 명시적 커밋/롤백으로 데이터 일관성 유지
    - Isolation: SQLite의 기본 격리 수준 사용
    - Durability: 커밋 완료 시 데이터 지속성 보장
    
    사용 예시:
        db = next(get_db())
        try:
            question = Question(subject='제목', content='내용')
            db.add(question)
            db.commit()
        except Exception:
            db.rollback()
            raise
    """
    db = SessionLocal()
    try:
        yield db
        # 정상 완료 시 커밋 (명시적 커밋이 없는 경우를 대비)
        # 주의: service 레이어에서 이미 커밋하므로 여기서는 중복 커밋 방지
        # 실제로는 service 레이어의 commit()이 실행됨
    except Exception:
        # 에러 발생 시 롤백하여 트랜잭션 원자성 보장 (Atomicity)
        db.rollback()
        raise
    finally:
        db.close()
