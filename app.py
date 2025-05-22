import psycopg2

conn = psycopg2.connect(
    dbname="magazin",
    user="postgres",
    password="1211",
    host="127.0.0.1"
)

cursor = conn.cursor()

def create_table(table_name:str, fields:dict):
    fields_info = ', '.join(f'{name} {type}' for name, type in fields.items()) #GPT подсказала про метод join
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name}(
        {fields_info}
        )
''')

def insert_data(table_name:str, data:list):
    for row in data:
        fields = ', '.join(row.keys())
        placeholders = ', '.join(['%s'] * len(row)) #GPT подсказала как сделать нужное количество %s
        values = list(row.values())
        cursor.execute(f'''
            INSERT INTO {table_name}({fields})
            VALUES({placeholders});
        ''', values)
        conn.commit()

def select_data(table_name:str, fields='*', filter=None): #Тут все сам придумал 
    if isinstance(fields, list):
        fields = ', '.join(fields)
    if filter: #Мб фильтер не очень, потому что условие юзер сам должен писать, но хз как еще
        filter = "WHERE " + filter
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT {fields} FROM {table_name} {filter}
    ''')
    conn.commit()
    fetched_data = cursor.fetchall()
    return fetched_data

def update_data(table_name:str, id:int, fields_new_values:dict): #Тут тоже все сам.
    for field in fields_new_values: #Можно по идее запариться сделать чтоб несколько сразу рядов можно было обновить, но лень да и зачем
        cursor.execute(f'''
            UPDATE {table_name} 
            SET {field} = '{fields_new_values[field]}' 
            WHERE id = {id}
        ''')
        conn.commit()

def delete_data(table_name:str, id:int): #Тут тоже можно было сделать чтоб несколько рядов сразу, но зачем?
    cursor.execute(f"""
        DELETE FROM {table_name} WHERE id = {id}
    """)
    conn.commit()

def drop_table(table_name:str): #Ну это изи
    cursor.execute(f"""
        DROP TABLE IF EXISTS {table_name}
    """)
    conn.commit()

create_table(table_name="customers", fields={
    "id":"SERIAL PRIMARY KEY",
    "first_name":"VARCHAR(50)",
    "last_name":"VARCHAR(50)",
    "age":"INT"})

insert_data(table_name="customers", data=[{"first_name":"Rakhat", "last_name":"Abdrakhmanov", "age":24},
                                          {"first_name":"Ruslan", "age":23},
                                          {"first_name":"Zhanel", "last_name":"Mektepbayeva"},
                                          {"last_name":"Abishev", "age":21, "first_name":"Bekzhan"}])

print(select_data(table_name="customers", fields=["first_name", "age"], filter="age is not NULL"))

update_data(table_name="customers", id=3, fields_new_values={"age":27})
print(select_data(table_name="customers", fields=["first_name", "age"], filter="age is not NULL"))

delete_data(table_name="customers", id=4)
print(select_data(table_name="customers"))

drop_table(table_name="customers")
print(select_data(table_name="customers"))

cursor.close()
conn.close()