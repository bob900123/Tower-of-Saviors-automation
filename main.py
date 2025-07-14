import time

import cv2
import numpy as np
import pyautogui

from utils.utils import is_image_similar, wait

# img1_bgr = cv2.imread("energy.png")  

# def main():
    # energy_points = [
    #     [949, 551],
    #     [834, 885]
    # ]

    # start_point = [1125, 967]
    # skill_points = [
    #     [1175, 301], 
    #     [837, 697],
    #     [801, 428], 
    #     [833, 812], 
    #     [891, 426],
    #     [835, 812],
    #     [1079, 445],
    #     [1166, 436],
    #     [933, 620],
    #     [840, 805],
    #     [990, 428]
    # ]
    # skill2_points = [
    #     [1178, 431],
    #     [837, 812]
    # ]
    # prepare_point = [1126, 927]

    # wait(1, "準備中...")
    # print("")

    # for i in range(200):
    #     print(f"第 {i + 1} 輪")
    #     s = time.time()
    #     # 開始
    #     x, y = start_point
    #     pyautogui.moveTo(x, y)
    #     pyautogui.doubleClick()

    #     # 等待進入關卡
    #     wait(10, "進入關卡")

    #     # 技能
    #     for point in skill_points:
    #         x, y = point

    #         if (x == 1166 and y == 436) or (x == 1079 and y == 445):
    #             wait(0.5, None)

    #         pyautogui.moveTo(x, y)
    #         pyautogui.doubleClick()
    #         wait(0.5, None)
        
    #     # 等待通過關卡
    #     wait(55, "通關中")

    #     # 等待 vistory
    #     wait(20, "勝利動畫")

    #     # 準備
    #     x, y = prepare_point
    #     pyautogui.moveTo(x, y)
    #     pyautogui.click()
    #     wait(1.5, None)

    #     # 補充能量
    #     img2 = pyautogui.screenshot()
    #     img2_np = np.array(img2)
    #     img2_bgr = cv2.cvtColor(img2_np, cv2.COLOR_RGB2BGR)
        
    #     if is_image_similar(img1_bgr, img2_bgr):
    #         for point in energy_points:
    #             x, y = point
    #             pyautogui.moveTo(x, y)
    #             pyautogui.doubleClick()
    #             wait(0.5, None)

    #         wait(1.5, None)
    #         pyautogui.doubleClick()
    #         wait(1, None)

    #         x, y = prepare_point
    #         pyautogui.moveTo(x, y)
    #         pyautogui.click()
    #         wait(1.5, None)

    #     e = time.time()
    #     print("每輪用時：", e - s, "\n")

import threading

import flet as ft
from flet import ControlEvent

from pages.points import PointsPage, table_data
from pages.loop import LoopPage
from utils.local_keyboard import listen_keyboard

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
            page.go("/loop")

    def window_event(e: ft.WindowEvent):
        if e.data == "close":
            stop_event.set() 

            page.window.prevent_close = False
            page.window.on_event = None
            page.update()
            page.window.close()

    page.window.on_event = window_event

    # def on_keyboard(e: ft.KeyboardEvent):
    #     nonlocal point_idx
    #     if e.key.lower() == "w" and page.route == "/points":
    #         point = pyautogui.position()
    #         table_data.append([f"point{point_idx}", str(point.x), str(point.y)])
    #         point_idx += 1
    #         route_change(None) 

    # page.on_keyboard_event = on_keyboard

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
        ],
        on_change=router,
    )


    def route_change(e):
        page.views.clear()  
        url = page.route.split("?")[0]
        if url == "/points":
            r = ft.Row([rail, ft.VerticalDivider(width=1)], expand=True)
            r.controls.append(PointsPage(page))
            page.views.append(
                ft.View("/points",[r])
            )
        elif url == "/loop":
            r = ft.Row([rail, ft.VerticalDivider(width=1)], expand=True)
            r.controls.append(LoopPage(page))
            page.views.append(
                ft.View("/loop",[r])
            )
        else:
            # 首頁
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


