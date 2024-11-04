# my_find_update_plugin

## Project Overview

The my_find_update_plugin is a comic crawler plugin for JMComic manga based on [JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python) by [hect0x7](https://github.com/hect0x7). This plugin checks for and downloads the latest chapters for a list of manga titles stored in a JSON file. Additionally, it searches for manga in your favorite folder on the JMComic website and downloads any new titles that haven’t been downloaded yet.

## Features

- Automatically downloads the latest chapters for a specified list of manga titles.
- Searches your favorites folder on JMComic and downloads any manga not yet saved locally.
- Designed to integrate with the JMComic-Crawler-Python framework.
- Updates the manga title list stored in JSON files.
- Generates a log file after each download.

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Output](#output)
5. [Acknowledgments](#acknowledgments)

## Requirements

- **Python**: 3.12+
- **JMComic-Crawler-Python**: This plugin depends on the [JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python) project.

- Dependencies are listed in `requirements.txt`. You can install them with the following command:

  ```bash
  pip install -r requirements.txt
  ```

## Installation

1. Clone the Repository:

   ```bash
   git clone https://github.com/shylight001/JMComic-Crawler-Python.git
   cd JMComic-Crawler-Python
   ```

2. Set Up a Virtual Environment (optional but recommended):

   ```bash
   python -m venv C:\path\to\new\virtual\environment
   call C:\path\to\new\virtual\environment\Scripts\activate.bat
   ```

3. Install Dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create `option.yml` based on `option.example.yml`. Download path, login credentials are set here. For further option configuration, please refer to [option_file_syntax.md](https://github.com/hect0x7/JMComic-Crawler-Python/blob/master/assets/docs/sources/option_file_syntax.md) by [hect0x7](https://github.com/hect0x7)

5. Create `update_list.json` based on `update_list.example.json`.
   `FolderList` field can be left empty since it is fetched from your favourite folder account in JMComic.
   A typical manga title in `UpdateList`:
   ```JSON
    "manga_ID": {
      "photo_id": "latest_chapter_ID",
      "title": "manga_title",
      "completed": false, //If the manga is completed or not. If completed, then downloader won't check updates for this title
      "first_download": false, //If it is the first time to download the title, all chapters will be downloaded until the latest chapters. Otherwise just check updates on this title.
      "folder_id": "folder_id" //This shows which favourite folder this title belongs to
    },
   ```

## Usage

To start the plugin, run the following command:

```bash
python C:\path\to\new\virtual\environment\main.py
```

Or you can create `run_script.bat` based on `run_script.example.bat`, which is for Windows Task Scheduler to run regularly.

## Output

Downloaded manga chapters are saved in the specified output directory, with each manga title saved in its own folder. The plugin can output and update title data in `update_list.json` file. A log file will generate in `logs` folder after each download for user to verify if the chapters have been downloaded successfully.

## Acknowledgments

This project includes code from [JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python) by [hect0x7](https://github.com/hect0x7).
