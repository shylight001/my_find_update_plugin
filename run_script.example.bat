:: Disable command echoing for cleaner output.
@echo off

:: Change to the project directory.
cd path\to\your\venv

:: Activate the Python virtual environment.
call .\Scripts\activate.bat

:: Specify Python IO encoding.
set PYTHONIOENCODING=utf-8

:: ------------------ Date and Time Modifier ------------------------

:: THIS CODE WILL DISPLAY A 2-DIGIT TIMESTAMP FOR USE IN APPENDING FILENAMES

:: CREATE VARIABLE %TIMESTAMP%

for /f "tokens=1-8 delims=.:/-, " %%i in ('echo exit^|cmd /q /k"prompt $D $T"') do (
   for /f "tokens=2-4 skip=1 delims=/-,()" %%a in ('echo.^|date') do (
set dow=%%i
set %%a=%%j
set %%b=%%k
set %%c=%%l
set hh=%%m
set min=%%n
set sec=%%o
set hsec=%%p
)
)

:: ensure that hour is always 2 digits

if %hh%==0 set hh=00
if %hh%==1 set hh=01
if %hh%==2 set hh=02
if %hh%==3 set hh=03
if %hh%==4 set hh=04
if %hh%==5 set hh=05
if %hh%==6 set hh=06
if %hh%==7 set hh=07
if %hh%==8 set hh=08
if %hh%==9 set hh=09

:: assign timeStamp:
:: Add the date and time parameters as necessary - " yy-mm-dd-dow-min-sec-hsec "
:: Create a timestamp variable for the log filename.
set timeStamp=%yy%%mm%%dd%_%hh%-%min%-%sec%

:: Define the path for the log file with the timestamp.
set log_file=path\to\your\script\logs\update_%timestamp%.log

:: Run the Python script and redirect output to the log file.
python path\to\your\script\main.py > %log_file% 2>&1  

:: Deactivate the Python virtual environment.
deactivate