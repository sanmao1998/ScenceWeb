import requests
import json
import time
from urllib.parse import urlencode
from SpyderTool.MulThread import MulitThread

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
    def RoadManager(self,cityCode):
        dic=self.Roads(cityCode) #道路基本信息
        dataList = self.__realTimeRoad(dic, cityCode) #获取数据

        for item, data in zip(dic['route'], dataList['data']):

            print(item)
            print(data)
            # b = Base()
            # b.date = date
            # b.DetailTime = DetailTime
            # b.name = item["name"]
            # b.speed = float(item["speed"])
            # b.data = json.dumps(data)
            # b.direction = item['dir']
            # b.bounds = json.dumps({"coords": item['coords']})
            # b.save()



    def Roads(self, cityCode):

        req = {
            "roadType": 0,
            "timeType": 0,
            "cityCode": cityCode
        }
        url = "https://report.amap.com/ajax/roadRank.do?" + urlencode(req)
        data = self.s.get(url=url, headers=self.headers)
        date = time.strftime("%Y-%m-%d", time.localtime())
        DetailTime = time.strftime("%H:%M", time.localtime())

        try:
            Route = json.loads(data.text)  # 道路信息包
        except Exception:
            return None
        listId = []  # 记录道路pid
        listRoadName = []  # 记录道路名
        listDir = []  # 记录道路方向
        listSpeed = []  # 记录速度
        for item in Route["tableData"]:
            listRoadName.append(item["name"])  # 道路名
            listDir.append(item["dir"])  # 方向
            listSpeed.append(item["speed"])  # 速度
            listId.append(item["id"])  # 道路pid
        dic = {} #存放所有数据
        dic["route"] = Route['tableData']
        dic["listId"] = listId
        dic["listRoadName"] = listRoadName
        dic["listDir"] = listDir
        dic["listSpeed"] = listSpeed

        return dic

    # 某条路实时路况
    def __realTimeRoad(self, dic, cityCode):
        req = {
            "roadType": 0,
            "timeType": 0,
            "cityCode": cityCode,
            'lineCode': ''

        }
        url = "https://report.amap.com/ajax/roadDetail.do?" + urlencode(req)
        threadlist = []
        data = []
        for id, i in zip(dic["listId"],
                         range(0, (dic["listId"]).__len__())):
            RoadUrl = url + str(id)
            t = MulitThread(target=self.__RealTimeRoadData, args=(RoadUrl, i,))  # i表示排名
            t.start()
            threadlist.append(t)
        for t in threadlist:
            t.join()
            if t.get_result is not None:
                data.append(t.get_result)

        ##排好序列
        if len(data) > 0:
            sorted(data, key=lambda x: ["num"])

        return {"data": data}

    def __RealTimeRoadData(self, RoadUrl, i):
        data = self.s.get(url=RoadUrl, headers=self.headers)
        try:
            g = json.loads(data.text)  # 拥堵指数
        except Exception:
            return None
        l = []  # 拥堵指数
        t = []  # 时间
        for item in g:
            t.append(time.strftime("%H:%M", time.strptime(time.ctime(int(item[0] / 1000 + 3600 * 8)))))
            l.append(item[1])
        # {排名，时间，交通数据}
        realData = {"num": i, "time": t, "data": l}
        return realData


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


GaodeTraffic(None).RoadManager("654000")