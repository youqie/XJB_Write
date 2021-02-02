"""
针对Windows Server + SQL Server的预约屏压力测试
1. 创建楼宇（id=1)
2. 创建200个会议室(id>=1 && id<=200)
3. 绑定200个预约屏(id>=198 && id<=397)
4. 模拟轮训请求（每10秒轮训一遍，每次轮训7个接口） 每分钟200*6*7
5. 订会请求测试
"""
from random import choice
import requests
import string
import json
import threading
import time

# 登录token
token = ''
url = 'http://192.168.10.194/'
letters_digits = string.ascii_uppercase + string.digits
headers_tablet = {'Content-Type': 'application/json'}
flag = True


def login():
    # 登录获取token
    """ 正确密码 """
    payload = "{\n    \"model\": {\n        \"account\": \"admin@dfocuspace.com\",\n        \"password\": " \
              "\"s6RAk1jZm2A+lU9YWlSSzw==\",\n        \"tenantId\": 1\n    }\n} "
    headers = {
        'Content-Type': 'application/json'
    }
    r = requests.post(url=url+"apis/account/login", data=payload, headers=headers)
    global token
    token = r.json()['model']['token']

def getFloorId(room_id):
    if room_id <= 48:
        return 4
    elif room_id <= 98 and room_id > 48:
        return 3
    elif room_id <= 148 and room_id > 98:
        return 2
    else:
         return 1

# 绑定预约屏
def bindTablet(room_id):
    # 随机生成序列号
    url_bind = url + "apis/admin/devices/displays"
    headers_utf8 = {'Authorization': token, 'Content-Type': 'application/json;charset=UTF-8'}
    sn = ''.join(choice(letters_digits) for i in range(13))
    payload = {
            'model': {
                'sn': sn,
                'categoryId': 4,
                'buildingId': 1,
                'floorId': getFloorId(room_id),
                'spaceId': room_id,
                'position': '俺在这里'
            }
        }
    response = requests.post(url=url_bind, headers=headers_utf8, data=json.dumps(payload))
    return response.json()['msg']

# 循环200次绑定
def recurrenceBind():
    for i in range(1, 201):
        print("---绑定第" + str(i) + "个预约屏结果：" + bindTablet(i) + "---")

class RecurrenceRequests(threading.Thread):
    def __init__(self, device_id):
        threading.Thread.__init__(self)
        self.id = device_id
    
    def keepAlive(self):
        url_ka = url + 'apis/tablet/' + str(self.id) + "/alive"
        payload = {
            'model': {
                'versionCode': 1202011300,
                'versionName': '4.0.7'
            }
        }
        response = requests.post(url=url_ka, headers=headers_tablet, data=json.dumps(payload))
        print("No " + str(self.id) + "..Keep Alive")
    
    def queryLed(self):
        url_ql = url + "apis/tablet/" + str(self.id) + "/led"
        response = requests.get(url=url_ql)
        print("No " + str(self.id) + "..Query Led")

    def queryCalc(self):
        url_qc = url + "apis/tablet/" + str(self.id) + "/spaces?isCalc=false"
        response = requests.get(url=url_qc)
        print("No " + str(self.id) + "..Query Calc")

    def queryAppt(self):
        url_qa = url + "apis/tablet/" + str(self.id) + "/appts?status=1,2,4,8"
        response = requests.get(url=url_qa)
        print("No " + str(self.id) + "..Query Appt")

    def queryQrcode(self):
        url_qq = url + "apis/tablet/" + str(self.id) + "/qrcode"
        response = requests.get(url=url_qq)
        print("No " + str(self.id) + "..Query Qrcode")

    def queryScreen(self):
        url_qs = url + "apis/tablet/" + str(self.id) + "/screen"
        response = requests.get(url=url_qs)
        print("No " + str(self.id) + "..Query Screen")

    def queryApk(self):
        url_qap = url + "apis/tablet/apk?deviceId=" + str(self.id) + "&tenantId=1&isOldTablet=false"
        response = requests.get(url=url_qap)
        print("No " + str(self.id) + "..Query Apk")
    
    def getConfigs(self):
        url_gc = url + "apis/admin/tablet/" + str(self.id) + "/configs"
        response = requests.get(url=url_gc)
        print("No " + str(self.id) + "..Get Configs")
    
    def getThemes(self):
        url_gt = url + "apis/admin/tablet/" + str(self.id) + "/themes"
        response = requests.get(url=url_gt) 
        print("No " + str(self.id) + "..Get Themes")

    def getPng(self):
        url_gp = url + "files/dmeeting/2020/apk_images/202012/DFB00FEE14805B8DD26ACD222BDAAC96.png"
        response = requests.get(url=url_gp)
        print("No " + str(self.id) + "..Get PNG")

    def run(self):
        while flag:
            self.keepAlive()
            self.queryLed()
            self.queryCalc()
            self.queryAppt()
            self.queryQrcode()
            self.queryScreen()
            self.queryApk()
            self.getConfigs()
            self.getThemes()
            self.getPng()
            time.sleep(10)


def main():
    """
    压测
    """
    for i in range(201, 401):
        thread = RecurrenceRequests(i)
        thread.start()
        print("No " + str(i-197) + "..Thread Start")
    """
    绑定预约屏
    """
    # login()
    # recurrenceBind()

if __name__ == "__main__":
    main()