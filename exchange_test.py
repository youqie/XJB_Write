from exchangelib import DELEGATE, IMPERSONATION, Message, Account, HTMLBody, Credentials, Configuration, NTLM, FaultTolerance, CalendarItem, EWSDateTime
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
from exchangelib.items import MeetingRequest, SEND_TO_ALL_AND_SAVE_COPY
from exchangelib.recurrence import Recurrence, WeeklyPattern
from exchangelib.fields import WEEK_DAY, MONDAY
from time import sleep
from datetime import timedelta, datetime

BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

# credentials = Credentials(username='dfocus\\administrator', password='DfocuSpace@P20m7')
credentials = Credentials(username='dfocuspace\\administrator', password='DfocuSpace@P20m9')
config = Configuration(retry_policy=FaultTolerance(max_wait=3600), server="192.168.10.118", credentials=credentials, auth_type=NTLM)

user_one = Account(primary_smtp_address='test_1@dfocuspace.com', credentials=credentials, autodiscover=False, config=config, access_type=DELEGATE)
user_two = Account(primary_smtp_address='test_2@dfocuspace.com', credentials=credentials, autodiscover=False, config=config, access_type=DELEGATE)


item_1 = CalendarItem(
    account = user_one,
    folder = user_one.calendar,
    start = user_one.default_timezone.localize(EWSDateTime(2021, 1, 21, 17, 00)),
    end = user_one.default_timezone.localize(EWSDateTime(2021, 1, 21, 18, 00)),
    location = "testroom1",
    subject = "Meeting Test",
    body = "Test 1",
    required_attendees = ['testroom_1@dfocus.cn', 'test_3@dfocus.cn']
)

item_2 = CalendarItem(
    account = user_two,
    folder = user_two.calendar,
    start = user_two.default_timezone.localize(EWSDateTime(2021, 1, 21, 17, 00)),
    end = user_two.default_timezone.localize(EWSDateTime(2021, 1, 21, 18, 00)),
    location = "TestRoom2",
    subject = "Meeting Test 2",
    body = "Test 2",
    required_attendees = ['TestRoom_2@dfocus.cn', 'test_3@dfocus.cn']
)

import time
from threading import Thread

def task1():
    print("Thread 1 start " + str(int(time.time()*1000)))
    for item in user_one.calendar.all().order_by('-datetime_received')[:1]:
        item.subject = "Meeting 1"
        item.required_attendees = ['testroom3@dfocuspace.com']
        item.save()

def task2():
    print("Thread 2 start " + str(int(time.time()*1000)))
    for item in user_two.calendar.all().order_by('-datetime_received')[:1]:
        item.subject = "Meeting 2"
        item.required_attendees = ['testroom2@dfocuspace.com']
        item.save()

def main():
    # item_1.save(send_meeting_invitations=SEND_TO_ALL_AND_SAVE_COPY)
    # item_2.save(send_meeting_invitations=SEND_TO_ALL_AND_SAVE_COPY)
    t1 = Thread(target=task1)
    t2 = Thread(target=task2)
    t1.start()
    t2.start()


if __name__ == '__main__':
    main()






# # account = Account(primary_smtp_address='Administrator@dfocuspace.com', credentials=credentials, autodiscover=False, config=config, access_type=DELEGATE)
# user_one = Account(primary_smtp_address='autotest_1@dfocuspace.com', credentials=credentials, autodiscover=False, config=config, access_type=DELEGATE)
# # room3_account = Account(primary_smtp_address='autotest_3@dfocuspace.com', credentials=credentials, autodiscover=False, config=config, access_type=DELEGATE)

# # 创建循环会议测试
# start = EWSDateTime(2021, 1, 18, 3, tzinfo=user_one.default_timezone)
# end = start + timedelta(hours=2)

# # 循环规则： 7 occurrences on Mondays of every third week, starting 2021, 1, 18
# master_recurrence = CalendarItem(
#     folder=user_one.calendar,
#     start=start,
#     end=end,
#     subject='Recurrence Meeting',
#     recurrence=Recurrence(
#         pattern=WeeklyPattern(interval=3, weekdays=[MONDAY]),
#         start=start.date(),
#         number=7
#     )
# )

# # master_recurrence.save(send_meeting_invitations=SEND_TO_ALL_AND_SAVE_COPY)

# # 编辑循环会议
# for occurrence in user_one.calendar.view(start=start, end=start + timedelta(days=4*3*7)):
#     occurrence.delete()
#     # occurrence.start = occurrence.start.astimezone(user_one.default_timezone)
#     # occurrence.start += timedelta(minutes=30)
#     # occurrence.end = occurrence.end.astimezone(user_one.default_timezone)
#     # occurrence.end += timedelta(minutes=30)
#     # occurrence.subject = 'Modify'
#     # occurrence.save()
# # start = EWSDateTime(2021, 1, 12, 0, tzinfo=room3_account.default_timezone)

# # end = EWSDateTime(2022, 1, 13, 0, tzinfo=room3_account.default_timezone)
# # for i in room3_account.calendar.filter(start__lt=end, end__gt=start):
# #     print(i.subject, i.start, i.end)
# #     print(i.recurrence)
#     # print(i.first_occurrence)
#     # print(i.last_occurrence)
# # account.ad_response

# # for calendar_item in user_one.calendar.all().order_by('-datetime_received')[:5]:
# #     print(calendar_item.subject)

# # start = EWSDateTime(2021, 1, 14, 0, 0, 0, tzinfo=user_one.default_timezone)
# # end = EWSDateTime(2022, 1, 14, 23, 59, 59, tzinfo=user_one.default_timezone)

# # master_recurrence = CalendarItem(
# #     folder = user_one.calendar,
# #     start = start,
# #     end = end,
# #     subject = '循环会议测试',
# #     recurrence = Recurrence(
# #         pattern = MonthlyPattern(interval = 1, weekdays = [WEEK_DAY]),
# #         start = start.date(),
# #         number = 7
# #     )
# # )


# # item = CalendarItem(
# #     account = user_one,
# #     folder = user_one.calendar,
# #     start = user_one.default_timezone.localize(EWSDateTime(2021, 1, 7, 16, 00)),
# #     end = user_one.default_timezone.localize(EWSDateTime(2021, 1, 7, 18, 00)),
# #     subject = "Subject of Meeting",
# #     body = "Test of My Exchangelib with Python",
# #     required_attendees = []
# # )

# # item.save(send_meeting_invitations=SEND_TO_ALL_AND_SAVE_COPY)

# # sleep(50)

# # for calendar_item in user_one.calendar.all().order_by('-datetime_received')[:5]:
# #     if calendar_item.organizer.email_address == user_one.primary_smtp_address:
# #         calendar_item.delete()
