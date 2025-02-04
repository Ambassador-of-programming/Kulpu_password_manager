import flet as ft
import asyncio
import aiofiles
import json


async def settings_view(page: ft.Page):

    async def check_update(event):
        pass
        # page.go('/settings/update')

    # выбор языка приложения
    class Language_selection:
        def __init__(self) -> None:
            self.error_language = ft.Text(color='red')
            self.language_selects = ft.Dropdown(
                width=280,
                label='Выберите язык приложения',
                options=[
                    ft.dropdown.Option("Russian"),
                ]
            )

        async def language_select(self, event):
            if self.language_selects.value == None:
                self.error_language.color = 'red'
                self.error_language.value = "Нельзя выбрать пустое значение"
                self.error_language.update()
                await asyncio.sleep(5)
                self.error_language.value = ''
                self.error_language.update()
            else:
                async with aiofiles.open('config/user_settings.json', mode='r') as file:
                    data = json.loads(await file.read())
                data['system_language'] = self.language_selects.value
                async with aiofiles.open('config/user_settings.json', mode='w') as file:
                    await file.write(json.dumps(data, indent=4))
                page.update()
                self.error_language.color = 'green'
                self.error_language.value = 'Успешно обновлено'
                self.error_language.update()
                await asyncio.sleep(5)
                self.error_language.value = ''
                self.error_language.update()

        async def language_submit(self):
            return ft.ElevatedButton(text="Выбрать", on_click=self.language_select)

    language_selection = Language_selection()

    content = ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Настройки", size=30),
                    ft.IconButton(icon=ft.icons.SETTINGS_ROUNDED,
                                  icon_size=30, disabled=True),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(width=15),

            ft.Row(width=5),

            # Выбор языка приложения из выподающей меню
            ft.ResponsiveRow(
                [
                    language_selection.language_selects,
                    language_selection.error_language,
                    await language_selection.language_submit(),
                ]
            ),

            ft.Row(width=5),

            # Синхронизация
            ft.ResponsiveRow(
                [
                    ft.ElevatedButton("Синхронизация", on_click=check_update)
                ]
            ),

            ft.Row(width=5),

            # Проверка обновления приложения
            ft.ResponsiveRow(
                [
                    ft.ElevatedButton(
                        "Проверить наличие обновлений", on_click=check_update, icon_color="green")
                ]
            ),

        ]

    )

    return content
