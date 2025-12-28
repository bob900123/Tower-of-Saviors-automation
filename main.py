import threading
import uuid
import dotenv

import flet as ft
from flet import ControlEvent

from pages.points import PointsPage, table_data
from pages.loop import LoopPage
from pages.file import FilePage
from utils.local_keyboard import listen_keyboard

dotenv.load_dotenv() 

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 500
    page.window.height = 700
    page.window.resizable = False

    page.window.prevent_close = True

    stop_event = threading.Event()
    page.run_thread(listen_keyboard, page, table_data, stop_event)

    def router(e: ControlEvent):
        if e.data == "0":
            page.go("/points")
        elif e.data == "1":
            page.go("/loop?" + str(uuid.uuid4())[:10])
        elif e.data == "2":
            page.go("/file?" + str(uuid.uuid4())[:10])
        

    def window_event(e: ft.WindowEvent):
        if e.data == "close":
            stop_event.set() 

            page.window.prevent_close = False
            page.window.on_event = None
            page.update()
            page.window.close()

    page.window.on_event = window_event

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=20,
        min_extended_width=20,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.CONTROL_POINT, 
                selected_icon=ft.Icons.CONTROL_POINT_DUPLICATE_OUTLINED, 
                label="位置",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.THREESIXTY),
                selected_icon=ft.Icon(ft.Icons.THREESIXTY_OUTLINED),
                label="迴圈",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.ATTACH_FILE),
                selected_icon=ft.Icon(ft.Icons.ATTACH_FILE_OUTLINED),
                label="檔案",
            ),
        ],
        on_change=router,
    )


    def route_change(e):
        page.views.clear()

        route = page.route 

        if route.startswith("/points"):
            r = ft.Row([rail, ft.VerticalDivider(width=1)], expand=True)
            r.controls.append(PointsPage(page))
            page.views.append(ft.View(route, [r]))

        elif route.startswith("/loop"):
            r = ft.Row([rail, ft.VerticalDivider(width=1)], expand=True)
            r.controls.append(LoopPage(page))
            page.views.append(ft.View(route, [r]))

        elif route.startswith("/file"):
            r = ft.Row([rail, ft.VerticalDivider(width=1)], expand=True)
            r.controls.append(FilePage(page))
            page.views.append(ft.View(route, [r]))

        else:
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Text("首頁", size=32),
                        ft.ElevatedButton("進入 Points 頁面", on_click=lambda e: page.go("/points")),
                        ft.ElevatedButton("進入 Loop 頁面", on_click=lambda e: page.go("/loop")),
                    ],
                )
            )

        page.update()


    page.on_route_change = route_change
    page.go("/points")

ft.app(main)


