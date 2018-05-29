# -*- coding: utf-8 -*-
import json

from copy import deepcopy

import datetime
from lxml import etree
from pprint import pprint

import requests
import scrapy


# 当前日期,明天日期
def process_urltime():
    now = datetime.date.today()
    tomorrw = now + datetime.timedelta(days=1)
    return now, tomorrw

"详情页 http://touch.qunar.com/hotel/hoteldetail?city=%E5%8C%97%E4%BA%AC&checkInDate=2018-05-12&checkOutDate=2018-05-13&seq=beijing_city_37451&type=0&extra=%7B%22L%22%3A%22%22%2C%22DU%22%3A%22%22%2C%22MIN%22%3A0%2C%22MAX%22%3A0%7D&sort=0"
class QnSpider(scrapy.Spider):
    name = 'QN'
    allowed_domains = ['qunar.com']
    start_urls = ['http://touch.qunar.com/hotel/']
    # 列表页
    # duibi = "http://touch.qunar.com/api/hotel/hotellist?checkInDate=2018-05-14&checkOutDate=2018-05-15&extra=%7B%7D&couponsSelected=-1&city=%E6%B7%B1%E5%9C%B3&page=2"
    list_url = "http://touch.qunar.com/api/hotel/hotellist?checkInDate={}&checkOutDate={}&extra=%7B%22L%22%3A%22%22%2C%22DU%22%3A%22%22%2C%22MIN%22%3A0%2C%22MAX%22%3A0%7D&couponsSelected=-1&city=%E5%8C%97%E4%BA%AC&page={}"
    # 详情页电话
    Ph_detail_url = "http://touch.qunar.com/hotel/hoteldetail?city=%E5%8C%97%E4%BA%AC&checkInDate={}&checkOutDate={}&seq={}&type=0&extra=&sort=0"
    # 详情页房间
    # duibi =      "http://touch.qunar.com/api/hotel/hotelprice?seq=shenzhen_11052&checkInDate=2018-05-14&checkOutDate=2018-05-15&type=0&sleepTask=&productId=&fromSource=&reqReferer="
    detail_url = "http://touch.qunar.com/api/hotel/hotelprice?seq={}&checkInDate={}&checkOutDate={}&type=0&sleepTask=&productId=&fromSource=&reqReferer="
    # 当前页数
    cur_page = 1

    def start_requests(self):
        now,tomorrw = process_urltime()
        headers = {
            "Referer":"http://touch.qunar.com/hotel/shenzhen/"
        }
        yield scrapy.Request(
            headers=headers,
            url=self.list_url.format(now,tomorrw,self.cur_page)

        )

    def parse(self, response):
        response_str = response.body.decode()
        response_json = json.loads(response_str)
        hotels = response_json["data"]["hotels"]
        for hotel in hotels:
            item = {}
            item["Source"] = "2"
            item["Hcity"] = hotel["cityName"]
            item["Hprice"] = hotel["price"]
            item["HId"] = hotel["id"]
            item["status"] = hotel["status"]
            item["Score"] = hotel["attrs"]["CommentScore"]
            item["Hname"] = hotel["attrs"]["hotelName"]
            item["street"] = hotel["attrs"]["gpoint"]
            item["Himage"] = hotel["attrs"]["imageID"]
            item["address"] = hotel["attrs"]["hotelAddress"]
            item["dangci"] = hotel["attrs"]["dangciText"]
            # 获取当前日期和明天
            now,tomorrw = process_urltime()
            item["Hurl"] = self.detail_url.format(item["HId"],now,tomorrw)
            # 获取酒店电话和开业时间
            headers1 = {
                "Referer":"http://touch.qunar.com/hotel/shenzhen/",
                "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
            }
            # 获取当前时间和明天
            now,tomorrw = process_urltime()
            Ph_response_str = requests.get(self.Ph_detail_url.format(now,tomorrw,item["HId"]),headers=headers1)
            Ph_response_html = etree.HTML(Ph_response_str.content.decode())
            item["KYdate"] = Ph_response_html.xpath(".//div[@class='text-overflow qt-lh']//span[1]/text()")
            item["phone"] = Ph_response_html.xpath(".//div[@class='text-overflow qt-lh']//span[2]/text()")
            # pprint(item)
            headers2 = {
                "Referer":self.Ph_detail_url.format(now,tomorrw,item["HId"]),
            }
            yield scrapy.Request(
                url = self.detail_url.format(item["HId"],now,tomorrw),
                headers = headers2,
                meta={"item":deepcopy(item)},
                callback=self.detail_parse

            )
        # #翻页
        totalpage = response_json["data"]["totalPage"]
        print("当前第%s页" %self.cur_page)
        if self.cur_page < totalpage:
            now,tomorrw = process_urltime()
            yield scrapy.Request(
                url = self.list_url.format(now,tomorrw,self.cur_page+1),
                callback=self.parse
            )
            self.cur_page = self.cur_page + 1
            print("*"*50)
            print(self.cur_page)
            print("*"*50)

    def detail_parse(self,response):
        item = response.meta["item"]
        # print(response)
        response_str = response.body.decode()
        response_json = json.loads(response_str)
        rooms = response_json["data"]["rooms"]
        for room in rooms:
            item["Rname"] = room["name"]
            item["Rprice"] = room["lowPrice"]
            item["Rdesc"] = room["roomDesc"]
            item["Rid"] = room["tag"]
            item["Rbaseimage"] = room["images"][0]["url"] if room["images"] != [] else ''
            item["Rimage"] = []
            for image in room["images"]:
                item["Rimage"].append(image["url"])
            for Rtype in room["venders"]:
                item["Roomtype"] = {}
                item["Roomtype"]["room"] = Rtype["room"]
                item["Roomtype"]["rule"] = Rtype["priceBasicInfoList"][0]["desc"] if Rtype["priceBasicInfoList"] != [] else ''
                item["Roomtype"]["price"] = Rtype["price"]
                # item["Roomtype"]["window"] = Rtype["rtDescInfo"][1]["窗"]
                # item["Roomtype"]["area"] = Rtype["rtDescInfo"][3]["建筑面积"]
                # item["Roomtype"]["floor"] = Rtype["rtDescInfo"][4]["楼层"]
                # item["Roomtype"]["bed"] = Rtype["rtDescInfo"][5]["床型"]
                item["Roomtype"]["window"] = ''
                item["Roomtype"]["area"] = ''
                item["Roomtype"]["floor"] = ''
                item["Roomtype"]["bed"] = ''
                if Rtype["rtDescInfo"] != []:
                    for faci in Rtype["rtDescInfo"]:
                        if "窗" in faci:
                            item["Roomtype"]["window"] = faci["窗"]
                        if "建筑面积" in faci:
                            item["Roomtype"]["area"] = faci["建筑面积"]
                        if "楼层" in faci:
                            item["Roomtype"]["floor"] = faci["楼层"]
                        if "床型" in faci:
                            item["Roomtype"]["bed"] = faci["床型"]
                item["Roomtype"]["Pid"] = Rtype["seq"]
                item["Roomtype"]["breakfast"] = Rtype["roomRtInfo"][0]["tag"] if Rtype["roomRtInfo"] != [] else ''
                # print(item)
                yield deepcopy(item)
