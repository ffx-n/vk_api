import requests
from bs4 import BeautifulSoup as bs
import random
import time as t
import os
import datetime
from python_rucaptcha import ImageCaptcha, RuCaptchaControl, CallbackClient
RUCAPTCHA_KEY = "d9746b4d461fcd8eba406b099b7674de"
image_link = ""
headers = {'accept':'*/*',
           'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

messages = ['']
tokens = ['']
owner_ids=['']
owner_id =[]
a=0
key = ''

msg = open('messages.txt', encoding= "UTF-8")
lines1 = msg.readlines()
num_lines = sum(1 for line in open('messages.txt', encoding = "UTF-8"))
for i in range(0,num_lines):
    lines1[i]=lines1[i].strip()
    messages.append(lines1[i])
del messages[0]
'''
token = open('access_token.txt')
lines2 = token.readlines()
num_lines = sum(1 for line in open('access_token.txt'))
for i in range(0,num_lines):
    lines2[i]=lines2[i].strip()
    tokens.append(lines2[i])
del tokens[0]
#access_token = lines2[0]
'''
tokens.append(os.environ.get('token1'))

#tokens.append(os.environ.get('token2'))

del tokens[0]

f = open('groups.txt')
lines3 =f.readlines()
num_lines_groups = sum(1 for line in open('groups.txt'))
for i in range(0,num_lines_groups):
    lines3[i] = lines3[i].strip()
    owner_ids.append(lines3[i])
del owner_ids[0]

version = '5.101'

def check_balance(key):
    response = requests.post(f'https://rucaptcha.com/res.php?key={key}&action=getbalance')
    return response.text


def sendd_comment(num,access_token):
    global image_link
    response = requests.post(f'https://api.vk.com/method/wall.post?owner_id={owner_ids[num]}&from_group=0&message={messages[random.randint(0,len(messages)-1)]}&access_token={access_token}&v={version}')
    text = response.json()
    try:
        if len(text['response']) > 0:
            print(f'Отправил комментарий в группе - {owner_ids[num]}')
    except:
        print('Разгадываю капчу')
    balance = check_balance(RUCAPTCHA_KEY)
    if float(balance)>0:
        try:
            sid = text['error']['captcha_sid']
            image_link = text['error']['captcha_img']
            user_answer = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(captcha_link=image_link)
            if not user_answer['error']:
                # решение капчи
                key = user_answer['captchaSolve']
            elif user_answer['error']:
                # Тело ошибки, если есть
                print(user_answer['errorBody']['text'])
                print(user_answer['errorBody']['id'])
            response_second = requests.post(f'https://api.vk.com/method/wall.post?owner_id={owner_ids[num]}&from_group=0&message={messages[random.randint(0, len(messages) - 1)]}&captcha_sid={sid}&captcha_key={key}&access_token={access_token}&v={version}')
            otvet = response_second.json()
            if len(otvet['response'])>0:
                print(f'Отправил комментарий в группе - {owner_ids[num]}')
            #print(response_second.json())
        except:
            print('error! Возможно, группа не запрашивает капчу, либо закончились деньги')
            print(f'Отправил комментарий в группе - {owner_ids[num]}')
    else:
        print('Работа остановлена, т.к баланс ниже указанного')

def get_friends(token):
    try:
        item = requests.post(f'https://api.vk.com/method/friends.getRequests?offset=0&count=40&extended=0&need_mutual=0&&access_token={token}&v=5.101')
        ids = item.json()
        ids_dict = ids['response']['items']
        for i in range(0,len(ids_dict)):
            adding = requests.post(f'https://api.vk.com/method/friends.add?&user_id={ids_dict[i]}&access_token={token}&v=5.101')
            t.sleep(0.5)
            if adding.status_code==200:
                print(f'Добавил в друзья - {ids_dict[i]}')
    except:
        print('Добавить в друзья не удалось :(')

while True:
    print(tokens)
    balance = check_balance(RUCAPTCHA_KEY)
    for j in range(0,len(owner_ids)):
        for i in range(0,len(tokens)):
            get_friends(tokens[i])
        for i in range(0,len(tokens)):
            sendd_comment(j,tokens[i])
    print(f'Отдыхаю, чтобы не забанило')
    print(f'Баланс - {balance}')
    t.sleep(random.randint(60, 70))
