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

def run_workflow(data: list, controls: dict) -> threading.Event:
    def worker(stop_event: threading.Event = threading.Event()):
        parent_condition = {}

        while not stop_event.is_set():
            for action in data:
                if stop_event.is_set():
                    break
                uid = action["uuid"]
                tile = controls.get(uid)
                tile_bgcolor = tile.bgcolor
                if tile:
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

    stop_event = threading.Event()
    threading.Thread(target=worker, daemon=True, args=(stop_event,)).start()
    return stop_event
