# android-uiautomation-voidremote
Lightweight Android UI automation in Python using ADB + voidremote — launches apps, dumps UI hierarchy, and simulates taps/swipes/text without Appium.   android  python  adb  ui-automation  voidremote  uiautomator  test-automation  appium-alternative


# Android UI Automation with Python

Lightweight Android UI automation using **ADB + voidremote** — no Appium server required.

## Features
- Launch any installed app by package name
- Capture screenshots and UI hierarchy dumps (`uiautomator`)
- Locate elements by text, resource-id, or bounds
- Simulate taps, swipes, text input, and key events

## Tech stack
Python 3.12+ · voidremote · ADB (Android Platform Tools) · uiautomator

## Setup
```bash
python -m venv android-env
# Windows PowerShell
.\android-env\Scripts\Activate.ps1
pip install voidremote
