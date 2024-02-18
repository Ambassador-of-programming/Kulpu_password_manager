import flet as ft
import json
import aiofiles

async def main(page: ft.Page):
    async with aiofiles.open('config/user_settings.json', 'r') as file:
        data = json.loads(await file.read())
    language_system = data['system_language']

    if language_system == 'Russian':
        from language_system.ru.navigation.FletRouter import Router
        from language_system.ru.navigation.bar import appbar
        
        page.title = f'Кулпу: менеджер паролей'
        page.theme_mode = "dark"
        page.scroll = 'HIDDEN'
        page.padding = 10

        page.bgcolor = None
        page.window_width = 390
        page.window_height = 700
        page.bottom_appbar = await appbar(page)

        myRouter = Router()
        await myRouter.init(page)
        page.on_route_change = myRouter.route_change
        await page.add_async(
            myRouter.body
        )
        await page.go_async('/')
        
ft.app(
    target=main, 
    assets_dir="assets", 
)