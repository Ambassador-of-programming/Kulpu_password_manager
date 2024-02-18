import flet as ft
from language_system.ru.add.add import add
from language_system.ru.index.index_main import index
from language_system.ru.settings.settings import settings_view
from language_system.ru.password_generator.pass_generator import generator_pass

class Router:
    async def init(self, page: ft.Page):
        self.routes = {
            '/': await index(page),
            '/add': await add(page),
            '/settings': await settings_view(page),
            '/password_generator': await generator_pass(page),
        }
        self.body = ft.Container()

    async def route_change(self, route):
        self.body.content = self.routes[route.route]
        await self.body.update_async()