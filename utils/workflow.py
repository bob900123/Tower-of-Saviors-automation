import os
import time
import threading

from .utils import wait, is_image_similar, is_template_in_image
import pyautogui
import cv2
import flet as ft

'''
points = {
    "point1": "1142,330",
    "point2": "12,20",
    ...
}
'''

def run_workflow(data: list, controls: dict, page: ft.Page, lv: ft.ListView) -> threading.Event:
    stop_event = threading.Event()
    current_lv = lv

    def get_active_list_view():
        nonlocal current_lv
        candidate = current_lv
        if candidate is not None and getattr(candidate, "page", None):
            return candidate
        candidate = controls.get("_list_view")
        if candidate is not None and getattr(candidate, "page", None):
            current_lv = candidate
            return candidate
        return None

    def worker():
        parent_condition = {}

        while not stop_event.is_set():
            for action in data:
                if stop_event.is_set():
                    break
                uid = action["uuid"]
                tile = controls.get(uid)
                tile_bgcolor = tile.bgcolor if tile else None
                if tile:
                    list_view = get_active_list_view()
                    if list_view:
                        list_view.scroll_to(key=tile.key, duration=300)
                    tile.bgcolor = ft.Colors.PINK_100
                    tile.update()

                if not parent_condition.get(action["parent"], True):
                    if tile:
                        tile.bgcolor = tile_bgcolor
                        tile.update()
                    continue

                t = action["type"]
                if t == "click":
                    x, y = int(action["x"]), int(action["y"])
                    pyautogui.moveTo(x, y, duration=0.1)
                    pyautogui.click()
                elif t == "doubleclick":
                    x, y = int(action["x"]), int(action["y"])
                    pyautogui.moveTo(x, y, duration=0.1)
                    pyautogui.doubleClick()
                elif t == "delay":
                    wait(float(action["value"]), control=controls.get("show_text"), stop_event=stop_event)
                elif t == "similar":
                    if action["file1"] == "current.png":
                        screenshot = pyautogui.screenshot()
                        screenshot.save(r"D:\Python_Projects\Madhead\static\current.png")
                    img1 = cv2.imread(os.path.join(action["dir1"], action["file1"]))
                    img2 = cv2.imread(os.path.join(action["dir2"], action["file2"]))
                    result = is_image_similar(img1, img2)
                    parent_condition[uid] = result
                elif t == "template":
                    template = cv2.imread(os.path.join(action["dir1"], action["file1"]))
                    img = cv2.imread(os.path.join(action["dir2"], action["file2"]))
                    result = is_template_in_image(img, template)
                    parent_condition[uid] = result

                if tile:
                    tile.bgcolor = tile_bgcolor
                    tile.update()

        print("工作流程已停止")

    page.run_thread(worker)
    return stop_event

