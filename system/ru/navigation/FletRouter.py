import flet as ft
from system.ru.add.add import add
from system.ru.index.index_main import index
from system.ru.settings.settings import settings_view
from system.ru.password_generator.pass_generator import generator_pass
from system.ru.payment_data.payment import payment

class Router:
    async def init(self, page: ft.Page):
        self.routes = {
            '/': await index(page),
            '/add': await add(page),
            '/settings': await settings_view(page),
            '/password_generator': await generator_pass(page),
            '/payment_data': await payment(page),
        }
        self.body = ft.Container()

    async def route_change(self, route):
        self.body.content = self.routes[route.route]
        self.body.update()