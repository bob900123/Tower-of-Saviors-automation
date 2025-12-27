import os
import uuid
import json
import time

import flet as ft

from storage.data import items, table_data
from storage.data import pastel_rainbow, pastel_index, parent_color
from utils.workflow import run_workflow

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
        if not e.files: return
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

    def pick_file(e: ft.ControlEvent):
        nonlocal selected_control
        uid, index = e.control.data.split(",")
        selected_control = {"uuid": uid, "idx": index, "element": e.control}
        pick_files_dialog.pick_files(allow_multiple=False, initial_directory=".")

    pick_files_dialog = ft.FilePicker(on_result=pick_file_result)
    point_map = dict()

    def update_parent(e: ft.ControlEvent):
        item_uuids = [item["uuid"] for item in items]
        idx = item_uuids.index(e.control.data)
        
        if idx == 0:
            return
        
        parent_uuid = items[idx-1]["parent"]
        self_parent_uuid = items[idx]["parent"]

        if self_parent_uuid is not None:
            parent_uuid = None

            for i in range(idx+1, len(items)):
                if items[i]["parent"] == self_parent_uuid:
                    items[i]["parent"] = None
                    control_map[items[i]["uuid"]].bgcolor = None
                    control_map[items[i]["uuid"]].update()
                else:
                    break

        items[idx]["parent"] = parent_uuid
        e.control.bgcolor = parent_color.get(parent_uuid)
        e.control.update()

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
                    on_long_press=remove_item,
                    on_click=update_parent,
                    bgcolor=parent_color.get(item.get("parent")),
                    key=item["uuid"]
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
                    on_long_press=remove_item,
                    on_click=update_parent,
                    bgcolor=parent_color.get(item.get("parent")),
                    key=item["uuid"]
                )
            elif item["type"] == "drag":
                def change_first_value(e: ft.ControlEvent):
                    uuid = e.control.data
                    for i in items:
                        if i["uuid"] == uuid:
                            if i.get("value") is None:
                                i["value"] = [None, None]
                            i["value"][0] = e.data
                            break
                def change_second_value(e: ft.ControlEvent):
                    uuid = e.control.data
                    for i in items:
                        if i["uuid"] == uuid:
                            if i.get("value") is None:
                                i["value"] = [None, None]
                            i["value"][1] = e.data
                            break
                    print(items)
                point0, point1 = item["value"] if item.get("value") else [None, None]
                first_dropdown = ft.Dropdown(
                    width=120,
                    options=[ft.dropdown.Option(f"{name}") for name, x, y in table_data],
                    text_size=15,
                    border_width=0,
                    value= point0 if point0 else None,
                    data= item["uuid"],
                    on_change= change_first_value,
                )
                second_dropdown = ft.Dropdown(
                    width=120,
                    options=[ft.dropdown.Option(f"{name}") for name, x, y in table_data],
                    text_size=15,
                    border_width=0,
                    value= point1 if point1 else None,
                    data= item["uuid"],
                    on_change= change_second_value,
                )
                c = ft.Row([ ft.Text("拖曳"), ft.Column([first_dropdown, second_dropdown])])
                listtile = ft.ListTile(
                    title= c, 
                    leading=ft.Icon(ft.Icons.DONE_OUTLINED),
                    data=item["uuid"],
                    on_long_press=remove_item,
                    on_click=update_parent,
                    bgcolor=parent_color.get(item.get("parent")),
                    key=item["uuid"]
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
                    on_long_press=remove_item,
                    on_click=update_parent,
                    bgcolor=parent_color.get(item.get("parent")),
                    key=item["uuid"]
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
                    bgcolor=parent_color.get(item.get("parent")),
                    key=item["uuid"]
                )
            elif item["type"] == "not_similar":
                file_col = ft.Column([
                        ft.TextButton(item.get("file1") if item.get("file1") else "選擇檔案", on_click=pick_file, data=item["uuid"] + ",0"), 
                        ft.TextButton(item.get("file2") if item.get("file2") else "選擇檔案", on_click=pick_file, data=item["uuid"] + ",1"), 
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
                c = ft.Row([ ft.Text("相異"), file_col], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                listtile = ft.ListTile(
                    title= c, 
                    leading=ft.Icon(ft.Icons.SWAP_HORIZ),
                    data=item["uuid"],
                    on_long_press=remove_item,
                    bgcolor=parent_color.get(item.get("parent")),
                    key=item["uuid"]
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
                    on_long_press=remove_item,
                    bgcolor=parent_color.get(item.get("parent")),
                    key=item["uuid"]
                )
            elif item["type"] == "notify":
                def change_value(e: ft.ControlEvent):
                    uuid = e.control.data
                    for i in items:
                        if i["uuid"] == uuid:
                            i["value"] = e.data
                            break
                dropdown = ft.Dropdown(
                    width=120,
                    options=[ft.dropdown.Option(f"Pushover")],
                    text_size=15,
                    border_width=0,
                    value= item.get("value"),
                    data= item["uuid"],
                    on_change= change_value,
                )
                c = ft.Row([ ft.Text("通知"), dropdown])
                listtile = ft.ListTile(
                    title= c, 
                    leading=ft.Icon(ft.Icons.NOTIFICATIONS),
                    data=item["uuid"],
                    on_long_press=remove_item,
                    on_click=update_parent,
                    bgcolor=parent_color.get(item.get("parent")),
                    key=item["uuid"]
                )
            controls.append(listtile)
            control_map[item["uuid"]] = listtile
        list_view = ft.ReorderableListView(
            controls=controls,
            on_reorder=on_reorder,
            key="reorderable-list"
        )
        control_map["_list_view"] = list_view
        return list_view

    def on_reorder(e: ft.OnReorderEvent):
        item = items.pop(e.old_index)
        items.insert(e.new_index, item)
        refresh()

    def button_clicked(e: ft.ControlEvent):
        global pastel_index

        uuid_str = str(uuid.uuid4())
        parent = None
        if e.control.data in ["similar", "template", "not_similar"]:
            pastel_index = (pastel_index + 1) % len(pastel_rainbow)
            parent_color[uuid_str] = pastel_rainbow[pastel_index]
            parent = uuid_str
        items.append({"type": e.control.data, "uuid": uuid_str, "parent": parent})
        refresh()

    def refresh():  
        row.controls[0].controls[1] = build_lv()
        row.update()

    # 初始構建
    lv = build_lv()

    sleep_bar = ft.SnackBar(
        content=ft.Text(f"{sleep_num} 秒後開始執行"),
        duration=3000
    )
    
    def invoke_workflow(e: ft.ControlEvent):
        global stop_event, start
        if start:
            stop_event.set()
            start = False
            e.control.text = "執行"
            e.control.bgcolor = "#cc91bd"
            e.control.icon = ft.Icons.PLAY_ARROW_OUTLINED
            e.control.update()
            for item in items:
                control = control_map.get(item["uuid"])
                if control:
                    control.bgcolor = parent_color.get(item.get("parent"))
                    control.update()
            return
        
        start = True
        e.control.text = "停止"
        e.control.icon = ft.Icons.STOP_OUTLINED
        e.control.bgcolor = "#ff6f91"   
        e.control.disabled = True
        e.control.update()

        sleep_time = 3
        page.open(sleep_bar)

        for t in range(sleep_time, 0, -1):
            nonlocal sleep_num
            sleep_num = t
            sleep_bar.content.value = f"{sleep_num} 秒後開始執行" 
            sleep_bar.update() 
            page.update()
            time.sleep(1)
        for i in items:
            if i["type"] == "click" or i["type"] == "doubleclick":
                x, y = point_map[i["value"]].split(",")
                i["x"] = x
                i["y"] = y
            if i["type"] == "drag":
                if all(val is not None for val in i["value"]):
                    x0, y0 = point_map[i["value"][0]].split(",")
                    x1, y1 = point_map[i["value"][1]].split(",")
                    i["points"] = [x0, y0, x1, y1]
                else:
                    i["poins"] = None
        e.control.disabled = False
        e.control.update()
        stop_event = run_workflow(items, control_map, page, lv)

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
                    ft.ElevatedButton("點擊", ft.Icons.DONE_OUTLINED, bgcolor=ft.Colors.DEEP_ORANGE_100, on_click=button_clicked, data="click"),
                    ft.ElevatedButton("雙擊", ft.Icons.DONE_ALL_OUTLINED, bgcolor=ft.Colors.ORANGE_100, on_click=button_clicked, data="doubleclick"),
                    ft.ElevatedButton("拖曳", ft.Icons.FLIP_TO_FRONT, bgcolor=ft.Colors.AMBER_100, on_click=button_clicked, data="drag"),
                    ft.ElevatedButton("延遲", ft.Icons.BROWSE_GALLERY_OUTLINED, bgcolor=ft.Colors.YELLOW_100, on_click=button_clicked, data="delay"),
                    ft.ElevatedButton("相似", ft.Icons.FIBER_SMART_RECORD_OUTLINED, bgcolor=ft.Colors.LIGHT_GREEN_100, on_click=button_clicked, data="similar"),
                    ft.ElevatedButton("相異", ft.Icons.SWAP_HORIZ, bgcolor=ft.Colors.GREEN_100, on_click=button_clicked, data="not_similar"),
                    ft.ElevatedButton("匹配", ft.Icons.FIND_IN_PAGE_OUTLINED, bgcolor=ft.Colors.BLUE_100, on_click=button_clicked, data="template"),
                    ft.ElevatedButton("通知", ft.Icons.NOTIFICATIONS, bgcolor=ft.Colors.PURPLE_100, on_click=button_clicked, data="notify"),
                    ft.Divider(thickness=1),
                    ft.ElevatedButton("執行", ft.Icons.PLAY_ARROW_OUTLINED, bgcolor=ft.Colors.PINK_100, on_click=invoke_workflow),
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
            sleep_bar,
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )
    return row
