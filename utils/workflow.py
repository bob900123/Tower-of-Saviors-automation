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
    if is_similar:
        pass
    else:
        pass

# 需要修改
def template_function(is_in:bool, points: dict):
    if is_in:
        pass
    else:
        pass

def run_workflow(data: list, points: dict):
    print(data)
    return
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
            wait(float(t["value"]))
        elif t == "similar":
            img1 = cv2.imread(t["file1"])
            img2 = cv2.imread(t["file2"])
            result = is_image_similar(img1, img2)
            similar_function(result, points)
        elif t == "template":
            template = cv2.imread(t["file1"])
            img = cv2.imread(t["file2"])
            result = is_template_in_image(img, template)
            template_function(result, points)