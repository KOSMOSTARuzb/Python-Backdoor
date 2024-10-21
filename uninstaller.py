print("start")

import ctypes
import os
import time
import winreg
import sys

print("Everything imported.\ndefining functions")

winpath = os.environ.get("SystemRoot")

def is_installed():
    path_of_luck = os.path.join(winpath,"Systematic Luck.bak")
    if not os.path.exists(path_of_luck):
        print("Fresh installation")
        
        return False
    print("Reading luck...")
    file = open(path_of_luck,'r')
    path_readed = file.read().strip()
    file.close()
    print("Path:",path_readed)
    splitted = path_readed.split('\\')
    print("Splitted")
    temp = str(splitted[0])
    for i in range(1,len(splitted)-1):
        temp = os.path.join(temp,str(splitted[i]))
    print("temp:",temp)
    exec_name=path_readed.split('\\')[-1][:-4]
    print("Executable detected:", exec_name)
    del_reg(exec_name)
    print("Stopping process...")
    os.system('TASKKILL /F /IM "'+exec_name+'.exe" /T')
    os.system("del \""+path_of_luck+'"')
    os.system("del \""+path_readed+'"')
    os.system("del \"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\Windows Security Updates.lnk\"")
    print(temp)
    os.system("rmdir "+temp+" /s /q")
    print('\nExiting...\n\n\n')
def del_reg(name:str,REG_PATH:str=r'Software\Microsoft\Windows\CurrentVersion\Run')->bool:
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,  winreg.KEY_WRITE)
        winreg.DeleteValue(registry_key, name)
        winreg.CloseKey(registry_key)
        return True
    except:
        return False

print("Checking admin privilages...")
is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
if is_admin:
    try:
        print("\n\nIs admin.\n\n\n\n")
        is_installed()
    except Exception as e:
        print(e)
    os.system("pause")
else:
    print('\n'*100,"NOT ADMIN")
    print('\n'*5)
    t_end = time.time_ns()/1000000 + 3000
    while True:
        t_remaining = round(t_end - time.time_ns()/1000000,2)
        if t_remaining<0:
            sys.exit(1223)
        print(f"Waiting {t_remaining}ms before exiting"+'['+int(t_remaining/100)*'.'+(15-int(t_remaining/100))*' '+']',end='\r')
        time.sleep(0.1)