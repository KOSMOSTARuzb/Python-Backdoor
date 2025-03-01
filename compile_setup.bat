@ECHO OFF
pyinstaller main.py --onefile --noconsole -i .\icons\filemgmt_236.ico
pyinstaller setup.py --onefile -i .\icons\filemgmt_236.ico --add-data .\dist\main.exe:. --uac-admin
pause
exit