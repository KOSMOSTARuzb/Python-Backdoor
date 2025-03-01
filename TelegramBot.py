import requests
import urllib.parse as kiij

readme='Telegram: @kosmostaruzb\nMore in github !!!'
def en(text:str) -> str: return kiij.quote_plus(text) #URL encoder
def report_bug(some_information):
    pass
class need_to_improve:pass
class Bot():
    def __init__(self,TOKEN_of_bot:str):
        self.tkn = TOKEN_of_bot
        self.url="https://api.telegram.org/bot"+TOKEN_of_bot
    def __str__(self):return str(requests.get(self.url+"/getMe").json())
    def update(self,offset:int=None,limit:int=100,timeout:int=0,allowed_updates:list=[]):
        method='getUpdates'
        url1=['limit','timeout']
        url2=[limit,timeout]
        url=self.url+'/'+method
        url2=list(map(str,url2))
        url2=list(map(en,url2))
        if offset != None:
            url1.append('offset')
            url2.append(offset)
        if allowed_updates != []:
            url1.append('allowed_updates')
            url2.append(allowed_updates)
        for i in range(len(url1)):
            if i==0:
                url+='?'
            else:
                url+='&'
            url+=(url1[i] + '=' + str(url2[i]))
        return requests.get(url).json()
    def me(self):
        return requests.get(self.url+"/getMe").json()
    def out(self):
        return requests.get(self.url+"/LogOut").json()
    def close(self):
        return requests.get(self.url+"/Close").json()
    def send(self,chat_id,text,parse_mode:str=None,entities:need_to_improve=None,disable_web_page_preview:bool=None,disable_notification:bool=None,protect_content:bool=None,reply_to_message_id:int=None,allow_sending_without_reply:bool=None,reply_markup=None):
        method='sendMessage'
        url1=['chat_id','text']
        url2=[chat_id,text]
        url=self.url+'/'+method
        url2=list(map(str,url2))
        url2=list(map(en,url2))
        if parse_mode != None:
            url1.append('parse_mode')
            url2.append(parse_mode)
        if entities != None:
            url1.append('entities')
            url2.append(entities)
        if disable_web_page_preview != None:
            url1.append('disable_web_page_preview')
            url2.append(disable_web_page_preview)
        if disable_notification != None:
            url1.append('disable_notification')
            url2.append(disable_notification)
        if protect_content != None:
            url1.append('protect_content')
            url2.append(protect_content)
        if reply_to_message_id != None:
            url1.append('reply_to_message_id')
            url2.append(reply_to_message_id)
        if allow_sending_without_reply != None:
            url1.append('allow_sending_without_reply')
            url2.append(allow_sending_without_reply)
        if reply_markup != None:
            url1.append('reply_markup')
            url2.append(reply_markup.get())
        for i in range(len(url1)):
            if i==0:
                url+='?'
            else:
                url+='&'
            url+=(url1[i] + '=' + str(url2[i]))
        return requests.get(url).json()
    def send_doc_upload(self,
                   chat_id:int,
                   doc_file_opened,
                   caption:str = None):
        tmp = {
                "chat_id":int(chat_id)
            }
        if caption:
            tmp['caption'] = str(caption)
        return requests.post(
            self.url+'/sendDocument', files={'document':doc_file_opened}, data=tmp).json()
    def send_photo_upload(self,
                   chat_id:int,
                   photo_file_opened,
                   caption:str = None):
        tmp = {
                "chat_id":int(chat_id)
            }
        if caption:
            tmp['caption'] = str(caption)
        return requests.post(
            self.url+'/sendPhoto', files={'photo':photo_file_opened}, data=tmp).json()
    def forward(self,chat_id,from_chat_id,message_id,disable_notification=None,protect_content=None):
        method='sendMessage'
        url1=['chat_id','from_chat_id','message_id']
        url2=[chat_id,from_chat_id,message_id]
        url=self.url+'/'+method
        url2=list(map(str,url2))
        url2=list(map(en,url2))
        if disable_notification != None:
            url1.append('disable_notification')
            url2.append(disable_notification)
        if protect_content != None:
            url1.append('protect_content')
            url2.append(protect_content)
        for i in range(len(url1)):
            if i==0:
                url+='?'
            else:
                url+='&'
            url+=(url1[i] + '=' + str(url2[i]))
        return requests.get(url).json()
    def copy(self,chat_id,from_chat_id,message_id,caption=None,parse_mode=None,caption_entities:need_to_improve=None,disable_notification:bool=None,protect_content:bool=None,reply_to_message_id=None,allow_sending_without_reply=None,reply_markup=None):
        method='copyMessage'
        url1=['chat_id','from_chat_id','message_id']
        url2=[chat_id,from_chat_id,message_id]
        url=self.url+'/'+method
        url2=list(map(str,url2))
        url2=list(map(en,url2))
        if disable_notification != None:
            url1.append('disable_notification')
            url2.append(disable_notification)
        if protect_content != None:
            url1.append('protect_content')
            url2.append(protect_content)
        for i in range(len(url1)):
            if i==0:
                url+='?'
            else:
                url+='&'
            url+=(url1[i] + '=' + str(url2[i]))
        return requests.get(url).json()
    def answer(self,callback_query_id,text=None,show_alert=None,url=None,cache_time=None):
        method='sendMessage'
        url1=['callback_query_id']
        url2=[callback_query_id]
        url=self.url+'/'+method
        url2=list(map(str,url2))
        url2=list(map(en,url2))
        if text != None:
            url1.append('text')
            url2.append(text)
        if show_alert != None:
            url1.append('show_alert')
            url2.append(show_alert)
        if cache_time != None:
            url1.append('cache_time')
            url2.append(cache_time)
        for i in range(len(url1)):
            if i==0:
                url+='?'
            else:
                url+='&'
            url+=(url1[i] + '=' + str(url2[i]))
        return requests.get(url).json()
    def delete(self,chat_id,message_id:int):
        return requests.get(f'{self.url}/deleteMessage?chat_id={chat_id}&message_id={message_id}').json()
    def edit(self,text,chat_id=None,message_id=None,inline_message_id=None,parse_mode=None,entities=need_to_improve,disable_web_page_preview=None,reply_markup=None):
        method='editMessage'
        url1=['text']
        url2=[text]
        url=self.url+'/'+method
        url2=list(map(str,url2))
        url2=list(map(en,url2))
        if parse_mode != None:
            url1.append('parse_mode')
            url2.append(parse_mode)
        if chat_id != None:
            url1.append('chat_id')
            url2.append(chat_id)
        if message_id != None:
            url1.append('message_id')
            url2.append(message_id)
        if inline_message_id != None:
            url1.append('inline_message_id')
            url2.append(inline_message_id)
        if entities != None:
            url1.append('entities')
            url2.append(entities)
        if disable_web_page_preview != None:
            url1.append('disable_web_page_preview')
            url2.append(disable_web_page_preview)
        if reply_markup != None:
            url1.append('reply_markup')
            url2.append(reply_markup.get())
        for i in range(len(url1)):
            if i==0:
                url+='?'
            else:
                url+='&'
            url+=(url1[i] + '=' + str(url2[i]))
        return requests.get(url).json()
    def sticker(self,chat_id,sticker,disable_notification=False,protect_content=False,reply_to_message_id=None,allow_sending_without_reply=None,reply_markup=None):
        method='sendSticker'
        url1=['chat_id',"sticker","disable_notification","protect_content"]
        url2=[chat_id,sticker,disable_notification,protect_content]
        url=self.url+'/'+method
        url2=list(map(str,url2))
        url2=list(map(en,url2))
        if reply_to_message_id != None:
            url1.append("reply_to_message_id")
            url2.append(reply_to_message_id)
        if allow_sending_without_reply != None:
            url1.append("allow_sending_without_reply")
            url2.append(allow_sending_without_reply)
        if reply_markup != None:
            url1.append("reply_markup")
            url2.append(reply_markup)
        for i in range(len(url1)):
            if i==0:
                url+='?'
            else:
                url+='&'
            url+=(url1[i] + '=' + str(url2[i]))
        return requests.get(url).json()
    def leave(self,chat_id):
        return requests.get(self.url+"/leavechat?chat_id="+str(chat_id)).json()
    def getFile(self,file_id:str):
        return requests.get(self.url+"/getFile?file_id="+str(file_id)).json()['result']
    def downloadFile(self, file_path:str) -> bytes:
        return requests.get(f'https://api.telegram.org/file/bot{self.tkn}/'+file_path, allow_redirects=True).content
