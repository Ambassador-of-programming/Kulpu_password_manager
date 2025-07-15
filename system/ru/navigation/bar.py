import flet as ft

async def bottomappbar(page: ft.Page) -> ft.AppBar:
    async def go_add(event):
        return page.go('/add')
    
    async def go_home(event):
        return page.go('/')
    
    async def go_settings(event):
        return page.go('/settings')

    bottomappbar = ft.BottomAppBar(
        bgcolor=ft.Colors.TERTIARY_CONTAINER,
        content=ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.HOME, icon_color=ft.Colors.BLUE_200, on_click=go_home),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.ADD, icon_color=ft.Colors.BLUE_200, on_click=go_add),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.SETTINGS, icon_color=ft.Colors.BLUE_200, on_click=go_settings),
                ft.Container(expand=True),
            ]
        ),
        height=65,
    )
    return bottomappbar

async def appbar(page: ft.Page) -> ft.CupertinoAppBar:

    async def go_slide_password_generator(event):
        return page.go('/password_generator')
    
    async def go_slide_payment_data(event):
        return page.go('/payment_data')
    
    async def go_slide_notes(event):
        return
    
    async def go_slide_statistics(event):
        return page.go('/statistik')
    
    async def theme_changed(event):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        page.update()


    appbar = ft.AppBar(
        leading= ft.PopupMenuButton(
            icon=ft.Icons.MENU,
            items=[
                ft.PopupMenuItem(
                    text="Генератор паролей",
                    on_click=go_slide_password_generator,
                ),
                ft.PopupMenuItem(
                    text="Платежные данные",
                    on_click=go_slide_payment_data,
                ),
                ft.PopupMenuItem(
                    text="Категории", 
                    on_click=go_slide_payment_data,
                ),
                ft.PopupMenuItem(
                    text="Заметки", 
                    on_click=go_slide_notes,
                ),
                ft.PopupMenuItem(
                    text="Статистика", 
                    on_click=go_slide_statistics,
                ),
            ],
        ),
        actions=[
            ft.Switch(on_change=theme_changed)

        ]
        
    )
    return appbar