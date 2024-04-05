import flet as ft 
from system.ru.add.modules.addpass_module import AddPass
from system.ru.add.modules.deletepassword_module import DeletePassword

async def add(page: ft.Page):
    
    class Button:
        def __init__(self) -> None:
            self.column = ft.Column(visible=False)
            self.all_bottons = ft.ResponsiveRow(controls=[
                ft.FilledButton(
                text='Добавить пароль',
                icon=ft.icons.ADD,
                icon_color=ft.colors.GREEN,
                on_click=self.choice_add_pass,
                col=6),
                
                ft.FilledButton(
                text='Удалить пароль',
                icon=ft.icons.DELETE,
                icon_color=ft.colors.RED,
                on_click=self.choice_delete_pass,
                col=6),
                
                ft.FilledButton(
                text='Добавить категорию',
                icon=ft.icons.ADD,
                icon_color=ft.colors.YELLOW,
                on_click=self.choice_add_category,
                col=6),

                ft.FilledButton(
                text='Изменить пароль',
                icon=ft.icons.EDIT,
                icon_color=ft.colors.GREEN_200,
                on_click=self.choice_edit_pass,
                col=6),

                ft.FilledButton(
                text='Изменить категорию',
                icon=ft.icons.EDIT,
                icon_color=ft.colors.YELLOW_200,
                on_click=self.choice_edit_category,
                col=6),
            
            ])
    
        async def choice_add_pass(self, event):
            if self.column.visible == False:
                self.column.controls = await add_pass.group()
                self.column.visible = True
                self.column.update()
            else:
                self.column.visible = False
                self.column.update()
        
        async def choice_delete_pass(self, event):
            if self.column.visible == False:
                self.column.controls = await delete_password.group()
                self.column.visible = True
                self.column.update()
            else:
                self.column.visible = False
                self.column.update()

        async def choice_add_category(self, event):
            if self.column.visible == False:
                self.column.controls = await add_pass.group()
                self.column.visible = True
                self.column.update()
            else:
                self.column.visible = False
                self.column.update()

        async def choice_edit_pass(self, event):
            if self.column.visible == False:
                self.column.controls = await add_pass.group()
                self.column.visible = True
                self.column.update()
            else:
                self.column.visible = False
                self.column.update()

        async def choice_edit_category(self, event):
            if self.column.visible == False:
                self.column.controls = await add_pass.group()
                self.column.visible = True
                self.column.update()
            else:
                self.column.visible = False
                self.column.update()
    
    button = Button()

    delete_password = DeletePassword()
    await delete_password.init(page, button.column)

    add_pass = AddPass()
    await add_pass.init(page, button.column)

    content = ft.Column(
        controls=[
            button.all_bottons,
            button.column,
        ],
    )

    return content