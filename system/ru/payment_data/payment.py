import flet as ft

class DataTable:
    def __init__(self) -> None:
        self.table = ft.DataTable(
            vertical_lines=ft.border.BorderSide(1, "blue"),
            horizontal_lines=ft.border.BorderSide(1, "green"),
            heading_row_color=ft.colors.BLACK12,
            columns=[
                ft.DataColumn(ft.Text("№")),
                ft.DataColumn(ft.Text("Заголовок")),
                ft.DataColumn(ft.Text("Дата создания")),
            ])
        self.all_battom = ft.Row(controls=[
            ft.IconButton(icon=ft.icons.ARROW_CIRCLE_LEFT,),
            ft.IconButton(icon=ft.icons.ARROW_CIRCLE_RIGHT, ),
            ft.IconButton(icon=ft.icons.UPDATE, ),
            ], alignment=ft.MainAxisAlignment.END)

class TableListView:
    def __init__(self) -> None:
        pass

class AddPaymentData:
    def __init__(self) -> None:
        self.all_bottos_payment_data = ft.ResponsiveRow(controls=[
            ft.ElevatedButton(text='Добавить', on_click=None, col=6),
            ft.ElevatedButton(text='Изменить', on_click=None, col=6),
            ft.ElevatedButton(text='Удалить', on_click=None, col=6),
        ])

async def payment(page: ft.Page):
    datatable = DataTable()
    addpaymentdata = AddPaymentData()

    content = ft.Column(controls=[
        ft.Row(controls=[
            ft.Icon(name=ft.icons.PAYMENT, size=30, disabled=True),
            ft.Text(value="Платежные данные",size=30, text_align=ft.TextAlign.CENTER),
        ], alignment=ft.MainAxisAlignment.CENTER),

        # All buttons (add, modify and delete)
        addpaymentdata.all_bottos_payment_data,

        # Table display
        ft.ResponsiveRow(controls=[
            datatable.table
            ]),
        
        # Left, right, refresh buttons
        datatable.all_battom,
    ])
    return content