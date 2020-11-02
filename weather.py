# -*- coding:utf-8 -*-
#author:菜鸟小白的学习分享
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

KEY = "&key=9fe217be2d2840******d702183"#替换和风天气的key值
APIURL = "https://geoapi.heweather.net/v2/"
cityname = "合肥"
USERNAME = "菜鸟小白的学习分享"
s = requests.session()

def send_msg(content):

    title = cityname + "天气情况"
    print(title)
    params={
        'text':title,
        'desp':content
    }
    serverURL = "https://sc.ftqq.com/SCU48241Td01d****2e9d35caaccd7e9283.send"#替换自己的server酱KEY
    print(serverURL)
    print(params)
    response = requests.session().post(serverURL,data=params)
    print(response)
    # if response.json()['error'] != 0:
    #     print('发送成功')
    # else:
    #     print('发送失败')

class HeWeather(object):
    now_text = ""
    now_raw = []
    city_text = ""
    city_raw = []

    def __init__(self):
        self.city()

    # 利用获取IP地址的网页，获取本地城市名
    # @staticmethod
    # def getcity():
    # #     # inf = s.get("http://ip.lockview.cn/ShowIP.aspx").text
    # #     # print(inf)
    # #     # cityname = re.findall(r"(.*?)省", inf)[0]
    # #     # print(cityname)
    # #     # return cityname
    #     return "合肥"

    # 实况天气
    def now(self):
        api_type = "now?"
        # url = "https://geoapi.heweather.net/v2/city/lookup?city=深圳&key=2d849c62d67a4b9e94607d0f1c744561"

        url = "https://devapi.heweather.net/v7/weather/" + api_type + CITY + KEY
        # print(url)
        raw_json = s.get(url).json()
        # print(raw_json)
        if raw_json["code"] != "200":
            return  "获取天气失败:", raw_json["code"]
        self.now_raw = raw_json
        now_basic = raw_json["now"]
        updateTime = raw_json["updateTime"]
        print(now_basic)
        basic_city = self.city_raw[0]["name"]  # 城市
        # basic_cnty = now_basic["cnty"]  # 国家
        # basic_id = now_basic["id"]  # 城市代码
        # basic_lat = now_basic["lat"]  # 城市纬度
        # basic_lon = now_basic["lon"]  # 城市经度
        basic_loc = now_basic["obsTime"]  # 当地时间
        now_tmp = now_basic["temp"]  # 实时气温
        now_cond = now_basic["text"]  # 天气描述
        now_vis = now_basic["vis"]  # 能见度
        now_hum = now_basic["humidity"]  # 相对湿度
        now_fl = now_basic["feelsLike"]  # 体感温度
        now_pcpn = now_basic["precip"]  # 降雨量
        now_pres = now_basic["pressure"]  # 气压
        now_deg = now_basic["wind360"]  # 风向(360度)
        now_dir = now_basic["windDir"]  # 风向
        now_sc = now_basic["windScale"]  # 风力
        now_spd = now_basic["windSpeed"]  # 风速(kmph)

        text = """
实时天气:\n
亲爱的 {},您所在的地区为 {} ,\n
现在{}的天气是 {}天,\n
气温为 {}°\n
体感气温为 {}°\n
风向 {},\n
风速 {}\n
                """.format(USERNAME, basic_city, updateTime, now_cond, now_tmp, now_fl, now_dir, now_spd)
        self.now_text = text
        return text

    def city(self):
        # cityname = self.getcity()

        apitype = "city/lookup?location="
        # url = https://geoapi.heweather.net/v2/city/lookup?location=合肥&key=2d849c62d67a4b9e94607d0f1c744561
        url = APIURL + apitype + cityname + KEY
        raw_json = s.get(url).json()
        if raw_json["status"] != "200":
            return "获取天气失败:", raw_json["status"]
        print(raw_json)
        basic = raw_json["location"]
        self.city_raw = basic
        basic_name = basic[0]["name"]
        basic_country = basic[0]["country"]
        basic_id = basic[0]["id"]
        basic_adm1 = basic[0]["adm1"]  # 所属省会

        location = "&location=" + basic_id

        global CITY
        CITY = location
        city = "国家:{} 城市:{} 所属省会:{} 城市代码:{}".format(basic_country, basic_name, basic_adm1, basic_id)
        self.city_text = city
        return

def job():
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    heWeather = HeWeather()
    now = heWeather.now()
    city = heWeather.city_text
    send_msg(now)
    print(city)
    print(now)

if __name__ == '__main__':

    # 定义BlockingScheduler
    sched = BlockingScheduler()
    sched.add_job(job, 'interval', seconds=60)
    sched.start()