@echo off
echo Building Loqui executable...

:: Install requirements just in case
.venv\Scripts\python.exe -m pip install -r requirements.txt

:: Build the executable
:: We use a directory build rather than onefile because large AI libraries (like PyTorch)
:: take too long to unpack into temp folders on every startup with --onefile.
.venv\Scripts\python.exe -m PyInstaller -y --noconsole --name Loqui --collect-all plyer --collect-data faster_whisper --add-data "config.yaml;." main.py

:: Copy config.yaml next to the executable for easy user modification
copy config.yaml dist\Loqui\config.yaml

echo.
echo Build complete! 
echo The executable is located in the "dist\Loqui" folder.
echo You can zip the "Loqui" folder and deploy it to other laptops.
