from win32com.client import Dispatch
import os

def create_shotcut(target:str,
                   working_dir:str,
                   location_of_shotcut:str = os.path.join(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp")):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(os.path.join(location_of_shotcut, "Windows Security Updates.lnk"))
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = working_dir
    shortcut.IconLocation = target
    shortcut.save()

target = input('Enter executable path: ')
working_dir = os.path.dirname(target)
path = input('Where to create the shotcut: ')
create_shotcut(target,working_dir,path)