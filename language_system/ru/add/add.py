import flet as ft 
from language_system.ru.add.modules.addpass_module import AddPass
        
async def add(page: ft.Page):
    
    class Button:
        def __init__(self) -> None:
            self.column = ft.Column(visible=False)
            self.button_add_pass = ft.FilledButton(
                text='Добавить пароль',
                icon=ft.icons.ADD,
                icon_color=ft.colors.GREEN,
                on_click=self.choice_add_pass,
                col={"md": 4, "sm": 100}
            )
            self.button_add_category = ft.FilledButton(
                text='Добавить категорию',
                icon=ft.icons.ADD,
                icon_color=ft.colors.YELLOW,
                on_click=self.choice_add_category,
                col={"md": 4, "sm": 100}
            )
            self.button_edit_pass = ft.FilledButton(
                text='Изменить пароль',
                icon=ft.icons.EDIT,
                icon_color=ft.colors.GREEN_200,
                on_click=self.choice_edit_pass,
                col={"md": 4},
            )
            self.button_edit_category = ft.FilledButton(
                text='Изменить категорию',
                icon=ft.icons.EDIT,
                icon_color=ft.colors.YELLOW_200,
                on_click=self.choice_edit_category,
                col={"md": 4},
            )
    
        async def choice_add_pass(self, event):
            if self.column.visible == False:
                self.column.controls = await add_pass.group()
                self.column.visible = True
                await self.column.update_async()
            else:
                self.column.visible = False
                await self.column.update_async()

        async def choice_add_category(self, event):
            if self.column.visible == False:
                self.column.controls = await add_pass.group()
                self.column.visible = True
                await self.column.update_async()
            else:
                self.column.visible = False
                await self.column.update_async()

        async def choice_edit_pass(self, event):
            if self.column.visible == False:
                self.column.controls = await add_pass.group()
                self.column.visible = True
                await self.column.update_async()
            else:
                self.column.visible = False
                await self.column.update_async()

        async def choice_edit_category(self, event):
            if self.column.visible == False:
                self.column.controls = await add_pass.group()
                self.column.visible = True
                await self.column.update_async()
            else:
                self.column.visible = False
                await self.column.update_async()
    
    button = Button()
    add_pass = AddPass()
    await add_pass.init(page, button.column)
    content = ft.Column(
        controls=[
            ft.Row(height=10),
            ft.ResponsiveRow(
                controls=[
                    button.button_add_pass,
                    button.button_add_category,
                ],
                run_spacing={"xs": 10},
                alignment=ft.MainAxisAlignment.CENTER,
                # spacing=10,
            ),
            ft.ResponsiveRow(
                controls=[
                    button.button_edit_pass,
                    button.button_edit_category,
                ],
                run_spacing={"xs": 10},
                alignment=ft.MainAxisAlignment.CENTER,

                # spacing=10,
            ),
            button.column
        ],
    )

    return content
            
        
    
# async def main(page: ft.Page):
#     await page.add_async(
#         await add(page)
#     )

# ft.app(target=main)