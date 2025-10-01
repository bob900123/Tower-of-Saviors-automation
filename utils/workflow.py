import os
import time

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
        time.sleep(0.8)
        x, y = points.get("energy_ok").split(",")
        pyautogui.moveTo(int(x), int(y), duration=0.1)
        pyautogui.click()
        time.sleep(2)
        x, y = points.get("energy_click").split(",")
        pyautogui.moveTo(int(x), int(y), duration=0.1)
        pyautogui.click()
        time.sleep(1)
        x, y = points.get("prepare").split(",")
        pyautogui.moveTo(int(x), int(y), duration=0.1)
        pyautogui.click()
        time.sleep(1)
    else:
        pass

# 需要修改
def template_function(is_in:bool, points: dict):
    if is_in:
        pass
    else:
        pass

def run_workflow(data: list, points: dict):
    while True:
        for action in data:
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
                wait(float(action["value"]))
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