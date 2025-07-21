import flet as ft
import json
import aiofiles


async def main(page: ft.Page):
    async with aiofiles.open('src/config/user_settings.json', 'r') as file:
        data = json.loads(await file.read())
    language_system = data['system_language']

    if language_system == 'Russian':
        from system.ru.navigation.FletRouter import Router
        from system.ru.navigation.bar import bottomappbar, appbar

        page.title = f'Kulpu: менеджер паролей'
        page.theme_mode = "dark"
        page.scroll = 'HIDDEN'
        page.padding = 10

        page.bgcolor = None
        page.window.width = 390
        page.window.height = 700
        page.adaptive = True

        page.appbar = await appbar(page)
        page.bottom_appbar = await bottomappbar(page)

        myRouter = Router()
        await myRouter.init(page)
        page.on_route_change = myRouter.route_change
        page.add(
            myRouter.body
        )
        page.go('/')

ft.app(
    target=main,
    assets_dir="assets",
)
