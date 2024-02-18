import aiosqlite
import datetime
import asyncio

class DatabaseManager:
    def __init__(self):
        self.db_name = 'config/passwords.db'

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

    async def add_record(self, **kwargs):
        await self.connect()

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

    
# async def main():
#     db = DatabaseManager()
#     return await db.read_records('id', 'title', 'creation_date')

# print(asyncio.run(main()))
