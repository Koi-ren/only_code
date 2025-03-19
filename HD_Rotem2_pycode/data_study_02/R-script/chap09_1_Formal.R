# chap09_1_Formal

#####################################
## Chapter09_1. 정형 데이터 처리
#####################################

## 1.1 Oracle 정형 데이터 처리 

# 1. 패키지 설치
# - RJDBC 패키지를 사용하기 위해서는 우선 java를 설치해야 한다.
install.packages("rJava")
install.packages("DBI")
install.packages("RJDBC")

# 2. 패키지 로딩
library(DBI)
Sys.setenv(JAVA_HOME='C:\\Program Files\\Java\\jre1.8.0_151')
library(rJava)
library(RJDBC) # rJava에 의존적이다.(rJava 먼저 로딩)

# 3) Oracle 연동   

############ Oracle 11g ##############
# driver  
drv <- JDBC("oracle.jdbc.driver.OracleDriver", 
      "C:\\oraclexe\\app\\oracle\\product\\11.2.0\\server\\jdbc\\lib\\ojdbc6.jar")
# db연동(driver, url,uid,upwd)   
conn<-dbConnect(drv, "jdbc:oracle:thin:@//127.0.0.1:1521/xe","scott","tiger")
####################################


# 1. 모든 레코드 검색
query <- "select * from test_table"
dbGetQuery(conn, query)

# db 내용 수정 : insert, update, delete

# 2. 정렬 조회 - 나이 칼럼을 기준으로 내림차순 정렬
query = "SELECT * FROM test_table order by age desc"
dbGetQuery(conn, query)

# 3. 레코드 삽입 
query <- "insert into test values('kang', '1234', '강감찬', 45)"
dbSendUpdate(conn, query)
query <- "select * from test_table"
dbGetQuery(conn, query)

# 4. 조건 검색 - 나이가 40세 이상인 레코드 조회
query = "select * from test_table where age >= 40"
result <- dbGetQuery(conn, query)
result

# 5. 레코드 수정 : 데이터 ‘강감찬’의 나이를 40으로 수정
query = "update test_table set age=40 where name='강감찬'"
dbSendUpdate(conn, query)
query <- "select * from test_table"
dbGetQuery(conn, query)

# 6. 레코드 삭제 – 데이터 ‘홍길동’ 레코드 삭제
query = "delete from test_table where name='홍길동'"
dbSendUpdate(conn, query)
query <- "select * from test_table"
dbGetQuery(conn, query)

# db 연결 종료
dbDisconnect(conn)


## 1.2 MariaDB 정형 데이터 처리 

# 패키지 설치
#install.packages("rJava")
#install.packages("DBI")
#$install.packages("RJDBC") # JDBC()함수 제공 

# 패키지 로딩
library(DBI)
Sys.setenv(JAVA_HOME='C:\\Program Files\\Java\\jre1.8.0_151')
library(rJava)
library(RJDBC) # rJava에 의존적이다.

################ MariaDB or MySql ###############
drv <- JDBC(driverClass="com.mysql.jdbc.Driver", 
            classPath = "C:/mysql-connector/mysql-connector-java-5.1.37-bin.jar")

# driver가 완전히 로드된 후 db를 연결한다.
conn <- dbConnect(drv, "jdbc:mysql://127.0.0.1:3306/work", "scott", "tiger")
#################################################           

# DB 연결 확인 :  테이블의 컬럼 보기 
dbListFields(conn, "goods") 
# [1] "code" "name" "su"   "dan" 

# 테이블의 레코드 조회
# 1. 전체 레코드 검색(select 문)
query = "select * from goods"
goodsAll <- dbGetQuery(conn, query)
goodsAll

# 2. 조건 검색 - 수량이 3 이상인 경우
query = "select * from goods where su >= 3"
goodsOne <- dbGetQuery(conn, query)
goodsOne

# 3.정렬 검색 - 단가를 내림차순으로 정렬
query = "SELECT * FROM goods order by dan desc"
dbGetQuery(conn, query)

# [실습] 테이블에 자료 저장
insert.df <- data.frame(code=5, name='식기세척기', su=1, dan=250000)
insert.df    
dbWriteTable(conn, "goods", insert.df)

# 테이블 조회 
query = "select * from goods"
goodsAll <- dbGetQuery(conn, query) 
goodsAll


# [실습] CSV 파일의 자료를 테이블에 저장
# 1. 파일 자료를 테이블에 저장하기
recode <- read.csv("C:/Rwork/Part-II/recode.csv") 
dbWriteTable(conn, "goods", recode)

# 2. 테이블 조회
query = "select * from goods"
goodsAll <- dbGetQuery(conn, query) 
goodsAll

# [실습] 테이블에 자료 추가, 수정, 삭제
# 1. 테이블에 레코드 추가하기
query = "insert into goods values (6, 'test', 1, 1000)"
dbSendUpdate(conn, query)

# 2. 테이블의 레코드 수정
query = "update goods set name='테스트' where code=6"
dbSendUpdate(conn, query)

# 3. 테이블의 레코드 삭제
delquery = "delete from goods where code=6"
goodsInsert <- dbSendUpdate(conn, delquery) 

# db 연결 종료
dbDisconnect(conn)


