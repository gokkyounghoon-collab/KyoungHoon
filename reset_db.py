from gaeun1.db import engine, Base, init_db

# 데이터베이스 재초기화
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# 초기 데이터 삽입
init_db()

print("데이터베이스 재초기화 완료")
