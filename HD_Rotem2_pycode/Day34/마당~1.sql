select phone
from customer
where name = '김연아';

SELECT bookname, price
FROM Book;

SELECT price, bookname
FROM Book;

SELECT bookid, bookname, publisher, price
FROM Book;

Select *
FROM Book;

select publisher
from book;

SELECT DISTINCT publisher
FROM Book;

SELECT *
FROM Book
WHERE price BETWEEN 10000 AND 20000;

SELECT	bookname, publisher
FROM	Book
WHERE	bookname LIKE '축구의 역사';

SELECT	bookname, publisher
FROM	Book
WHERE	bookname LIKE '%축구%';

SELECT *
FROM Book
WHERE publisher IN('굿스포츠', '대한미디어');

SELECT *
FROM Book
WHERE publisher NOT IN('굿스포츠', '대한미디어');

SELECT *
FROM Book
WHERE bookname LIKE '_구%';

SELECT	*
FROM	Book
ORDER BY	bookname;

SELECT	*
FROM	Book
ORDER BY	price, bookname; 


