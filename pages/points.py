import flet as ft

table_data = [
]

def PointsPage(page: ft.Page):
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("名稱")),
            ft.DataColumn(ft.Text("x"), numeric=True),
            ft.DataColumn(ft.Text("y"), numeric=True),
            ft.DataColumn(ft.Text("刪除")), 
        ],
        width=350,
    )

    def rebuild_table():
        table.rows.clear()
        for i, row in enumerate(table_data):
            cells = []
            for j, val in enumerate(row):
                txt = ft.Text(val)
                def make_on_tap(i=i, j=j, txt=txt):
                    def on_tap(e):
                        if j != 0: return
                        tf = ft.TextField(value=txt.value, autofocus=True, width=100)
                        def save(e2):
                            table_data[i][j] = tf.value
                            rebuild_table()
                            table.update()
                        tf.on_blur = save
                        tf.on_submit = save
                        cell.content = tf
                        cell.update()
                    cell = ft.DataCell(txt, on_tap=on_tap)
                    return cell
                cell = make_on_tap()
                cells.append(cell)

            def del_row_fn(e, idx=i):
                table_data.pop(idx)
                rebuild_table()
                table.update()
            cells.append(
                ft.DataCell(
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        tooltip="刪除此列",
                        on_click=del_row_fn,
                        icon_color="gray",
                    ),
                )
            )

            table.rows.append(ft.DataRow(cells=cells))
    rebuild_table()

    return ft.Column(
        controls=[
            ft.Container(
                content= ft.Text("按 w 鍵儲存位置", color="gray", size=20, weight=ft.FontWeight.BOLD),
                margin= 10
            ),
            ft.Column(
                controls=[table],
                height=550,
                scroll="ALWAYS"
            ),
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


