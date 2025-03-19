import cx_Oracle;
import pandas as pd;

con = cx_Oracle.connect("madang", "madang", "localhost:1521/xe", encoding="UTF-8");
query = "SELECT * FROM book";

df = pd.read_sql_query(query, con)
df