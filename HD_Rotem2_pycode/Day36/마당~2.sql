SELECT bookname
FROM Book
WHERE price = (
            SELECT MAX(price) 
            FROM Book);
            
SELECT bookname
FROM Book
WHERE price = (
            SELECT MAX(price) 
            FROM Book);

SELECT name
FROM Customer
WHERE custid IN(
                SELECT custid
                FROM Orders);
                
SELECT name
FROM Customer
WHere custid IN(
                SELECT custid 
                From Orders 
                Where bookid IN(
                                SELECT custid
                                FROM Orders
                                Where bookid IN(
                                                SELECT bookid
                                                FROM Book
                                                WHERE publisher='대한미디어')));
                                                
SELECT b2.publisher, avg(b2.price)
FROM Book b2
GROUP BY b2.publisher;

SELECT b1.bookname
FROM Book b1
WHERE b1.price > ( SELECT avg(b2.price)
                    FROM d