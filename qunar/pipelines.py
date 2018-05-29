# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymssql
from pprint import pprint


class QunarPipeline(object):
    def __init__(self):
        self.conn = pymssql.connect(host='192.168.2.135\sql2008', user='sa', password='sa', database='HotelSpider')
        self.cur = self.conn.cursor()

    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):

        # 清洗开业时间
        item["KYdate"] = item["KYdate"][0] if item["KYdate"] != [] else ''
        # 清洗电话
        item["phone"] = item["phone"][0] if item["phone"] != [] else ''
        # 清洗可入住人数
        item["Roomtype"]["people"] = item["Rdesc"][-2] if item["Rdesc"] != '' and type(int(item["Rdesc"][-2])) == int else 2
        # 清洗经纬度
        item["Latitude"] = item["street"].split(",")[0] if len(item["street"].split(",")) == 2 else ''
        item["Longitude"] = item["street"].split(",")[1] if len(item["street"].split(",")) == 2 else ''
        # 清洗有无窗户
        if item["Roomtype"]["window"] == "有窗":
            item["Roomtype"]["window"] = 1
        elif item["Roomtype"]["window"] == "无窗":
            item["Roomtype"]["window"] = 0
        elif item["Roomtype"]["window"] == '':
            item["Roomtype"]["window"] = 1
        else:
            item["Roomtype"]["window"] = 1
        

        # insert 酒店表
        # self.insert_hotels(item)
        # insert 房间表
        # self.insert_rooms(item)
        # insert 图片表
        self.insert_images(item)
        # insert 价格表
        # self.insert_price(item)
        # pprint(item)
        return item

    def insert_hotels(self,item):
        insert = "INSERT INTO Hotel (Source, HId, City, Name, Cover, [Level], Score, Address, Price, Phone, KYDate," \
                 + "Latitude, Longitude, Url, Status) values ('%d','%s','%s','%s','%s','%s','%f','%s','%.2f','%s','%s','%f','%f','%s','%d')" % (
            int((item["Source"])), item["HId"], str(item["Hcity"]), str(item["Hname"]), str(item["Himage"]),
            str(item["dangci"]), float(item["Score"]), str(item["address"]), float(item["Hprice"]),
            str(item["phone"]), str(item["KYdate"]), \
            float(item["Latitude"]), float(item["Longitude"]), str(item["Hurl"]), int(item["status"])
        )
        try:
            self.cur.execute(insert)
            print("插入成功Hotel")
        except Exception as e:
            print("插入失败Hotel")
            print(e)
        self.conn.commit()

    def insert_rooms(self,item):
        insert = "INSERT INTO Room (Source, HId, RId, Cover, Name, Floor, Area, Price, People, Bed, window) VALUES ('%d','%s','%s','%s','%s','%s','%s','%.2f','%d','%s','%d')" % (
            int((item["Source"])), str(item["HId"]), str(item["Rid"]), str(item["Rbaseimage"]),
            str(item["Rname"]),
            str(item["Roomtype"]["floor"]), str(item["Roomtype"]["area"]), float(item["Rprice"]),
            int(item["Roomtype"]["people"]), str(item["Roomtype"]["bed"]), int(item["Roomtype"]["window"])
        )

        try:
            self.cur.execute(insert)
            print("插入成功Room")
        except Exception as e:
            print(e)
            print("插入失败Room")
        self.conn.commit()

    def insert_images(self,item):
        if len(item["Rimage"]) > 1:
            # for i in item["Rimage"]:
            image_str = ';'.join(item["Rimage"])
        else:
            image_str = item["Rimage"][0] if item["Rimage"] != [] else ''
        # print("*"*100)
        # print(item["Rimage"])
        # print(type(item["Rimage"]))
        # print(image_str)
        # print("*"*100)
        if image_str != '':
            insert = "INSERT INTO Image (HId, RId, Url, Status) VALUES ('%s','%s','%s','%d')" % (
            str(item["HId"]), str(item["Rid"]), str(image_str), int(item["status"]))
    
            try:
                self.cur.execute(insert)
                print("插入成功Image")
            except Exception as e:
                print(e)
                print("插入失败Image")
        self.conn.commit()
    
    def insert_price(self,item):
        insert = "INSERT INTO Price (Source, HId, RId, PId, Name, Meal, [Rule], Price, Status) VALUES ('%d','%s','%s','%s','%s','%s','%s','%.2f','%d')" % (
            int((item["Source"])), str(item["HId"]), str(item["Rid"]), str(item["Roomtype"]["Pid"]),
            str(item["Rname"]), str(item["Roomtype"]["breakfast"]),str(item["Roomtype"]["rule"]),
            float(item["Roomtype"]["price"]), int(item["status"])
        )

        try:
            self.cur.execute(insert)
            print("插入成功Price")
        except Exception as e:
            print(e)
            print("插入失败Price")
        self.conn.commit()


