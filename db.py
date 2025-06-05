import psycopg2

try:
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1211",
        host="127.0.0.1",
        port=5432
    )
    cursor = connection.cursor()
except Exception as e:
    print(e)

CREATE_QUERY : str = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        login VARCHAR(32) NOT NULL,
        password CHAR(32) NOT NULL
    );
"""
cursor.execute(CREATE_QUERY)
connection.commit()

TRANSACTIONS_TABLE_QUERY : str = """
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        user_id SERIAL NOT NULL,
        amount DECIMAL NOT NULL,
        is_income BOOLEAN NOT NULL,
        category_id SERIAL NOT NULL,

        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
"""
cursor.execute(TRANSACTIONS_TABLE_QUERY)
connection.commit()

CATEGORY_TABLE_QUERY : str = """
    CREATE TABLE IF NOT EXISTS categories (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL
    );
"""
cursor.execute(CATEGORY_TABLE_QUERY)
connection.commit()
