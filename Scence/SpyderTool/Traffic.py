import requests
import json
import time
from urllib.parse import urlencode


def deco(func):
    def Load(self, cityCode):
        data = func(self, cityCode)
        return data

    return Load


class GaodeTraffic(object):

    def __init__(self, db):
        self.db = db
        self.s = requests.Session()
        self.headers = {
            'Host': 'report.amap.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

        }

    @deco
    def CityTraffic(self, cityCode):
        url = "http://report.amap.com/ajax/cityHourly.do?cityCode=" + str(cityCode)
        data = self.s.get(url=url, headers=self.headers)
        try:
            g = json.loads(data.text)
        except Exception as e:
            print("编号%d--网络链接error:%s" %(cityCode,e))
            print(data)

            return None
        today = time.strftime("%Y-%m-%d", time.localtime())  # 今天的日期
        date = today
        if '00:00' in str(g):
            date = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3600 * 24))  # 昨天的日期
        # 含有24小时的数据
        dic = {}
        for item in g:
            detailTime = time.strftime("%H:%M", time.localtime(int(item[0]) / 1000))
            if detailTime == '00:00':
                date = today
            dic['date'] = date
            dic['index'] = float(item[1])
            dic['detailTime'] = detailTime
            yield dic

    def LoadDatabase(self, CityTableCode, date, index, detailTime):
        cursor = self.db.cursor()

        sql = "insert into  traffic(pid_id,date,TrafficIndex,detailTime) values('%d','%s','%s','%s');" % (
            CityTableCode, date, index, detailTime)

        try:
            cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("error:%s" % e)
            self.db.rollback()


class BaiduTraffic(object):

    def __init__(self, db):

        self.db = db
        self.s = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

        }
        # 获取实时城市交通情况

    @deco
    def CityTraffic(self, cityCode, timeType='minute'):

        parameter = {
            'cityCode': cityCode,
            'type': timeType  # 有分钟也有day
        }
        href = 'https://jiaotong.baidu.com/trafficindex/city/curve?' + urlencode(parameter)
        data = self.s.get(url=href, headers=self.headers)
        try:
            g = json.loads(data.text)
        except Exception as e:
            print("网络链接error:%s" % e)
            return None
        today = time.strftime("%Y-%m-%d", time.localtime())  # 今天的日期
        date = today
        if '00:00' in str(g):
            date = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3600 * 24))  # 昨天的日期
        # 含有24小时的数据
        dic = {}
        for item in g['data']['list']:
            # {'index': '1.56', 'speed': '32.83', 'time': '13:45'}
            if item["time"] == '00:00':
                date = today
            dic['date'] = date
            dic['index'] = float(item['index'])
            dic['detailTime'] = item['time']
            yield dic

    def LoadDatabase(self, CityTableCode, date, index, detailTime):
        cursor = self.db.cursor()

        sql = "insert into  traffic(pid_id,date,TrafficIndex,detailTime) values('%d','%s','%s','%s');" % (
            CityTableCode, date, index, detailTime)
        try:
            cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("error:%s" % e)
            self.db.rollback()
        cursor.close()