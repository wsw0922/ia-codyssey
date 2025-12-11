"""
데이터베이스 연결 설정 모듈

이 모듈은 SQLAlchemy를 사용하여 SQLite 데이터베이스와의 연결을 설정합니다.
프로젝트의 데이터베이스 계층 초기화 단계에서 실행됩니다.
"""
import contextlib
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

@contextlib.contextmanager
def get_db():
    db = SessionLocal()
    print("--- DB 세션 연결됨 ---")  # 테스트용 로그 추가
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        print("--- DB 세션 종료됨 ---")  # 테스트용 로그 추가
        db.close()