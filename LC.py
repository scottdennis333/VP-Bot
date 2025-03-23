import pyautogui
import time

while True:
    time.sleep(3)  # Adjust delay as needed
    x, y = pyautogui.position()
    print(f"({x}, {y})")