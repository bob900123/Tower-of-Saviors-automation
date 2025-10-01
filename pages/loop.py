import os
import uuid
import json
import time

import flet as ft

from .points import table_data
from utils.workflow import run_workflow

items = []
control_map = {}
stop_event = None
start = False

def LoopPage(page: ft.Page):
    selected_control = dict()
    sleep_num = 3
    show_text = ft.Text("", size=15, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_500)
    control_map["show_text"] = show_text

    def pick_file_result(e: ft.ControlEvent):
        nonlocal selected_control
        selected_control["element"].text = e.files[0].name
        selected_control["element"].update()
        for i in items:
            if i["uuid"] == selected_control["uuid"]:
                if selected_control["idx"] == "0":
                    dir_path, file_name = os.path.split(e.files[0].path)
                    i["file1"] = file_name
                    i["dir1"] = dir_path
                elif selected_control["idx"] == "1":
                    dir_path, file_name = os.path.split(e.files[0].path)
                    i["file2"] = file_name
                    i["dir2"] = dir_path

    def pick_file_result2(e: ft.ControlEvent):
        global items
        file_name = e.files[0].path
        if file_name:
            with open(file_name, "r") as f:
                workflow = json.load(f)["workflow"]
                items = workflow
                refresh()

    def pick_file(e: ft.ControlEvent):
        nonlocal selected_control
        uid, index = e.control.data.split(",")
        selected_control = {"uuid": uid, "idx": index, "element": e.control}
        pick_files_dialog.pick_files(allow_multiple=False, initial_directory=".")

    def pick_file2(e: ft.ControlEvent):
        pick_files_dialog2.pick_files(allow_multiple=False, initial_directory=".")

    pick_files_dialog = ft.FilePicker(on_result=pick_file_result)
    pick_files_dialog2 = ft.FilePicker(on_result=pick_file_result2)
    point_map = dict()

    def build_lv():
        nonlocal point_map
        def remove_item(e: ft.ControlEvent):
            uuid = e.control.data
            for idx, i in enumerate(items):
                if i["uuid"] == uuid:
                    items.pop(idx)
                    break
            refresh()
        controls = []
        point_map = {name: f"{x},{y}" for name, x, y in table_data}
        
        ft.TextField(label="", border_width=1, width=80, height=30, text_size=12),
        for idx, item in enumerate(items):
            if item["type"] == "click":
                def change_value(e: ft.ControlEvent):
                    uuid = e.control.data
                    for i in items:
                        if i["uuid"] == uuid:
                            i["value"] = e.data
                            break
                dropdown = ft.Dropdown(
                    width=120,
                    options=[ft.dropdown.Option(f"{name}") for name, x, y in table_data],
                    text_size=15,
                    border_width=0,
                    value= item.get("value"),
                    data= item["uuid"],
                    on_change= change_value,
                )
                c = ft.Row([ ft.Text("點擊"), dropdown])
                listtile = ft.ListTile(
                    title= c, 
                    leading=ft.Icon(ft.Icons.DONE_OUTLINED),
                    data=item["uuid"],
                    on_long_press=remove_item
                )
            elif item["type"] == "doubleclick":
                def change_value(e: ft.ControlEvent):
                    uuid = e.control.data
                    for i in items:
                        if i["uuid"] == uuid:
                            i["value"] = e.data
                            break
                dropdown = ft.Dropdown(
                    width=120,
                    options=[ft.dropdown.Option(f"{name}") for name, x, y in table_data],
                    text_size=15,
                    border_width=0,
                    value= item.get("value"),
                    data= item["uuid"],
                    on_change= change_value,
                )
                c = ft.Row([ ft.Text("雙擊"), dropdown])
                listtile = ft.ListTile(
                    title= c, 
                    leading=ft.Icon(ft.Icons.DONE_OUTLINED),
                    data=item["uuid"],
                    on_long_press=remove_item
                )
            elif item["type"] == "delay":
                def change_value(e: ft.ControlEvent):
                    uuid = e.control.data
                    for i in items:
                        if i["uuid"] == uuid:
                            i["value"] = e.data
                field = ft.TextField(
                    label="", 
                    border=ft.InputBorder.UNDERLINE, 
                    border_width=1, 
                    width=80, 
                    text_align=ft.TextAlign.CENTER,
                    on_change= change_value,
                    data = item["uuid"],
                    value= item.get("value")        
                )
                c = ft.Row([ ft.Text("延遲"), field, ft.Text("秒")])
                listtile = ft.ListTile(
                    title= c, 
                    leading=ft.Icon(ft.Icons.BROWSE_GALLERY_OUTLINED), 
                    data=item["uuid"],
                    on_long_press=remove_item
                )
            elif item["type"] == "similar":
                file_col = ft.Column([
                        ft.TextButton(item.get("file1") if item.get("file1") else "選擇檔案", on_click=pick_file, data=item["uuid"] + ",0"), 
                        ft.TextButton(item.get("file2") if item.get("file2") else "選擇檔案", on_click=pick_file, data=item["uuid"] + ",1"), 
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
                c = ft.Row([ ft.Text("相似"), file_col], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                listtile = ft.ListTile(
                    title= c, 
                    leading=ft.Icon(ft.Icons.FIBER_SMART_RECORD_OUTLINED),
                    data=item["uuid"],
                    on_long_press=remove_item,
                )
            elif item["type"] == "template":
                file_col = ft.Column([
                        ft.TextButton(item.get("file1") if item.get("file1") else "選擇模板", on_click=pick_file, data=item["uuid"] + ",0"), 
                        ft.TextButton(item.get("file2") if item.get("file2") else "選擇檔案", on_click=pick_file, data=item["uuid"] + ",1"), 
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
                c = ft.Row([ ft.Text("匹配"), file_col], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                listtile = ft.ListTile(
                    title= c, 
                    leading=ft.Icon(ft.Icons.FIND_IN_PAGE_OUTLINED),
                    data=item["uuid"],
                    on_long_press=remove_item
                )
            controls.append(listtile)
            control_map[item["uuid"]] = listtile
        return ft.ReorderableListView(
            controls=controls,
            on_reorder=on_reorder
        )

    def on_reorder(e: ft.OnReorderEvent):
        items.insert(e.new_index, items.pop(e.old_index))
        refresh()


    def button_clicked(e: ft.ControlEvent):
        items.append({"type": e.control.data, "uuid": str(uuid.uuid4())})
        refresh()

    def refresh():  
        row.controls[0].controls[1] = build_lv()
        row.update()

    # 初始構建
    lv = build_lv()

    save_bar = ft.SnackBar(
        content=ft.Text("儲存成功"),
        action="ok",
    )
    upload_bar = ft.SnackBar(
        content=ft.Text("上傳成功"),
        action="od"
    )

    sleep_bar = ft.SnackBar(
        content=ft.Text(f"{sleep_num} 秒後開始執行"),
        duration=1000
    )

    def save_workflow(e: ft.ControlEvent):
        with open("workflow.json", "w") as f:
            json.dump({"workflow": items}, f)
        page.open(save_bar)
    
    def invoke_workflow(e: ft.ControlEvent):
        global stop_event, start
        if start:
            stop_event.set()
            start = False
            e.control.text = "執行"
            e.control.bgcolor = "#cc91bd"
            e.control.icon = ft.Icons.PLAY_ARROW_OUTLINED
            e.control.update()
            for control in control_map.values():
                control.bgcolor = "#f8f9ff"
                control.update()
            return
        
        start = True
        e.control.text = "停止"
        e.control.icon = ft.Icons.STOP_OUTLINED
        e.control.bgcolor = "#ff6f91"   
        e.control.update()

        sleep_time = 3

        for t in range(sleep_time, 0, -1):
            nonlocal sleep_num
            sleep_num = t
            sleep_bar.content.value = f"{sleep_num} 秒後開始執行" 
            sleep_bar.update() 
            page.update()
            page.open(sleep_bar)
            page.update()
            time.sleep(1)
        for i in items:
            if i["type"] == "click" or i["type"] == "doubleclick":
                x, y = point_map[i["value"]].split(",")
                i["x"] = x
                i["y"] = y
        stop_event = run_workflow(items, point_map, control_map)

    

    row = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Text("腳本", color="gray", size=20, weight=ft.FontWeight.BOLD), 
                    lv 
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,  
                spacing=10,
                scroll="HIDDEN",
                width=260,
            ),
            ft.Column(
                controls=[ 
                    ft.ElevatedButton("點擊", ft.Icons.DONE_OUTLINED, bgcolor="#ffffff", on_click=button_clicked, data="click"),
                    ft.ElevatedButton("雙擊", ft.Icons.DONE_ALL_OUTLINED, bgcolor="#c0d7df", on_click=button_clicked, data="doubleclick"),
                    ft.ElevatedButton("延遲", ft.Icons.BROWSE_GALLERY_OUTLINED, bgcolor="#aeccd6", on_click=button_clicked, data="delay"),
                    ft.ElevatedButton("相似", ft.Icons.FIBER_SMART_RECORD_OUTLINED, bgcolor="#92bbc8", on_click=button_clicked, data="similar"),
                    ft.ElevatedButton("匹配", ft.Icons.FIND_IN_PAGE_OUTLINED, bgcolor="#77aabb", on_click=button_clicked, data="template"),
                    ft.Divider(thickness=1),
                    ft.ElevatedButton("匯入", ft.Icons.FILE_UPLOAD_OUTLINED, bgcolor="#ffffff", on_click=pick_file2),
                    ft.ElevatedButton("匯出", ft.Icons.SAVE_ALT_OUTLINED, bgcolor="#ffb6ed", on_click=save_workflow),
                    ft.Divider(thickness=1),
                    ft.ElevatedButton("執行", ft.Icons.PLAY_ARROW_OUTLINED, bgcolor="#cc91bd", on_click=invoke_workflow),
                    ft.Container(
                        content= show_text,
                        margin= ft.Margin(top=80, left=0, right=0, bottom=0)
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=100,
                alignment=ft.MainAxisAlignment.START,
                spacing=20
            ),
            pick_files_dialog,
            pick_files_dialog2,
            save_bar,
            upload_bar,
            sleep_bar,
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )
    return row
