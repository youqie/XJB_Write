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

r1 = Account(primary_smtp_address='testroom2@dfocuspace.com', credentials=credentials, autodiscover=False, config=config, access_type=DELEGATE)

item = CalendarItem(
    account = r1,
    folder = r1.calendar,
    start = r1.default_timezone.localize(EWSDateTime(2021, 1, 27, 17, 00)),
    end = r1.default_timezone.localize(EWSDateTime(2021, 1, 27, 18, 00)),
    location = "testroom1",
    subject = "meeting test",
    body = "test",
    required_attendees = ['testroom2@dfocuspace.com', 'asliu@dfocuspace.com', 'wangyu@dfocuspace.com']
)

def modify():
    for item in r1.calendar.all().order_by('-datetime_received')[:1]:
        item.subject = "修改会议测试"
        item.end = r1.default_timezone.localize(EWSDateTime(2021, 1, 27, 17, 30))
        item.save(send_meeting_invitations=SEND_TO_ALL_AND_SAVE_COPY)

def main():
    item.save(send_meeting_invitations=SEND_TO_ALL_AND_SAVE_COPY)
    sleep(20)
    modify()

if __name__ == '__main__':
    main()