import flet as ft 

async def generator_pass(page: ft.Page):
    class GenPass:
        def __init__(self) -> None:
            self.slider_value = ft.Text("Длина пароля: 0")
            self.password_length = ft.CupertinoSlider(
                min=1,
                max=100,
                active_color=ft.colors.PURPLE,
                thumb_color=ft.colors.PURPLE,
                on_change=self.handle_change,
            )
            self.digits = ft.Checkbox(adaptive=True, label="Использовать цифры", value=True)
            self.symbols = ft.Checkbox(adaptive=True, label="Использовать спец. символы", value=True)
            self.uppercase = ft.Checkbox(adaptive=True, label="Использовать большие буквы", value=True)
            self.buttom = ft.ElevatedButton(text='Сгенерировать')

        async def handle_change(self, event):
            self.slider_value.value = f'Длина пароля: {int(event.control.value)}'
            await self.slider_value.update_async()

    genpass = GenPass()
    content = ft.Column(controls=[
        ft.ResponsiveRow([
            ft.Text(
                value='Генератор паролей',
            ),
        ]),
        ft.ResponsiveRow([
            genpass.slider_value,
            genpass.password_length,
            
        ]),
        ft.ResponsiveRow([
            genpass.digits, genpass.symbols
        ]),
        ft.ResponsiveRow([
            genpass.uppercase
        ]),
        ft.ResponsiveRow([
            genpass.buttom
        ]),

    ])
    return content