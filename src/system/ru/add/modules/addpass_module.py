import flet as ft
from config.database.db import Password_Database
from config.database.crud import DatabaseManager

from datetime import datetime

class AddPass():
    async def init(self, page: ft.Page, column: ft.Column) -> None:
        self.page = page
        self.count = []
        self.column = column
        self.error_text = ft.Text(color='red')
        self.title = ft.TextField(
            label="* Заголовок",
            col={"md": 4},
        )
        self.pas = ft.TextField(
            label="* Пароль", can_reveal_password=True,
            password=True,
            col={"md": 4},
        )
        self.url_site = ft.TextField(
            label="Название учетной записи или сайта",
            col={"md": 4},
        )
        self.login = ft.TextField(
            label="Логин или имя пользователя",
            col={"md": 4},
        )
        self.email = ft.TextField(
            label="Электронная почта",
            col={"md": 4},
        )
        self.notes = ft.TextField(
            label="Примечания",
            col={"md": 4},
        )
        self.key_words = ft.TextField(
            label="Ключивые слова",
            col={"md": 4},
        )
        self.content = [
            ft.ResponsiveRow(controls=[
                await self.add_title(),
                await self.add_pass(),
            ],
            alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.ResponsiveRow(controls=[
                await self.add_login(),
                await self.add_url_site(),
            ],
            alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.ResponsiveRow(controls=[
                await self.add_email(),
                await self.add_note(),
            ],
            alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.ResponsiveRow(controls=[
                await self.add_key_words(),
            ],
            alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.ResponsiveRow(controls=[
                self.error_text,
                await self.add(),
                await self.add_save()
            ],
            alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.ResponsiveRow(height=10),
        ]

    async def add_title(self) -> ft.TextField:
        return self.title
    
    async def add_pass(self) -> ft.TextField:
        return self.pas
    
    async def add_url_site(self) -> ft.TextField:
        return self.url_site
    
    async def add_login(self) -> ft.TextField:
        return self.login
    
    async def add_email(self) -> ft.TextField:
        return self.email
    
    async def add_note(self) -> ft.TextField:
        return self.notes
    
    async def add_key_words(self) -> ft.TextField:
        return self.key_words
    
    async def add_click(self, event):
            if not self.count:
                self.count.append(1)
            else:
                self.count.append(self.count[-1] + 1)

            if len(self.content[-3].controls) == 1:
                self.content[-3].controls.append(
                    ft.TextField(
                    label='Дополнительный параметр',
                    col={"md": 4},
                    )
                )
                self.column.update()
                
            else:
                self.content.insert(-2, ft.ResponsiveRow(controls=[
                        ft.TextField(
                            label='Дополнительный параметр',
                            col={"md": 4},
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                    ))
                self.column.update()
            self.column.update()

    async def add(self):
        return ft.FilledButton(
            text='Добавить параметр',
            icon=ft.Icons.ADD,
            on_click=self.add_click,
            col={"md": 4},
        )
    async def add_save(self):
        async def save_click(event):
            if all([self.title.value, self.pas.value]):
                db = DatabaseManager()
                db.add_password_record(
                    title=self.title.value.strip(), password=self.pas.value.strip(),
                    login=self.login.value.strip(), url_site=self.url_site.value.strip(),
                    email=self.email.value.strip(), notes=self.notes.value.strip(), 
                    key_words=self.key_words.value.strip(), 
                    creation_date=datetime.now(), change_date=datetime.now()
                    
                )
                # db = Password_Database()
                # await db.add_record(title=self.title.value.strip(), password=self.pas.value.strip(),
                #     login=self.login.value.strip(), url_site=self.url_site.value.strip(),
                #     email=self.email.value.strip(),
                #     notes=self.notes.value.strip(), key_words=self.key_words.value.strip(), 
                #     creation_date=datetime.now(), change_date=datetime.now())
            else:
                print('нету значения')

        return ft.FilledButton(
            text='Сохранить',
            on_click=save_click,
            col={"md": 4},
        )
    
    async def group(self):
        return self.content