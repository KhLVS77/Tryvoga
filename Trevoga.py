import json
import requests
import os
import time
import datetime
import socket

flag=0
Region='Харківська область' # область, яка цікавить...

def f():
#Перевірка наявності інтернету
   try:
        socket.gethostbyaddr('www.google.com')
   except socket.gaierror:
        return False
   return True

now = datetime.datetime.now()
MyText2="'Програму моніторингу тривоги, запущено..."+" "+str(now.strftime("%d.%m.%Y %H:%M:%S"))+"'"
Message2='notify-send "Інформація..." --urgency=normal '+MyText2
os.system(Message2)

inetYES=True
while True:
    print(f())
# Перевіряємо наявність інтернету. Якшо нема, то виводимо відповідне повідомлення, зупиняємося на хвилину, а потім починаємо цикл спочатку
    if f()==False:
        now = datetime.datetime.now()
        MyText="'Проблема з Інтернетом ..."+" "+str(now.strftime("%d.%m.%Y %H:%M:%S"))+"'"
        Message='notify-send "Інформація ..." --urgency=normal --icon=/usr/share/icons/gnome/48x48/status/network-wired-disconnected.png '+MyText
        os.system(Message)
        inetYES=False
        time.sleep(60)
        continue
    
    if inetYES==False:
        now = datetime.datetime.now()
        MyText="'Зв`язок відновлено !"+" "+str(now.strftime("%d.%m.%Y %H:%M:%S"))+"'"
        Message='notify-send "Інформація ..." --urgency=normal --icon=/usr/share/icons/gnome/48x48/status/network-idle.png '+MyText
        os.system(Message)
        inetYES=True
    
    response = 0
    now = datetime.datetime.now()
    response = requests.get("https://emapa.fra1.cdn.digitaloceanspaces.com/statuses.json")
    todos = json.loads(response.text)
    trevoga=todos['states'][Region]['enabled']
    print(str(response)+ " "+now.strftime("%d.%m.%Y %H:%M:%S")+" "+ str(trevoga))

    now = datetime.datetime.now()
    if (trevoga==True and flag==0):
        MyText="'Тривога !   Всі по норах !"+" "+str(now.strftime("%d.%m.%Y %H:%M:%S"))+"'"
        Message='notify-send "УВАГА !" --urgency=critical --icon=/usr/share/icons/gnome/48x48/status/software-update-urgent.png '+MyText
        os.system(Message)
        flag=1
    
    if (trevoga==False and flag==1):
        MyText="'Все.   Можна вилазити з нори."+" "+str(now.strftime("%d.%m.%Y %H:%M:%S"))+"'"
        Message='notify-send "ВІДБІЙ ТРИВОГИ !" --urgency=critical --icon=/usr/share/icons/gnome/48x48/emblems/emblem-default.png '+MyText
        flag=0
        os.system(Message)
    time.sleep(25)
