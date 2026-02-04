# Debt Management System

## Description
A professional debt management system built with Python and Tkinter. This application allows users to manage debts, track payments, and maintain records securely.

## Features
- Secure activation system
- Manage debts per person with dedicated views
- Add, pay, and delete debts for each individual
- Display total debt per person
- Persistent storage using JSON
- User-friendly GUI interface with multiple windows
- Supports Iraqi Dinar currency
- Arabic language support

## Installation
1. Ensure Python 3.x is installed on your system.
2. Tkinter is usually included with Python. If not, install it:
   - On Windows: Python installer includes it.
   - On Linux: `sudo apt-get install python3-tk`
   - On macOS: `brew install python-tk`
3. Download or clone this repository.
4. (Optional) Add an `icon.ico` file in the same directory for custom window icon.
5. Run the application: `python debt_management.py`

## Building Executable
To create a standalone executable:
1. Install PyInstaller: `pip install pyinstaller`
2. Ensure `icon.ico` is in the directory for the icon.
3. Run: `pyinstaller --onefile --noconsole --icon=icon.ico debt_management.py`
4. The executable will be in the `dist/` folder with embedded icon.
5. The activation file is stored in the user's AppData/Roaming folder for security.
6. To sell: Run the exe on the customer's PC, enter the activation code to activate it, then provide the activated exe to the customer.

## Usage
1. Launch the program.
2. Enter the activation code when prompted (default: "my sweet").
3. Use the GUI to add debts, make payments, or delete records.
4. Data is automatically saved to `debts.json`.

## License
Copyright (c) 2026 Anas Mohammed. All rights reserved.
This software is protected and may not be copied or distributed without permission.

## Contact
For inquiries or purchases, contact Anas Mohammed.