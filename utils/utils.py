import sys 
import time
import threading
import os

import cv2
import flet as ft
import numpy as np
import requests

def wait(second: float, stop_event: threading.Event = None, control: ft.Control = None, message: str = "等待中"):
    s = int(second)
    ms = second - s

    for i in range(s):
        if stop_event is not None and stop_event.is_set():
            if message is not None:
                print("\n\033[32m等待中... \033[0m" + "已停止")
            if control is not None:
                control.value = f""
                control.update()
            return
        if message is not None:
            print(f"\r\033[32m{message}... \033[0m" + f"{i+1:.1f}/{second:.1f}" + "\t" * 3, end="")
        if control is not None:
            control.value = f"等待中...\n{round(float(i+1), 2)}/{round(float(second), 2)}"
            control.update()
        time.sleep(1)

    if ms > 1E-8:
        if message is not None:
            print(f"\r\033[32m{message}... \033[0m" + f"{second:.1f}/{second:.1f}" + "\t" * 3, end="")
        if control is not None:
            control.value = f"等待中...\n{round(float(second), 2)}/{round(float(second), 2)}"
            control.update()
        time.sleep(ms)

def mse_score(img1: np.ndarray, img2: np.ndarray):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    mse = np.mean((gray1 - gray2) ** 2)
    return mse

def is_image_similar(img1: np.ndarray, img2: np.ndarray, show: bool = True):
    mse = mse_score(img1, img2)
    result = mse < 18
    if show:
        print(f"\r\033[34m[相似]\033[0m" + f" 結果：{result}, mse score：{mse:.3f}")
    return result

def is_image_not_similar(img1: np.ndarray, img2: np.ndarray, show: bool = True):
    mse = mse_score(img1, img2)
    result = mse > 18
    if show:
        print(f"\r\033[94m[相異]\033[0m" + f" 結果：{result}, mse score：{mse:.3f}")
    return result

def is_template_in_image(big_img, small_img, threshold: float = 0.5) -> bool:
    img = cv2.imread(big_img)
    template = cv2.imread(small_img)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= threshold)

    return bool(loc[0].size)

def notify(app: str):
    if app == "Pushover":
        notify_pushover()
    elif app == "LINE":
        notify_line()
    elif app == "Telegram":
        notify_telegram()
    

def notify_pushover():
    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "title": "神魔之塔 Error",
            "message": "自動化錯誤",
            "priority": 1
        }
    )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Pushover HTTP error: {e}")
        print("回傳內容：", response.text)

def notify_line():
    pass

def notify_telegram():
    pass