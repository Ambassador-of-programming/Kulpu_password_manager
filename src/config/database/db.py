import aiosqlite
from typing import Union

class DatabaseManager:
    def __init__(self):
        self.db_name = 'src/config/database/passwords.db'

    async def connect(self):
        self.connection = await aiosqlite.connect(self.db_name)

    async def close(self):
        if self.connection:
            await self.connection.close()
    
    async def execute_query(self, query, *args):
        async with self.connection.execute(query, args) as cursor:
            return await cursor.fetchall()

    async def execute_write_query(self, query, *args):
        async with self.connection.execute(query, args) as cursor:
            await self.connection.commit()
            
class Password_Database(DatabaseManager):
    def __init__(self):
        super().__init__()

    async def create_db(self):
        await self.connect()
        query = "CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, title TEXT, password TEXT, login TEXT, url_site TEXT, email TEXT, notes TEXT, key_words TEXT, creation_date TEXT, change_date TEXT)"
        await self.execute_write_query(query)
        await self.close()

    async def delete_id(self, id: int):
        await self.connect()
        query = f"DELETE FROM passwords WHERE id = {id}"
        await self.execute_write_query(query)
        await self.close()

    async def add_record(self, **kwargs):
        '''Adding a password record to the "Passwords" database'''

        await self.connect()
        delete_key = []
        for key, value in kwargs.items():
            if isinstance(value, str) and value.strip() == '':
                delete_key.append(key)
        for i in delete_key:
            kwargs.pop(i)
        # Преобразование списка в строку через запятую, если он присутствует
        for key, value in kwargs.items():
            if isinstance(value, list):
                kwargs[key] = ', '.join(value)

        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs.values()])
        query = f"INSERT INTO 'passwords' ({columns}) VALUES ({placeholders})"
        await self.execute_write_query(query, *kwargs.values())
        await self.close()

    async def read_records(self, *args):
        fields = ', '.join(args)
        await self.connect()
        query = f"SELECT {fields} FROM passwords"

        result = await self.execute_query(query)
        await self.close()
        return result

    async def get_all_data_by_id(self, id: int) -> Union[dict, None]:
        await self.connect()
        query = f"SELECT * FROM passwords WHERE id = {id}"
        result = await self.execute_query(query)
        await self.close()
        if result:
            # Получаем имена столбцов из структуры результата
            columns = ["id", "title", "password", "login", "url_site", "email", "notes", "key_words", "creation_date", "change_date"]
            # Предполагаем, что result содержит один кортеж с данными, преобразуем его в словарь
            data_dict = {}
            for i, column in enumerate(columns):
                data_dict[column] = result[0][i]
            new_data_dict = {}
            for key, value in data_dict.items():
                if value is not None:  # Проверяем, что значение не равно None
                    new_data_dict[key] = value  # Добавляем ключ и значение в новый словарь
            return new_data_dict
        else:
            return None
        
class Payment_Database(DatabaseManager):
    def __init__(self):
        super().__init__()
    
    async def create_db(self):
        await self.connect()
        await self.execute_write_query("CREATE TABLE IF NOT EXISTS 'payments' \
            ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'title' TEXT, 'password' TEXT, \
            'login' TEXT, 'url_site' TEXT, 'email' TEXT, 'notes' TEXT, 'key_words' TEXT, \
            'creation_date' TEXT, 'change_date' TEXT)")
        await self.close()

    async def delete_db(self):
        await self.connect()
        await self.execute_write_query("DROP TABLE IF EXISTS 'passwords'")
        await self.close()

# import asyncio

# async def main():
#     db = Password_Database()
#     await db.create_db()

# asyncio.run(main())
