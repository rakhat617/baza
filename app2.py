import psycopg2

conn = psycopg2.connect(
    dbname="magazin",
    user="postgres",
    password="1211",
    host="127.0.0.1"
)

conn.autocommit = True
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXIST customers(
        id SERAIL PRIMARY KEY,
        name VARCHAR(60),
        age INTEGER
    )
''')

def create_customer(name:str, age:int):
    cur.execute("""INSERT INTO customers(name, age) VALUES(%s, %s)""", (name, age))

def read_customer():
    cur.execute("""
        SELECT * FROM customers
    """)
    customers = cur.fetchall()
    for customer in customers:
        print(customer)
    
def  update_customer(customer_id:int, name:str=None, age:int=None):
    