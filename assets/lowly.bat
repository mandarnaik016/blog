@echo off
setlocal enabledelayedexpansion

rem Prompt for the folder name
set /p folder="Enter the folder name (relative path): "

rem Set the quality and blur parameters
set quality=40
set blur=0x80

rem Change to the specified directory
cd "!folder!" || (
    echo Folder not found.
    exit /b
)

rem Create the 'lowly' folder if it doesn't exist
if not exist "lowly" (
    mkdir "lowly"
)

rem Loop through all .jpeg files in the specified directory
for %%f in (*.png) do (
    rem Extract the filename without the extension
    set filename=%%~nf
    rem Use the magick convert command to process the image and save it to 'lowly'
    magick "%%f" -quality !quality! -blur !blur! "lowly\!filename!.jpeg"
)

echo Processing complete. Output saved to 'lowly' folder.
pause
