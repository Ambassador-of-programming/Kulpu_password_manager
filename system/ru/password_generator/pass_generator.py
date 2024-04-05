import flet as ft 
import secrets
import string
import asyncio

async def generator_pass(page: ft.Page):
    class GenPass:
        def __init__(self) -> None:
            self.password_length = ft.CupertinoTextField(
                bgcolor=ft.colors.BLUE_100,
                color=ft.colors.BLACK,
                # shadow=ft.BoxShadow(color=ft.colors.RED_400, blur_radius=5, spread_radius=5),
                # on_change=lambda e: print("Введите длина па", e.control.value),
                placeholder_text="Введите длину пароля",
                suffix=ft.Icon(ft.icons.EDIT),
                suffix_visibility_mode=ft.VisibilityMode.EDITING,
                input_filter=ft.NumbersOnlyInputFilter(),
                max_length=3
            )
            self.digits = ft.Checkbox(adaptive=True, label="Использовать цифры", value=True)
            self.symbols = ft.Checkbox(adaptive=True, label="Использовать спец. символы", value=True)
            self.uppercase = ft.Checkbox(adaptive=True, label="Использовать большие буквы", value=True)
            self.buttom = ft.ElevatedButton(text='Сгенерировать', on_click=self.go_pass)
            self.copy_bottom = ft.IconButton(icon=ft.icons.COPY)
            self.error_text = ft.Text(color=ft.colors.RED_400, text_align=ft.TextAlign.CENTER, visible=False)
            self.get_created_password = ft.Text(text_align=ft.TextAlign.CENTER, 
                selectable=True, visible=False, col=2)

        async def go_pass(self, event):
            if all([self.password_length.value]) and int(self.password_length.value) >= 8:

                async def generate_password(length: int, digits=True, symbols=True, uppercase=True) -> str:
                    alphabet = string.ascii_lowercase
                    if uppercase:
                        alphabet += string.ascii_uppercase
                    if digits:
                        alphabet += string.digits
                    if symbols:
                        alphabet += string.punctuation
                    password = ''.join(secrets.choice(alphabet) for _ in range(int(length)))
                    return password
                
                self.error_text.visible = False
                self.error_text.update()

                self.get_created_password.visible = True
                self.get_created_password.value = await generate_password(length=self.password_length.value, digits=self.digits.value, symbols=self.symbols.value, uppercase=self.uppercase.value)
                self.get_created_password.update()

            else:
                self.error_text.visible = True
                self.error_text.value = 'Длина пароля не может быть меньше 8'
                self.error_text.update()
                await asyncio.sleep(5)
                self.error_text.visible = False
                self.error_text.update()

    genpass = GenPass()
    content = ft.Column(controls=[
        ft.ResponsiveRow([
            ft.Text(
                value='Надёжный генератор паролей',
                text_align=ft.TextAlign.CENTER,
            ),
        ]),
        ft.ResponsiveRow([
            genpass.password_length,
            
        ]),
        ft.ResponsiveRow([
            genpass.digits, genpass.symbols
        ]),
        ft.ResponsiveRow([
            genpass.uppercase
        ]),
        ft.ResponsiveRow([
            genpass.get_created_password,
            ft.IconButton(icon=ft.icons.COPY, col=2),
            genpass.error_text
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.ResponsiveRow([
            genpass.buttom
        ]),

    ])
    return content