import psycopg2

conn = psycopg2.connect(
    dbname="magazin",
    user="postgres",
    password="1211",
    host="127.0.0.1"
)

cursor = conn.cursor()

def create_table(table_name:str, fields:dict):
    fields_info = ', '.join(f'{name} {type}' for name, type in fields.items())
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name}(
        {fields_info}
        )
''')

create_table('fff', {'id':'SERIAL', 'name':'VARCHAR(60)', 'surname':'VARCHAR(100)'})

def insert_data(table_name:str, data:list):
    cursor = conn.cursor()
    for row in data:
        columns = ', '.join(row.keys())
        values = "', '".join(str(value) for value in row.values())
        cursor.execute(f'''
            INSERT INTO {table_name}({columns})
            VALUES('{values}');
        ''')
        conn.commit()

insert_data('fff', [{'surname':'Abdrakhmanov', 'name':'Rakhat'}, {'name': 'Adilya'}])


def select_data(table_name:str, fields='*', filter=''):
    if isinstance(fields, list):
        fields = ', '.join(fields)
    if filter:
        filter = "WHERE " + filter
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT {fields} FROM {table_name} {filter}
    ''')
    conn.commit()
    fetched_data = cursor.fetchall()
    return fetched_data

a = select_data(table_name='fff', filter="name = 'Rakhat'")
print(a)

cursor.close()
conn.close()