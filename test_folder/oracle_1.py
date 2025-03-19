import cx_Oracle
import pandas as pd

# 데이터베이스 연결
con = cx_Oracle.connect("madang", "madang", "localhost:1521/xe", encoding="UTF-8")
cursor = con.cursor()

# SQL 쿼리
query = """
    SELECT *
    FROM 테이블
"""

# 쿼리 실행 및 결과 출력
print(query)
cursor.execute(query)
for row in cursor:
    print(row)

# 커서와 커넥션 닫기
cursor.close()
con.close()
