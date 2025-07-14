import keyboard
import threading
import flet as ft
import pyautogui
import uuid

def listen_keyboard(page: ft.Page, data: list, stop_event: threading.Event):
    rlock = threading.RLock()
    point_idx = 0

    def on_key_press(event: keyboard.KeyboardEvent):
        nonlocal point_idx
        if event.name == "w":
            with rlock:
                point_idx += 1
                point = pyautogui.position()
                data.append([f"point_{point_idx}", str(point.x), str(point.y)])
            page.go(f"/points?refresh={uuid.uuid4()}")
            
    keyboard.on_press(on_key_press)
    while not stop_event.is_set():
        pass