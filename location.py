import pyautogui
import time

while True:
    time.sleep(3)
    x, y = pyautogui.position()
    print(f"({x}, {y})")
