from database.db_connection import execute_query


q = """
SELECT id
FROM heroes
WHERE lower(name) LIKE %s
"""
def like(str):
    return "%" + str + "%"

y = input("name")
str = like(y)
x = execute_query(q, (like(y), )).fetchall()
print(x)