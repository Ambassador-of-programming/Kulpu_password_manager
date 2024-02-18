import flet as ft
import asyncio
import aiofiles
import json

async def settings_view(page: ft.Page):
    async def toggle_dark_mode(event):
        if page.theme_mode == "dark":
            page.theme_mode = "light"
            await page.update_async()
        else: 
            page.theme_mode = "dark"
            await page.update_async()

    async def check_update(event):
        return await page.go_async('/settings/update')
    
    class EditResizeScale:
        def __init__(self) -> None:
            self.scale_textfield = ft.TextField(label="Изменить маштаб", hint_text="Пример: 1 или 0.1")
            self.scale_error = None

        async def resize_scale(self):
            async with aiofiles.open('config/user_settings.json', mode='r') as file:
                data = json.loads(await file.read())
            return data['scale']
    
        async def __scale_update(self, event):
            async def convert_to_float_or_str(value):
                try:
                    result = float(value)
                    return result
                except ValueError:
                    return value
            
            async def scale_change_confirmations():
                async def change_confirmation(event):
                    if self.scale_textfield.value is not None and \
                        isinstance(await convert_to_float_or_str(self.scale_textfield.value), (int, float)):

                        async with aiofiles.open('config/user_settings.json', mode='r') as file:
                            data = json.loads(await file.read())
                        data['scale'] = await convert_to_float_or_str(self.scale_textfield.value.strip().replace(" ", ""))
                        async with aiofiles.open('config/user_settings.json', mode='w') as file:
                            await file.write(json.dumps(data, indent=4))

                        content.scale = await self.resize_scale()
                        await page.update_async()
                        await page.close_dialog_async()
                    else:
                        await page.close_dialog_async()

                async def dialog_dismissed(event):
                    content.scale = await self.resize_scale()
                    await page.update_async()
                    await page.close_dialog_async()
                    
                cupertino_alert_dialog = ft.CupertinoAlertDialog(
                    content=ft.Text("Вы хотите изменения маштаба?"),
                    actions=[
                        ft.CupertinoDialogAction(
                            text = 'Да',
                            is_destructive_action=True,
                            on_click=change_confirmation,
                            ),

                        ft.CupertinoDialogAction(
                            text = "Отмена",
                            on_click=dialog_dismissed,
                            ),
                        ],
                    )
                page.dialog = cupertino_alert_dialog
                cupertino_alert_dialog.open = True
                await page.update_async()
            
            if self.scale_textfield.value is not None and \
                isinstance(await convert_to_float_or_str(self.scale_textfield.value), (int, float)):
                    
                content.scale = await convert_to_float_or_str(self.scale_textfield.value.strip().replace(" ", ""))
                await page.update_async()
                await asyncio.sleep(2)
                await scale_change_confirmations()
            else:
                print("у вас не int или float")

        async def scale_button(self):
            button = ft.ElevatedButton(
                icon=ft.icons.UPDATE,
                text="Изменить маштаб",
                on_click=self.__scale_update,
            )

            return button
            
    # выбор языка приложения
    class Language_selection:
        def __init__(self) -> None:
            self.error_language = ft.Text(color='red')
            self.language_selects = ft.Dropdown(
                width = 280,
                label = 'Выберите язык приложения',
                options = [
                    ft.dropdown.Option("Russian"),      
                ]
            )

        async def language_select(self, event):
            if self.language_selects.value == None:
                self.error_language.color = 'red'
                self.error_language.value = "Нельзя выбрать пустое значение" 
                await self.error_language.update_async()
                await asyncio.sleep(5)
                self.error_language.value = ''
                await self.error_language.update_async()
            else:
                async with aiofiles.open('config/settings_secret.json', mode='r') as file:
                    data = json.loads(await file.read())
                data['system_language'] = self.language_selects.value
                async with aiofiles.open('config/settings_secret.json', mode='w') as file:
                    await file.write(json.dumps(data, indent=4))
                # page.update()
                self.error_language.color = 'green'
                self.error_language.value = 'Успешно обновлено'
                await self.error_language.update_async()
                await asyncio.sleep(5)
                self.error_language.value = ''
                await self.error_language.update_async()

        async def language_submit(self):
            return ft.ElevatedButton(text="Выбрать", icon=ft.icons.LANGUAGE, on_click=self.language_select)
    

    editresizescale = EditResizeScale()
    language_selection = Language_selection()

    content = ft.Column(
        [
            ft.ResponsiveRow(
            [
                ft.Text("Мои Настройки", size=30), 
                ft.IconButton(icon=ft.icons.SETTINGS_ROUNDED, icon_size=30),
            ], 
            alignment=ft.alignment.center,
            ),

            ft.ResponsiveRow(
                [
                    ft.CupertinoSwitch(
                        label="Светлый/темный режим",
                        value=True,
                        on_change=toggle_dark_mode,
                        thumb_color=ft.colors.GREEN,
                        active_color=ft.colors.BLACK,
                        track_color=ft.colors.WHITE,
                    ),
        

                ],
            ),

            ft.ResponsiveRow(
                [
                    ft.TextButton("Проверить наличие обновлений", icon=ft.icons.UPDATE, on_click=check_update, icon_color="green")
                ]
            ),

            # Изменить маштаб приложения 
            ft.ResponsiveRow(
                [
                    editresizescale.scale_textfield,
                    await editresizescale.scale_button()
                ]
            ),
            
            # Выбор языка приложения из выподающей меню
            ft.ResponsiveRow(
                [
                    language_selection.language_selects,
                    language_selection.error_language,
                    await language_selection.language_submit(),
                ]
            ),

        ]

    )
    
    
    return content