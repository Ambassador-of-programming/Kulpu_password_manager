import flet as ft
from config.database.db import Password_Database
from datetime import datetime

class DeletePassword():
    async def init(self, page: ft.Page, column: ft.Column) -> None:
        self.page = page
        self.count = []
        self.column = column
        self.error_text = ft.Text(color='red')
        self.id = ft.TextField(
            label="* ID",
            col={"md": 4},
            input_filter=ft.NumbersOnlyInputFilter(),
        )

        self.content = [
            ft.ResponsiveRow(controls=[
                self.id,
                await self.delete_save()
            ],
            alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.ResponsiveRow(height=10),
        ]
    
    async def delete_save(self):
        async def save_click(event):
            if all([self.id.value]):
                db = Password_Database()
                await db.delete_id(id=int(self.id.value))
            else:
                print('нету значения')

        return ft.FilledButton(
            text='Удалить',
            on_click=save_click,
            col={"md": 4},
        )
    
    async def group(self):
        return self.content