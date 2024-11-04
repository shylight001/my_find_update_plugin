:: Disable command echoing for cleaner output.
@echo off

:: Change to the project directory.
cd path\to\your\venv

:: Activate the Python virtual environment.
call .\Scripts\activate.bat

:: Specify Python IO encoding.
set PYTHONIOENCODING=utf-16

:: Create a timestamp variable for the log filename.
set timestamp=%date:~-4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%

:: Define the path for the log file with the timestamp.
set log_file=path\to\your\script\logs\update_%timestamp%.log

:: Run the Python script and redirect output to the log file.
python path\to\your\script\main.py > %log_file% 2>&1  

:: Deactivate the Python virtual environment.
deactivate