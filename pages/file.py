import flet as ft
import json

from storage.data import items, table_data
from storage.data import pastel_index, parent_color, pastel_rainbow

file_name = None

def FilePage(page: ft.Page):
    save_bar = ft.SnackBar(
        content=ft.Text("儲存成功"),
        action="ok",
    )
    not_save_bar = ft.SnackBar(
        content=ft.Text("儲存失敗", color=ft.Colors.RED_200),
        action="ok",
    )
    input_bar = ft.SnackBar(
        content=ft.Text("匯入成功"),
        action="ok",
    ) 
    not_input_bar = ft.SnackBar(
        content=ft.Text("匯入失敗", color=ft.Colors.RED_200),
        action="ok",
    ) 

    def change_input_file_name(e: ft.ControlEvent):
        global file_name
        file_name = e.data

    file_input = ft.TextField(label="輸入檔案名稱", on_change= change_input_file_name)

    def handle_close(e: ft.ControlEvent):
        global file_name
        page.close(dlg_modal)

        if e.control.data == "save" and file_name:
            data = dict()
            data["points"] = [{"name": name, "x": x, "y": y} for name, x, y in table_data]
            data["workflow"] = items

            with open(f"{file_name}.json", "w") as f:
                json.dump(data, f)

            page.open(save_bar)
        else:
            page.open(not_save_bar)

        file_name = ""
        file_input.value = ""


    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=file_input,
        actions=[
            ft.TextButton("確定", on_click= handle_close, data="save"),
            ft.TextButton("取消", on_click=handle_close),
        ],
    )

    def pick_file_result(e: ft.ControlEvent):
        global table_data, items, pastel_index, parent_color, pastel_rainbow
        file_name = e.files[0].name if e.files else None
        if file_name:
            with open(file_name, "r") as f:
                j = json.load(f)
                points = j["points"]
                data = [[p["name"], int(p["x"]), int(p["y"])] for p in points]
                table_data.clear()
                table_data.extend(data)

                workflow = j["workflow"]
                for work in workflow:
                    if work["type"] in ["similar", "template"]:
                        parent_color[work["uuid"]] = pastel_rainbow[pastel_index]
                        pastel_index = (pastel_index + 1) % len(pastel_rainbow)
                items.clear()
                items.extend(workflow)

            page.open(input_bar)

        else:
            page.open(not_input_bar)
            print("未選擇檔案")

    pick_files_dialog = ft.FilePicker(on_result=pick_file_result)

    def pick_file(e: ft.ControlEvent):
        pick_files_dialog.pick_files(allow_multiple=False, initial_directory=".")

    def save_file(e: ft.ControlEvent):
        page.open(dlg_modal)
        return
        data = dict()
        data["points"] = [{"name": name, "x": x, "y": y} for name, x, y in table_data]

        with open("points.json", "w") as f:
            json.dump(data, f)
        page.open(save_bar)



    return ft.Column(
        controls=[
            ft.Container(
                content= ft.Text("檔案處理", color="gray", size=20, weight=ft.FontWeight.BOLD),
                margin= 10
            ),
            ft.Divider(),
            ft.Container(
                content = ft.ElevatedButton("匯入檔案", ft.Icons.SAVE_ALT_OUTLINED, bgcolor="#f2e390", on_click=pick_file),
                margin = ft.Margin(0, 10, 0, 10)
            ),
            ft.ElevatedButton("匯出檔案", ft.Icons.FILE_UPLOAD_OUTLINED, bgcolor="#e0e0e0", on_click=save_file),
            pick_files_dialog,
            dlg_modal,
            not_save_bar,
            save_bar,
            input_bar,
            not_input_bar
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


