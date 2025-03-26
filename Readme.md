# VP-Bot

VP-Bot is an automated script designed to manage roles and applicants in a virtual environment. It uses OCR (Optical Character Recognition) to detect stale roles and performs automated actions such as approving applicants and dismissing stale roles.

## Features

- **Applicant Approval**: Automatically approves applicants from a list.
- **Automated Role Management**: Detects stale roles and dismisses them based on configurable thresholds.
- **Conquerors Buff Mode**: Enhanced mode with additional UI configurations.
- **Configurable Settings**: All settings are customizable via a YAML configuration file.

## Requirements

- Python 3.8 or higher
- Tesseract OCR installed version ([Download here](https://github.com/UB-Mannheim/tesseract/wiki)). Download the `tesseract-ocr-w64-setup-5.5.0.20241111.exe` file
- Required Python packages (see `requirements.txt`)
- Last war running on a PC. Can be the Last War PC Version ([Last War](https://www.lastwar.com/en/home.html)) or running via an emulator.

## Installation
Install dependencies:
    `pip install -r requirements.txt`

## Usage
Run the bot with the following command:
    `python3 bot.py`

### Optional Arguments
--c: Enable Conquerors Buff mode.
Example:
    `python3 bot.py --c`

## Configuration
The bot's behavior is controlled via the config.yml file. Before running the bot you will need to update the config.yml file based on your screens resolution and location/window size of the last war game.

The `pytesseract_path` is currently the default path but you may need to update it based on your machine

There is a `location.py` script that will print your mouse location every 3 seconds. You can use this to find the x,y coordinates for your screen and update the config.yml with the new coordinate.

The other values in `config.yml` can be also be updated to your requirements if necessary.

## Notes
- The `threshold_max` value in `config.yml` is used as a preventive measure incase the screenshot or OCR are not accurate. Once the bot has been running and you can see it is working correctly this number can be increased to your desired amount.
- The bot will save the screenshot every time it looks to remove stale roles. This can be used to make sure your height width and location of the time is accurate during setup.
- There is an `example.jpg` file, the screenshots should look similar to this. It should only be taking a screenshot of the time!
- The bot will only dismiss for the roles defined in `staleRoleCoordinates`. You can add or remove roles based on your requirements.
- The conquerors buff mode has not been tested
