import keyboard
import pyautogui

print("w : 顯示鼠標位置")
print("c : 截取整個螢幕")
print("q : 離開整個程式")

while True:
    if keyboard.is_pressed("w"):
        print(pyautogui.position())
    elif keyboard.is_pressed("c"):
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        print("截圖完成")
    elif keyboard.is_pressed("q"):
        print("bye ~")
        break
