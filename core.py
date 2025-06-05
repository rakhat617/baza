from db import cursor, connection
from exceptions import UserAlreadyExists, UserAuthFailed


def register(login : str, password : str) -> None:
    query : str = f"SELECT * FROM users WHERE login = '{login}';"
    cursor.execute(query=query)
    if cursor.fetchone():
        raise UserAlreadyExists
    
    insert_query : str = f"""
        INSERT INTO users
        (login, password)
        VALUES
        ('{login}', '{password}');
    """
    cursor.execute(insert_query)
    connection.commit()

def auth(login : str, password : str) -> None:
    query : str = f"""
        SELECT * FROM users 
        WHERE login = '{login}'
        AND password = '{password}';
    """
    cursor.execute(query=query)
    if not cursor.fetchone():
        raise UserAuthFailed

def create_category(title : str) -> None:
    query : str = f"""
        INSERT INTO categories
        (title)
        VALUES
        ('{title}');
    """
    cursor.execute(query)
    connection.commit()

def show_categories() -> list:
    query : str = """SELECT * FROM categories"""
    cursor.execute(query=query)
    connection.commit()
    categories = cursor.fetchall()
    return categories

def show_transactions(username:str) -> list:
    query : str = f"""SELECT * FROM categories JOIN transactions
        ON categories.id = transactions.category_id JOIN users 
        ON transactions.user_id = users.id
        WHERE users.login = '{username}'
    """
    cursor.execute(query=query)
    connection.commit()
    transactions = cursor.fetchall()
    return transactions

def add_transaction(username:str, amount:float, is_income:bool, category:str) -> None:
    query : str = f"""INSERT INTO transactions (user_id, amount, is_income, category_id)
        VALUES ((SELECT id FROM users WHERE login = '{username}'), {amount}, {is_income}, (SELECT id FROM categories WHERE title = '{category}'))
    """
    cursor.execute(query)
    connection.commit()

def calculate_transactions(username:str, category:str) -> list[float]:
    query_income : str = f"""SELECT SUM(transactions.amount) FROM categories JOIN transactions
        ON categories.id = transactions.category_id JOIN users 
        ON transactions.user_id = users.id
        WHERE users.login = '{username}' AND transactions.is_income = TRUE{category}
    """
    cursor.execute(query_income)
    connection.commit()
    income_sum = cursor.fetchone()[0]
    if not income_sum:
        income_sum = 0
    query_outgoings : str = f"""SELECT SUM(transactions.amount) FROM categories JOIN transactions
        ON categories.id = transactions.category_id JOIN users 
        ON transactions.user_id = users.id
        WHERE users.login = '{username}' AND transactions.is_income = FALSE{category}
    """
    cursor.execute(query_outgoings)
    connection.commit()
    outgoings_sum = cursor.fetchone()[0]
    if not outgoings_sum:
        outgoings_sum = 0
    return income_sum, outgoings_sum
