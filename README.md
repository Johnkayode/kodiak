# Kodiak

Easily convert Excel/CSV data to JSON format. 


![](https://github.com/Johnkayode/kodiak/blob/main/assets/kodiak.gif)

## Features
- Convert Excel (.xls, .xlsx) files to JSON format
- Convert CSV (.csv) files to JSON format

## Installation
To install Kodiak, download the latest version for your operating system. It is available on Mac, Windows, and Linux.
Install the `.exe`, `.deb` and `.dmg` files for Windows, Linux and Mac OSes respectively.

## How To Use
- Select the source file format (Excel/CSV).
- Check the `Header` button if the first row of the data should be set as header.
- Select the source file from the file dialog.
- Copy or download the JSON data.

## Build/Run
To build or run `Kodiak` locally on your machine, first install [Python](https://www.python.org/downloads/).  

Then:
1. Clone the repository  

    ```shell
    git clone https://github.com/Johnkayode/kodiak
    ```
2. Install dependencies  

    ```shell
    pip install -r requirements.txt
    ```
3. Run the app  

    ```shell
    python main.py
    ```  

   or build the app  

    ```shell
    pyinstaller --name "kodiak" --onefile --windowed --icon=assets/kodiak.ico --noconfirm main.py
    ```
