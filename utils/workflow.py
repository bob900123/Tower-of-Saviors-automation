import os
import time
import threading

from .utils import wait, is_image_similar, is_template_in_image
import pyautogui
import cv2

'''
points = {
    "point1": "1142,330",
    "point2": "12,20",
    ...
}
'''
# 需要修改
def similar_function(is_similar: bool, points: dict):
    print("相似度檢測結果:", is_similar)
    print(points)
    if is_similar:
        x, y = points.get("energy").split(",")
        pyautogui.moveTo(int(x), int(y), duration=0.1)
        pyautogui.click()
        wait(0.8)
        x, y = points.get("energy_ok").split(",")
        pyautogui.moveTo(int(x), int(y), duration=0.1)
        pyautogui.click()
        wait(2)
        x, y = points.get("energy_click").split(",")
        pyautogui.moveTo(int(x), int(y), duration=0.1)
        pyautogui.click()
        wait(1)
        x, y = points.get("prepare").split(",")
        pyautogui.moveTo(int(x), int(y), duration=0.1)
        pyautogui.click()
        wait(1)
    else:
        pass

# 需要修改
def template_function(is_in:bool, points: dict):
    if is_in:
        pass
    else:
        pass

def run_workflow(data: list, points: dict, controls: dict):
    def worker(stop_event: threading.Event = threading.Event()):
        while not stop_event.is_set():
            for action in data:
                if stop_event.is_set():
                    break
                uid = action["uuid"]
                tile = controls.get(uid)
                if tile:
                    tile.bgcolor = "#fff176" 
                    tile.update()

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
                    similar_function(result, points)
                elif t == "template":
                    template = cv2.imread(os.path.join(action["dir1"], action["file1"]))
                    img = cv2.imread(os.path.join(action["dir2"], action["file2"]))
                    result = is_template_in_image(img, template)
                    template_function(result, points)

                if tile:
                    tile.bgcolor = "#f8f9ff"
                    tile.update()
        print("工作流程已停止")

    stop_event = threading.Event()
    threading.Thread(target=worker, daemon=True, args=(stop_event,)).start()
    return stop_event
