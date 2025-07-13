import time

import cv2
import numpy as np
import pyautogui

from utils import is_image_similar, wait

img1_bgr = cv2.imread("energy.png")  

def main():
    energy_points = [
        [949, 551],
        [834, 885]
    ]

    start_point = [1125, 967]
    skill_points = [
        [1175, 301], 
        [837, 697],
        [801, 428], 
        [833, 812], 
        [891, 426],
        [835, 812],
        [1079, 445],
        [1166, 436],
        [933, 620],
        [840, 805],
        [990, 428]
    ]
    skill2_points = [
        [1178, 431],
        [837, 812]
    ]
    prepare_point = [1126, 927]

    wait(1, "準備中...")
    print("")

    for i in range(200):
        print(f"第 {i + 1} 輪")
        s = time.time()
        # 開始
        x, y = start_point
        pyautogui.moveTo(x, y)
        pyautogui.doubleClick()

        # 等待進入關卡
        wait(10, "進入關卡")

        # 技能
        for point in skill_points:
            x, y = point

            if (x == 1166 and y == 436) or (x == 1079 and y == 445):
                wait(0.5, None)

            pyautogui.moveTo(x, y)
            pyautogui.doubleClick()
            wait(0.5, None)
        
        # 等待通過關卡
        wait(55, "通關中")

        # 等待 vistory
        wait(20, "勝利動畫")

        # 準備
        x, y = prepare_point
        pyautogui.moveTo(x, y)
        pyautogui.click()
        wait(1.5, None)

        # 補充能量
        img2 = pyautogui.screenshot()
        img2_np = np.array(img2)
        img2_bgr = cv2.cvtColor(img2_np, cv2.COLOR_RGB2BGR)
        
        if is_image_similar(img1_bgr, img2_bgr):
            for point in energy_points:
                x, y = point
                pyautogui.moveTo(x, y)
                pyautogui.doubleClick()
                wait(0.5, None)

            wait(1.5, None)
            pyautogui.doubleClick()
            wait(1, None)

            x, y = prepare_point
            pyautogui.moveTo(x, y)
            pyautogui.click()
            wait(1.5, None)

        e = time.time()
        print("每輪用時：", e - s, "\n")


if __name__ == "__main__":
    main()
