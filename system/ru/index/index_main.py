import flet as ft
from config.database.db import Password_Database


async def index(page: ft.Page):
    class Sort:
        def __init__(self, table: ft.DataTable) -> None:
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
                icon=ft.Icons.SEARCH,
                col={"md": 4, "sm": 4},
                on_click=self.search_click
            )

            self.search_text = ft.TextField(
                visible=False
            )

        async def dropdown_click(self, event):
            pass
            # print(event.control.value)

        async def bottom_dropdown(self) -> ft.Dropdown:
            return self.dropdown

        async def search_click(self, event) -> ft.IconButton:
            if self.search_text.visible == False:
                self.search_text.visible = True
                self.search_text.label = 'Введите поиск'
                self.search_text.border_radius = 5
                self.search_text.max_length = 300
                self.search_text.prefix_icon = ft.Icons.SEARCH_OUTLINED
                self.search_text.border_color = 'green'
                self.search_text.bgcolor = ft.Colors.DEEP_PURPLE

                self.search_text.update()
            else:
                self.search_text.visible = False
                self.search_text.update()

        async def bottom_search(self) -> ft.IconButton:
            return self.search

    class DataTable:
        def __init__(self) -> None:
            self.table = ft.DataTable(
                vertical_lines=ft.border.BorderSide(1, "blue"),
                horizontal_lines=ft.border.BorderSide(1, "green"),
                heading_row_color=ft.Colors.BLACK12,
                columns=[
                    ft.DataColumn(ft.Text("№")),
                    ft.DataColumn(ft.Text("Заголовок")),
                    ft.DataColumn(ft.Text("Дата создания")),
                ],
            )
            self.all_battom = ft.Row(controls=[
                ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_LEFT,
                              on_click=self.next_row),
                ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_RIGHT,
                              on_click=self.prev_row),
                ft.IconButton(icon=ft.Icons.UPDATE,
                              on_click=self.update_bottom),
            ], alignment=ft.MainAxisAlignment.END)

            self.current_row = 0
            self.rows = []

        async def update_bottom(self, event):
            self.table.clean()
            self.rows.clear()

            await self.fill_data()
            self.table.update()

        async def prev_row(self, e):
            if self.current_row + 5 < len(self.rows):
                self.current_row += 5
                await self.update_table()
            self.table.update()

        async def next_row(self, e):
            if self.current_row - 5 >= 0:
                # есть данные для предыдущей страницы
                self.current_row -= 5
                await self.update_table()
            self.table.update()

        async def click_detal_page(self, e):
            row = e.control  # получаем DataRow

            await tablelistview.create_row(row.cells[0].content.value)
            tablelistview.list.update()

            self.table.visible = False
            self.table.update()

            self.all_battom.visible = False
            self.all_battom.update()

        async def update_table(self):
            # берем 2 записи из списка по текущему индексу
            rows_to_show = self.rows[self.current_row:self.current_row + 5]
            # устанавливаем их в таблицу
            self.table.rows = rows_to_show

        async def fill_data(self):
            database = Password_Database()
            colonka = await database.read_records('id', 'title', 'creation_date')

            for batch in colonka:
                row = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(value=batch[0])),
                    ft.DataCell(ft.Text(value=batch[1])),
                    ft.DataCell(ft.Text(value=batch[2].split('.')[0])),
                ], on_select_changed=self.click_detal_page)
                self.rows.append(row)
            await self.update_table()

    class TableListView:
        def __init__(self, table: DataTable) -> None:
            self.table = table
            self.list = ft.ListView(adaptive=True, visible=False)
            self.new_table = []
            self.new_rows = []
            self.rows = ft.DataRow(cells=[])
            self.back = ft.ElevatedButton(
                text="Назад", icon=ft.Icons.ARROW_LEFT_OUTLINED, on_click=self.back_click)

        async def create_row(self, id):
            self.new_table.clear()
            self.new_rows.clear()
            self.list.visible = True

            db = Password_Database()
            get_all_data_by_id = await db.get_all_data_by_id(id)

            for key, value in get_all_data_by_id.items():
                self.new_table.append(
                    ft.DataTable(
                        vertical_lines=ft.border.BorderSide(1, "blue"),
                        horizontal_lines=ft.border.BorderSide(1, "green"),
                        heading_row_color=ft.Colors.BLACK12,
                        columns=[ft.DataColumn(ft.Text(key))]))
                self.new_rows.append(ft.DataRow(
                    cells=[ft.DataCell(ft.Text(value, selectable=True))]))

            for index, v in enumerate(self.new_table):
                self.new_table[index].rows.append(self.new_rows[index])

            self.new_table.append(self.back)
            self.list.controls = self.new_table

        async def back_click(self, event):
            self.list.visible = False
            self.list.update()

            self.table.table.visible = True
            self.table.table.update()

            self.table.all_battom.visible = True
            self.table.all_battom.update()

    datatable = DataTable()
    await datatable.fill_data()

    tablelistview = TableListView(datatable)

    sort = Sort(datatable.table)
    content = ft.Column(controls=[
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
            tablelistview.list,
            datatable.table
        ]),
        # ft.ResponsiveRow(controls=[
        #     datatable.table
        # ]),

        datatable.all_battom,



    ])

    return content
