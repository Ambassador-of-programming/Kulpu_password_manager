import flet as ft

async def appbar(page: ft.Page) -> ft.AppBar:
    async def go_add(event):
        return await page.go_async('/add')
    
    async def go_home(event):
        return await page.go_async('/')
    
    async def go_settings(event):
        return await page.go_async('/settings')
    
    async def go_password_generator(event):
        return await page.go_async('/password_generator')
    
    async def go_categories(event):
        return
    
    async def go_notes(event):
        return
    
    async def go_statistics(event):
        return

    appbar = ft.BottomAppBar(
        bgcolor=ft.colors.TERTIARY_CONTAINER,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.HOME, icon_color=ft.colors.BLUE_200, on_click=go_home),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.FAVORITE_BORDER, icon_color=ft.colors.BLUE_200, on_click=go_settings),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.ADD, icon_color=ft.colors.BLUE_200, on_click=go_add),
                ft.Container(expand=True),
                ft.PopupMenuButton(
                    icon=ft.icons.MENU,
                    items=[
                        ft.PopupMenuItem(
                            text="Генератор паролей",
                            on_click=go_password_generator,
                        ),
                        ft.PopupMenuItem(
                            text="Категории", 
                            on_click=go_categories,
                        ),
                        ft.PopupMenuItem(
                            text="Заметки", 
                            on_click=go_notes,
                        ),
                        ft.PopupMenuItem(
                            text="Статистика", 
                            on_click=go_statistics,
                        ),
                    ],
                ),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.SETTINGS, icon_color=ft.colors.BLUE_200, on_click=go_settings),
                ft.Container(expand=True),
            ]
        ),
        height=65,

    )
    return appbar