class inlineButton():
    def __init__(self, text:str, url:str=None, callback_data:str=None, web_app:need_to_improve=None, login_url:need_to_improve=None, switch_inline_query:str=None, switch_inline_query_current_chat:str=None, callback_game:need_to_improve=None, pay:bool=None):
        self.main={"text":en(text)}
        if callback_data != None: self.main['callback_data'] = en(callback_data)
        if web_app != None: self.main['web_app'] = web_app
        if login_url != None: self.main['login_url'] = en(login_url)
        if url != None: self.main['url'] = en(url)
        if switch_inline_query != None: self.main['switch_inline_query'] = switch_inline_query
        if switch_inline_query_current_chat != None: self.main['switch_inline_query_current_chat'] = switch_inline_query_current_chat
        if callback_game != None: self.main['callback_game'] = callback_game
        if pay != None: self.main['pay'] = pay
    def get(self):return self.main
class inlineKBMarkup():
    def __init__(self,*list_of_list_of_inline_keyboard_buttons:list):
        self.main = []
        if list_of_list_of_inline_keyboard_buttons!=():
            for i in range(len(list_of_list_of_inline_keyboard_buttons[0])):
                self.main.append([])
                for l in list_of_list_of_inline_keyboard_buttons[0][i]:
                    self.main[i].append(l.get())
    def add(self,row:int=1,*keyboard_buttons:inlineButton) -> None:
        row-=1
        for i in keyboard_buttons:
            while row+1 > len(self.main):
                self.main.append([])
            self.main[row].append(i.get())
    def get(self):
        j=''
        for i in ("{'inline_keyboard':"+str(self.main)+'}'):
            if i=="'":
                j+='"'
            else:j+=i
        return j

#qwefeghg