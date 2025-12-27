import sys 
import time
import threading

import cv2
import flet as ft
import numpy as np

def wait(second: float, stop_event: threading.Event = None, control: ft.Control = None, message: str = "等待中"):
    s = int(second)
    ms = second - s

    for i in range(s):
        if stop_event is not None and stop_event.is_set():
            if message is not None:
                print("\r等待中... 已停止" + " " * 10)
            if control is not None:
                control.value = f""
                control.update()
            return
        if message is not None:
            print(f"\r{message}... {i+1}/{second}" + " " * 10, end="")
        if control is not None:
            control.value = f"等待中...\n{round(float(i+1), 2)}/{round(float(second), 2)}"
            control.update()
        time.sleep(1)

    if ms > 1E-8:
        if message is not None:
            print(f"\r{message}... {second}/{second}" + " " * 10, end="")
        if control is not None:
            control.value = f"等待中...\n{round(float(second), 2)}/{round(float(second), 2)}"
            control.update()
        time.sleep(ms)

def is_image_similar(img1: np.ndarray, img2: np.ndarray):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    mse = np.mean((gray1 - gray2) ** 2)

    print("MSE Score:", mse)
    return mse < 18

def is_template_in_image(big_img, small_img, threshold: float = 0.5) -> bool:
    img = cv2.imread(big_img)
    template = cv2.imread(small_img)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= threshold)

    return bool(loc[0].size)