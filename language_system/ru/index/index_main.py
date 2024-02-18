import flet as ft
from config.database.db import DatabaseManager

async def index(page: ft.Page):
    class Sort:
        def __init__(self, table) -> None:
            self.dropdown = ft.Dropdown(
                label="Сортировка",
                border_radius=30,
                on_change=self.dropdown_click,
                # hint_text="Choose your favourite color?",
                options=[
                    ft.dropdown.Option("Новые"),
                    ft.dropdown.Option("Самые старые"),
                    ft.dropdown.Option("Последнее изменения"),
                    ft.dropdown.Option("Старые изменения"),
                    ft.dropdown.Option("Полностью заполненые"),
                ], 
                autofocus=True,
                col={"md": 4, "sm": 4}
                )
            self.table = table
            
            self.search = ft.IconButton(
                icon=ft.icons.SEARCH, 
                col={"md": 4, "sm": 4},
                on_click=self.search_click
                )
            
            self.search_text = ft.TextField(
                visible=False
                )
        async def dropdown_click(self, event):
            print(event.control.value)

        async def bottom_dropdown(self) -> ft.Dropdown:
            return self.dropdown
        
        async def search_click(self, event) -> ft.IconButton:
            if self.search_text.visible == False:
                self.search_text.visible = True
                self.search_text.label = 'Введите поиск'
                self.search_text.border_radius = 5
                self.search_text.max_length = 300
                self.search_text.prefix_icon = ft.icons.SEARCH_OUTLINED
                self.search_text.border_color = 'green'
                self.search_text.bgcolor = ft.colors.DEEP_PURPLE

                await self.search_text.update_async()
            else:
                self.search_text.visible = False
                await self.search_text.update_async()

        async def bottom_search(self) -> ft.IconButton:
            return self.search

    class DateTable:
        def __init__(self) -> None:
            self.table = ft.DataTable(
                vertical_lines=ft.border.BorderSide(1, "blue"),
                horizontal_lines=ft.border.BorderSide(1, "green"),
                heading_row_color=ft.colors.BLACK12,
                columns=[
                    ft.DataColumn(ft.Text("№")),
                    ft.DataColumn(ft.Text("Заголовок")),
                    ft.DataColumn(ft.Text("Дата создания")),
                ],
            )
            self.forward = ft.IconButton(icon=ft.icons.SKIP_NEXT, on_click=self.next_row)
            self.back = ft.IconButton(icon=ft.icons.SWIPE_LEFT_OUTLINED, on_click=self.prev_row)
            self.update = ft.IconButton(icon=ft.icons.UPDATE_OUTLINED, on_click=self.update_bottom)
            self.current_row = 0
            self.rows = []
        
        async def update_bottom(self, event):
            pass
            # await self.table.update_async()

        async def next_row(self, e):
            if self.current_row + 5 < len(self.rows):
                self.current_row += 5
                await self.update_table()
            await self.table.update_async()

        async def prev_row(self, e):
            if self.current_row - 5 >= 0:
                # есть данные для предыдущей страницы  
                self.current_row -= 5
                await self.update_table()
            await self.table.update_async()

        async def test(self, e):
            row = e.control  # получаем DataRow
            print(row.cells[0].content.value)
        
        async def update_table(self):
            # берем 2 записи из списка по текущему индексу
            rows_to_show = self.rows[self.current_row:self.current_row + 5]
            # устанавливаем их в таблицу 
            self.table.rows = rows_to_show
        
        async def fill_data(self):
            database = DatabaseManager()
        
            colonka = await database.read_records('id', 'title', 'creation_date')

            for i in colonka:
                batch = i
                row = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(value=batch[0])),
                    ft.DataCell(ft.Text(value=batch[1])),
                    ft.DataCell(ft.Text(value=batch[2])),
                ], on_select_changed=self.test)
                self.rows.append(row)
            await self.update_table()
    
    datatable = DateTable()
    await datatable.fill_data()
    sort = Sort(datatable.table)
    content = ft.Column(controls=[
        ft.Row(height=20),
        ft.Row(controls=[
            await sort.bottom_dropdown(),
            await sort.bottom_search()
        ], 
        run_spacing=0,

        alignment=ft.MainAxisAlignment.CENTER,
        
        ),
        ft.Row(controls=[
            sort.search_text
        ],
        alignment=ft.MainAxisAlignment.CENTER
        ),

        ft.ResponsiveRow(controls=[
            datatable.table
        ]),
        ft.Row(controls=[
            datatable.back,
            datatable.update,
            datatable.forward
        ],alignment=ft.MainAxisAlignment.END
        )
        

    ])

    return content