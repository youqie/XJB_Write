from exchangelib import DELEGATE, IMPERSONATION, Message, Account, HTMLBody, Credentials, Configuration, NTLM, FaultTolerance, CalendarItem, EWSDateTime
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
from exchangelib.items import MeetingRequest, SEND_TO_ALL_AND_SAVE_COPY
from exchangelib.recurrence import Recurrence, WeeklyPattern
from exchangelib.fields import WEEK_DAY, MONDAY
from time import sleep
from datetime import timedelta, datetime
from threading import Thread
import requests

BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

credentials = Credentials(username='dfocuspace\\administrator', password='DfocuSpace@P20m9')
config = Configuration(retry_policy=FaultTolerance(max_wait=3600), server="192.168.10.118", credentials=credentials, auth_type=NTLM)

user_one = Account(primary_smtp_address='test_1@dfocuspace.com', credentials=credentials, autodiscover=False, config=config, access_type=DELEGATE)
r1 = Account(primary_smtp_address='testroom2@dfocuspace.com', credentials=credentials, autodiscover=False, config=config, access_type=DELEGATE)
r2 = Account(primary_smtp_address='testroom3@dfocuspace.com', credentials=credentials, autodiscover=False, config=config, access_type=DELEGATE)
r3 = Account(primary_smtp_address='testroom4@dfocuspace.com', credentials=credentials, autodiscover=False, config=config, access_type=DELEGATE)

# testroom3 -> 测试会议室1
# testroom2 -> 测试会议室2
# testroom4 -> 测试会议室3

room_list = ['testroom2@dfocuspace.com', 'testroom3@dfocuspace.com', 'testroom4@dfocuspace.com']
user_list = ['test_1@dfocuspace.com', 'test_2@dfocuspace.com', 'asliu@dfocuspace.com', 'wangyu@dfocuspace.com', 'vivili@dfocuspace.com', 'llzuo@dfocuspace.com']

item = CalendarItem(
    account = user_one,
    folder = user_one.calendar,
    start = user_one.default_timezone.localize(EWSDateTime(2021, 1, 25, 17, 00)),
    end = user_one.default_timezone.localize(EWSDateTime(2021, 1, 25, 18, 00)),
    location = "testroom2@dfocuspace.com",
    subject = "Meeting Test",
    body = "Test 1",
    required_attendees = room_list + user_list
)

def modify():
    import random
    attendee_number = random.randint(1, 6)
    print("修改会议")
    print("随机" + str(attendee_number) + "个参会人")
    attendee = random.sample(user_list, attendee_number)
    for item in user_one.calendar.all().order_by('-datetime_received')[:1]:
        # 打印信息
        print(item.subject)
        item.subject = "修改会议测试" + str(random.randint(100, 999))
        item.required_attendees = room_list + attendee
        item.save(send_meeting_invitations=SEND_TO_ALL_AND_SAVE_COPY)

def correction(room_mail):
    url = "http://192.168.10.135/apis/test/correction/" + room_mail + "/1611504000000/1611590399999"
    response = requests.get(url=url)

import time

def task1():
    print("Thread 1 start " + str(int(time.time()*1000)))
    correction(room_list[0])

def task2():
    print("Thread 2 start " + str(int(time.time()*1000)))
    correction(room_list[1])

def task3():
    print("Thread 3 start " + str(int(time.time()*1000)))
    correction(room_list[2])

def start_threads():
    t1 = Thread(target=task1)
    t2 = Thread(target=task2)
    t3 = Thread(target=task3)
    t1.start()
    t2.start()
    t3.start()


def main():
    item.save(send_meeting_invitations=SEND_TO_ALL_AND_SAVE_COPY)
    from time import sleep
    for i in range(20):
        sleep(2)
        modify()
        start_threads()

if __name__ == '__main__':
    main()