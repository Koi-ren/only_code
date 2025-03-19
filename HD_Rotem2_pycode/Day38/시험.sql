--문항1] 오라클을 설치하면 제공되는 사용자인 SCOTT은 학습을 위해서 테이블들이 제공된다.
--SCOTT이 소유하고 있는 테이블을 살펴보면 dept, emp 테이블이 존재하는데,
--사원정보를 저장하는 emp 테이블에 저장된 데이터를 활용해
--사원의 이름과 급여와 입사일자만을 출력하는 SQL 문을 작성하시오. (배점:10)
--<힌트> 사원 정보가 저장된 테이블의 이름은 EMP이고,
--사원번호에 해당되는 컬럼 이름은 empno이고,
--사원이름 칼럼은 ENAME, 급여 칼럼은 SAL, 입사일자 칼럼은 HIREDATE 이다.

SELECT ENAME, SAL, HIREDATE
FROM EMP;

--[문항2] 부서번호(DEPTNO)가 10번이 아닌 사원의 사원이름, 부서번호, 직급을 출력하세요.
--(배점:10)
SELECT ENAME,DEPTNO, JOB	
FROM	EMP
WHERE	DEPTNO NOT IN (10);

--[문항3] 이름 중 A를 포함하는 사원을 검색하는 SQL을 작성하시오. (배점:10)
SELECT *
FROM    EMP
WHERE   ENAME LIKE ('%A%');


--부서별로 그룹지은 후(GROUP BY), 그룹 지어진 부서별 평균 급여가 2000 이상인(HAVING) 
--부서번호와 부서별 평균 급여를 출력하는 쿼리문을 작성하시오. (배점:10)


--[문항5] 이름이 SCOTT인 사람의 부서명을 출력하는 SQL 질의문을 작성하시오. (배점:10)
SELECT JOB
FROM EMP
WHERE ENAME LIKE('SCOTT');

--[문항6] 평균 급여를 구하는 쿼리문을 서브 쿼리로 사용하여 
--평균 급여보다 더 많은 급여를 받는 사원을 검색하는 
--SQL 질의문을 부속 질의(SubQuery)를 사용해 작성하시오. (배점:15)
SELECT *
FROM EMP
WHERE SAL> (SELECT AVG(SAL) FROM EMP);


--[문항7] 3000 이상 받는 사원이 소속된 부서(10번, 20번)와 동일한 부서에서 근무하는 
--사원이기에 서브 쿼리의 결과 중에서 하나라도 일치하면 
--참인 결과를 구하는 질의문을 술어 IN과 부속질의(SubQuery)를 사용해 작성하시오. (배점:15)
SELECT *
FROM EMP
WHERE DEPTNO IN (
    SELECT DEPTNO
    FROM EMP
    WHERE SAL >= 3000
    AND DEPTNO IN (10, 20)
);

--[문항8] 사원 테이블과 유사한 구조의 사원번호(EMPNO), 사원이름(ENAME), 급여(SAL) 3개의 칼럼으로 구성된 EMP01 테이블을 생성하는 질의를 작성하시오.
--
--+ 테이블명 : EMP01
--+ 사원번호(EMPNO) : 숫자 4자리
--+ 사원이름(ENAME) : 가변길이 문자, 최대20글자
--+ 급여(SAL) : 숫자 7자리 (배점:10)
CREATE TABLE EMP01 (
	EMPNO 		NUMBER(4),
	ENAME 		VARCHAR2(20),
	SAL         NUMBER(7)
	);