@ECHO OFF
pyinstaller uninstaller.py --onefile -i .\icons\filemgmt_236.ico --uac-admin
rmdir build /s /q
pause
exit