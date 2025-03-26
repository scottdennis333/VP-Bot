import pyautogui
import time
import re
import pytesseract
import yaml
import argparse
import cv2
import numpy as np

# Load configuration from YAML file
with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

pytesseract.pytesseract.tesseract_cmd = config["pytesseract_path"]

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Auto-clicker script with optional Conquerors Buff mode.")
parser.add_argument("--c", action="store_true", help="Enable Conquerors Buff mode")
args = parser.parse_args()

# Determine which coordinate set to use
conquerorsBuff = args.c
coordinates = config["coordinates"]["conquerors" if conquerorsBuff else "default"]
staleRoleCoordinates = config["staleRoleCoordinates"]["conquerors" if conquerorsBuff else "default"]

# Extract config values
threshold_minutes = config["threshold_minutes"]
threshold_max = config["threshold_max"]

# Function to convert HH:mm:ss to total minutes
def time_to_minutes(time_str):
    hours, minutes, _ = map(int, time_str.split(":"))
    return hours * 60 + minutes

# Function to sanitize OCR text
def text_sanitization(time_str):
    if not time_str:
        return ""
    if time_str[:3].isdigit():
        time_str = time_str[1:]  # Remove extra leading digit
    parts = time_str.split(":")
    if len(parts) > 2 and len(parts[2]) > 2:
        parts[2] = parts[2][:2]  # Remove extra trailing digit
    return ":".join(parts)

# Function to remove stale roles
def remove_stale_roles(left, top, width, height, message, x, y):
    print(message)
    region = (left, top, width, height)
    # Capture the screen region
    screenshot = pyautogui.screenshot(region=region)

    # Convert from RGB to BGR (OpenCV format)
    screenshot_rgb  = cv2.cvtColor(np.array(screenshot) , cv2.COLOR_RGB2BGR)

    # Save the sharpened image
    cv2.imwrite(f"img_{message}.jpg", screenshot_rgb)

    # Define OCR configuration options
    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789:'

    # Get the raw text
    raw_text = pytesseract.image_to_string(screenshot_rgb, config=custom_config)
    print(raw_text)

    # Extract text
    text = text_sanitization(raw_text)
    print(text)

    # Use regular expression to find time strings in HH:mm:ss format
    pattern = r'\b\d{2}:\d{2}:\d{2}\b'
    matches = re.findall(pattern, text)

    if matches:
        total_minutes = time_to_minutes(matches[0])
        if threshold_minutes <= total_minutes <= threshold_max:
            print(f"{matches[0]} {message} is greater than {threshold_minutes} minutes.")
            pyautogui.click(x, y)
            time.sleep(0.6)
            pyautogui.click(*config["dismiss_button"])
            time.sleep(0.6)
            pyautogui.click(*config["confirm_dismiss_button"])
            time.sleep(0.6)
            pyautogui.click(*config["exit_button"])
            time.sleep(0.6)
        else:
            print(f"{message} is less than {threshold_minutes} minutes or greater than {threshold_max} minutes.")

# Function to refresh positions
def refresh_positions():
    pyautogui.click(*config["back_button"])
    time.sleep(1.3)
    pyautogui.click(*config["capitol_button"])
    time.sleep(1)

# Function to approve applicant list
def approve_applicant_list(x, y):
    pyautogui.click(x, y)
    time.sleep(0.65)
    pyautogui.click(*config["list_button"])
    time.sleep(0.65)

    for _ in range(config["scroll_limit"]):  # Simulate scrolls
        pyautogui.moveTo(*config["scroll_start"])
        pyautogui.mouseDown()
        pyautogui.moveTo(*config["scroll_end"], duration=0.18)
        pyautogui.mouseUp()
        time.sleep(0.15)

    for _ in range(config["approval_limit"]):  # Approve applicants
        pyautogui.click(*config["approve_button"])
        time.sleep(0.35)

    pyautogui.click(*config["exit_button"])
    time.sleep(0.35)
    pyautogui.click(*config["exit_button"])
    time.sleep(0.65)

    return True

# Main function
def main():
    print(f"Starting script... Conquerors Buff mode: {'Enabled' if conquerorsBuff else 'Disabled'}")

    time.sleep(5)  # Giving time to get screen ready
    i = 9

    while True:
        i += 1
        for x, y in coordinates:
            approve_applicant_list(x, y)

        if i % 5 == 0:
            refresh_positions()
            for left, top, width, height, message, x, y in staleRoleCoordinates:
                remove_stale_roles(left, top, width, height, message, x, y)

        time.sleep(4) # Giving time to stop the bot

if __name__ == "__main__":
    main()
