-- 1. 마당 서점의 고객이 요구하는 다음 질문에 대해 SQL 문을 작성하시오
--- (1) 도서번호가 1인 도서의 이름
SELECT bookname 
FROM Book 
WHERE bookid=1;

--- (2) 가격이 20,000원 이상인 도서의 이름
SELECT bookname
FROM Book
WHERE price >=20000;

---(3) 박지성의 총 구매액
SELECT SUM(saleprice)
FROM Customer, Orders
WHERE Customer.custid=Orders.custid
        AND Customer.name LIKE '박지성';
        
---(4) 박지성의이 구매한 총 도서의 수
SELECT COUNT(*)
FROM Customer, Orders
WHERE Customer.custid=Orders.custid
        AND Customer.name LIKE '박지성';
    
---(1,5) 박지성이 구매한 도서의 출판사 수
SELECT COUNT(DISTINCT publisher)
FROM Customer, Orders, Book
WHERE Customer.custid=Orders.custid
        AND Orders.bookid=Book.bookid
        AND Customer.name LIKE '박지성';

---(1, 6) 박지성이 구매한 도서의 이름, 가격, 정과와 판매가격의 차이
SELECT bookname, price, price-saleprice
FROM Customer, Orders, Book
WHERE Customer.custid=Orders.custid
        AND Orders.bookid=Book.bookid
        AND Customer.name LIKE '박지성';
        
-- 2. 마당서점의 운영자와 경영자가 요구하는 다음 질문에 대해 SQL문을 작성하시오.
---(2, 1) 마당서점 도서의 총 개수
SELECT count(*)
FROM Book;

---(2, 2) 마당서점에 도서를 출고하는 출판사의 총 개수
SELECT COUNT(Distinct publisher)
FROM Book;

---(2, 3) 모든 고객의 이름, 주소
SELECT name, address
FROM Customer;

---(2, 4) 2014년 7월 4일~7월 7일 사이에 주문받은 도서의 주문번호
SELECT *
FROM Orders
WHERE orderdate BETWEEN '20140704' AND '20140707';

---(2, 5) 2014년 7월 4일~7월 7일 사이에 주문받은 도서를 제외한 도서의 주문번호
SELECT *
FROM Orders
WHERE orderdate NOT BETWEEN '20140704' AND '20140707';

---(2, 6) 성이 '김'씨인 고객의 이름과 주소
SELECT name, address
FROM Customer
WHERE name LIKE '김%';

---(2, 7) 성이 '김'씨이고 이름이 '아'로 끝나는 고객의 이름과 주소
SELECT name, address
FROM Customer
WHERE name LIKE '김%아';

---(2, 8) 주문하지 않은 고객의 이름(부속질의 사용)
SELECT name
FROM Customer
WHERE name NOT IN(
                    SELECT name
                    FROM Orders, Customer
                    WHERE Orders.custid=Customer.custid);
                    
---(2, 9) 주문 금액의 총액과 주문의 평균 금액
SELECT SUM(saleprice), AVG(saleprice)
FROM Orders;

---(2, 10) 고객의 이름과 고객별 구매액
SELECT name, SUM(saleprice)
FROM Orders, Customer
WHERE Orders.custid=Customer.custid
GROUP BY name;

---(2, 11) 고객의 이름과 고객이 구매한 도서 목록
SELECT name, bookname
FROM Book, Orders, Customer
WHERE Book.bookid=Orders.bookid
        AND Orders.custid=Customer.custid;

---(2, 12) 도서의 가격(Book 테이블)과 판매가격(Orders 테이블)의 차이가 가장 많은 주문
SELECT *
FROM Book, Orders
WHERE Book.bookid=Orders.bookid
        AND price-saleprice = (
                                SELECT MAX(price-saleprice)
                                FROM Book, Orders
                                WHERE Book.bookid=Orders.bookid);

--(2, 13)도서의 판매액 평균보다 자신의 구매액 평균이 더 높은 고객의 이름 ***
SELECT c.name
From customer c 
JOIN orders o ON c.custid = o.custid
GROUP BY c.name, o.custid -- 고객을 뽑고 싶기 때문
HAVING avg(saleprice)>(select avg(o.saleprice)
from orders o);
