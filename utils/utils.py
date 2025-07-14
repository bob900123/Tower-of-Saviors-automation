import time
import numpy as np
import cv2
import pyautogui

def wait(second: float, message: str = "等待中"):
    s = int(second)
    ms = second - s

    for i in range(s):
        if message is not None:
            print(f"\r{message}... {i+1}/{second}" + " " * 10, end="")
        time.sleep(1)

    if ms > 0:
        if message is not None:
            print(f"\r{message}... {second}/{second}" + " " * 10, end="")
    print("")

def is_image_similar(img1: np.ndarray, img2: np.ndarray):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    mse = np.mean((gray1 - gray2) ** 2)

    print("MSE Score:", mse)
    return mse < 10

def is_template_in_image(big_img, small_img, threshold: float = 0.5) -> bool:
    img = cv2.imread(big_img)
    template = cv2.imread(small_img)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= threshold)

    return bool(loc[0].size)