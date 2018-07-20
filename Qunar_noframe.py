import datetime
import hashlib
import pymssql
import json
import random
import re
import time
from pprint import pprint
from binascii import *
from lxml import etree

import requests
from zlib import adler32, decompress

def parseResponse(body, st):
    def setResource(bArr):
        i2 = 5
        if change(bArr, i) != 0:
            aa = change(bArr, i2)
            i3 = 0
            i2 += 4
            while i3 < aa:
                i4 = bArr[i2] & 255
                i2 += 1
                i2 += i4
                i2 += 1
                aa2 = change(bArr, i2)
                i2 += 4
                i2 += aa2
                i3 += 1
        return i2

    def change(arry, index):
        return ((((arry[index + 3] & 255) << 24) + ((arry[index + 2] & 255) << 16)) +
                ((arry[index + 1] & 255) << 8)) + ((arry[index] & 255) << 0)

    def dnl(response, timestamp):
        response = a2b_hex(b2a_hex(response)[8:])
        size, result, ii = len(response), "", 0
        result_list = []
        while ii < size:
            char = response[ii] - 0xd
            keychar = ord(timestamp[ii % len(timestamp)])
            dchar = ((char - keychar) ^ 0x45) & 0xff
            # result += chr(dchar) if dchar >= 0 else chr(dchar + 256)
            result_list.append(dchar)
            ii += 1
        return result_list

    bArr = [by if by < 127 else by-256 for by in body]

    i, i2, i4 = 14, 1, bArr[9] & 15

    if i4 != 0:
        a, i = change(bArr, 14), 18
    else:
        a = change(bArr, 10)

    a2 = dnl(body[i:i + a], st)
    if i4 != 0:
        a2 = [ss for ss in decompress(bytes(a2))]  # 假定dn1传回来的是byte[]
    if a2[0] & 255 == 1:
        i2 = setResource(a2)
    return bytes([s for s in a2[i2 + 4:i2 + 4 + change(a2, i2)]]).decode()


class QNspiders(object):
    #web
    url = "http://te.hotel.qunar.com/render/renderAPIList.jsp?attrs=0FA456A3,L0F4L3C1,ZO1FcGJH,J6TkcChI,HCEm2cI6,08F7hM4i,8dksuR_,YRHLp-jc,pl6clDL0,HFn32cI6,vf_x4Gjt,2XkzJryU,vNfnYBK6,TDoolO-H,pk4QaDyF,x0oSHP6u,z4VVfNJo,5_VrVbqO,VAuXapLv,U1ur4rJN,px3FxFdF,xaSZV4wU,ZZY89LZZ,ZYCXZYHIRU,sYWEvpo,er8Eevr,ha6ozyf,d90e9bb,HGYGeXFY,ownT_WG6,0Ie44fNU,yYdMIL83,MMObDrW4,dDjWmcqr,Y0LTFGFh,6X7_yoo3,8F2RFLSO,U3rHP23d,cGlja1Vw,7b4bfd15,yamiYIN,6bf51de0" \
           "&showAllCondition=1&showBrandInfo=1&showNonPrice=1&showFullRoom=1&showPromotion=1&showTopHotel=1&showGroupShop=1" \
           "&useCommend=1&output=json1.1&v=0.{randv}&requestTime={timestamp}" \
           "&mixKey=1171bc836e4c6215b220d150089069984417o3Fk1gOwGfy2LiuElZURia9&requestor=RT_HSLIST&cityurl={city}" \
           "&fromDate={beginDate}&toDate={endDate}&limit={pageToken}%2C{size}&filterid=e40bdeca-0e4d-4b96-9769-971b3b30cd1f_A" \
           "&isFirstPage=0&u=NS1zIpPh2j*-qSQ8t6bCVczOz466-ODc6aCh0KHIuY2hhckF0KHYrKykpKHAoKSxwKCkpKTticmVhhpm" \
           "&u=NS1zIpPh2j*-qSQ8t6bCVczOz466-ODc6aCh0KHIuY2hhckF0KHYrKykpKHAoKSxwKCkpKTticmVhhpm&__jscallback=XQScript_5"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "QN99=5227; QN601=5619c26a1a707b58e7c550223c200227; QunarGlobal=10.86.213.138_-25ad7a65_15cf2da82c7"
              "_7ed4|1498724394342; pgv_pvi=5830361088; QN48=tc_90f6ef1566df4b14_15cf2ef8384_d662; QN235=2017-06-29; "
              "QN9=localSearch%3D%26level%3D%26sort%3D%26checkInDate%3D2018-07-19%26keywords%3D%26filterValue%3D%26"
              "checkOutDate%3D2018-07-20%26location%3D%26pr%3D%26filter%3D%26city%3D%E5%8C%97%E4%BA%AC; "
              "QN621=fr%3Dmobile; _s=s_7WMVZ5UO3ORIS2EBTSLICM5OQ4; _v=fNAPZCA4louZVmk9wfvaSplgo_PrO0dHIg-"
              "2CwIOpxAC9PGt43uJfyvb9DKgKYJeS2ElGQJ53qyC9kjbkSaLFqL5Izpq_SthWzF6-Il0f5rEiJ7pwvbM0hj7S1NxX9os7rAu"
              "AAtwR0Ky917IXXQjVTUaKlL1zEMAdN2zT_HJheUw; _t=25239233; _q=U.nlbxcte4189; QN1=dXrgjVlxs8SZmRn4BIHbAg==;"
              " QN66=smart_app; QN300=smart_app; QN205=auto_4e0d874a; QN277=auto_4e0d874a; RT_CACLPRICE=1; "
              "csrfToken=ycgSRyDgxAClvDu77iozPpPZt1bWmzs8; QN163=0; QN269=57631D21679911E7BC93FA163E95E91F; "
              "Hm_lvt_75154a8409c0f82ecd97d538ff0ab3f3=1501120275,1501473996;"
              " Hm_lpvt_75154a8409c0f82ecd97d538ff0ab3f3=1501473996; QN70=21b15be2d15d96d3018e; pgv_si=s7500922880;"
              " QN73=2860-2861; _jzqx=1.1501062290.1501474003.6.jzqsr=hotel%2Equnar%2Ecom|jzqct=/city/beijing_city/"
              ".jzqsr=hotel%2Equnar%2Ecom|jzqct=/city/shenzhen/; _jzqckmp=1; QN44=nlbxcte4189; _i=ueHd86I_ynX9EbpXPlv1"
              "_M4WdQXX; _vi=P0oYKZTrKeNhilqeb3h8SGRQhsKCj-OuhHJX349f0-91H_CEXp5E6klnzfK2ftMT57n35IhfkM6YKuST0lkQ4c2B"
              "foNfHu83QmKeuZLc_SBta5qJ_fUmivtuqii5qjTIw8S2bbJ5iU05LncYeF9hRZri5SeQik35y_2rLdpha4Q0; QN268=15014743"
              "32061_6e0d15f7c669f1ad|1501474333014_ba15900b2cccfa96; __utma=183398822.1670760355.1501062286.1501233"
              "498.1501474000.6; __utmb=183398822.4.10.1501474000; __utmc=183398822; __utmz=183398822.1501226232.4.3"
              ".utmcsr=travel.qunar.com|utmccn=(referral)|utmcmd=referral|utmcct=/search/place/22-shenzhen-300118/0--"
              "---0/2; _jzqa=1.1229281856439020800.1501062290.1501232127.1501474003.14; _jzqc=1; _jzqb=1.3.10.1501474"
              "003.1; flowidList=.2-3.3-1.4-1.1-3.",
        # "Host": "te.hotel.qunar.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/59.0.3071.115 Safari/537.36",
    }

    # APP
    APP_URL = "http://client.qunar.com/ca?qrt=h_hdetailprice"  # 房型
    APP_DETAIL_URL = 'http://client.qunar.com/ca?qrt=h_hdetail'
    APP_HEADER = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "client.qunar.com",
        "Connection": "Keep-Alive",
    }
    APP_BODY = 'c={c}&b={b}&ext=&v=alex'

    b_str = u'{"cityTag":"%(city)s","cityTagName":"%(cityName)s","cityUrl":"%(city)s",' \
            u'"coordConvert":2,"currLatitude":"26.003806","currLongitude":"105.573273","extra":' \
            u'"{\\"hsrc\\":0,\\"qualityLabelList\\":[{\\"title\\":null,\\"fontColor\\":-1,\\"iconUrl\\":null,' \
            u'\\"rawType\\":3,\\"type\\":2,\\"content\\":\\"null\\",\\"frameColor\\":-16280065}],' \
            u'\\"ugcRecommend\\":\\"null\\",\\"landMarkCoord\\":null,\\"landMarkText\\":null,\\"recSrc\\":null,' \
            u'\\"kingOfKingsType\\":null,\\"lmlowest\\":false,\\"listChangeInfo\\":0,\\"hotelRec\\":null,' \
            u'\\"activityList\\":null,\\"hotelLevel\\":%(star)s,\\"bookGiveCarVoucher\\":null,\\"roomInfo\\":null}",' \
            u'"feedLog":"0,1","fromDate":"%(beginDate)s","fromForLog":0,"ids":"%(ids)s",' \
            u'"preListPrice":"%(price)s","preListType":0,"priceType":1,"quickCheckInFilter":0,"toDate":"%(endDate)s"}'
    b_key = '1505383062361'  # c中的ke， 即时间戳

    wifi_list = ["BT_CY"]  # wifi和某个东东有关联，不能换

    c_str = '{"adid":"c65f8107b89467ec","cid":"C2195","gid":"61529A41-556D-CD71-489D-D69874CBCAE7",' \
            '"ke":"%s","ma":"02:00:00:00:00:00","mno":"46003","model":"Redmi Note 3","msg":"","nt":"\\"%s\\"",' \
            '"osVersion":"6.0.1_23","pid":"10010","sid":"","t":"p_login","uid":"504566925795719","un":"","vid":"60001056"}'
    c_key = '6000lex'

    level_dict = {
        "1": "经济型",
        "2": "三星级/舒适",
        "3": "四星级/高档",
        "4": "五星级/豪华",
        "5": "二星级/其他",
    }
    meal_dict = {
        "0":"无早",
        "1":"单早",
        "2":"单早",
        "3":"双早"
    }

    def __init__(self):
        self.conn = pymssql.connect(host='119.145.8.188:16433', user='sa', password='Ecaim6688', database='HotelSpider')
        self.cur = self.conn.cursor()
        self.T = str(int(time.time() * 1000))

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def get_body(self,jsonstr, string1):
        i = 0
        byte_arry = []
        while i < len(jsonstr):
            char = ord(jsonstr[i]) ^ 0x45
            keychar = string1[i % len(string1)]
            encode = int(char + 0x07 + ord(keychar)) if string1 == '6000lex' else int(char + 0x0d + ord(keychar))
            i += 1
            byte_arry.append(encode)
            # dchar = chr(encode) if encode < 256 else chr(encode - 256)
            # result += dchar
        adl = "{0:X}".format(adler32(bytes(byte_arry)) & 0xffffffff)
        return "".join([adl[-2:], adl[:-2], b2a_hex(bytes(byte_arry)).upper().decode()])

    def get_params_bc(self,id,city='shenzhen',cityname="null"):
        now = datetime.date.today()
        tomorrw = now + datetime.timedelta(days=1)
        b = self.get_body(
            self.b_str % {"city": city, "cityName": cityname, "star": "0", "beginDate": now,
                     "ids": id, "price": "182.0", "endDate": tomorrw}
            , self.T
        )
        c = self.get_body(self.c_str % (self.T, random.choice(self.wifi_list)), self.c_key)
        return b,c

    def request_list(self,city='shenzhen',pageToken='0'):
        randv = ''.join([str(random.randrange(10)) for i in range(15)])
        now = datetime.date.today()
        tomorrw = now + datetime.timedelta(days=1)
        response = requests.get(url=self.url.format(city=city,pageToken=pageToken,size="15",randv=randv,timestamp=self.T,beginDate=now,endDate=tomorrw),headers=self.headers)
        list_obj = json.loads(re.findall(b'\{.*\}', response.content)[0].replace(b"\'", b"\"").decode())
        hotels = list_obj["hotels"]
        return hotels
        # for hotel in hotels:
        #     pprint(hotel)
        #     break

    def request_detail(self,HId):
        b,c = self.get_params_bc(HId)
        response = requests.post(self.APP_URL,headers=self.APP_HEADER,data=self.APP_BODY.format(b=b,c=c))
        ret = json.loads(parseResponse(response.content, self.T))
        # with open("detail.json","w",encoding="utf-8") as f:
        #     f.write(parseResponse(response.content, self.T))
        return ret

    def request_A_detail(self,HId):
        b, c = self.get_params_bc(HId)
        response = requests.post(self.APP_DETAIL_URL, headers=self.APP_HEADER, data=self.APP_BODY.format(b=b, c=c))
        ret = json.loads(parseResponse(response.content, self.T))
        return ret

    def insert_data(self,item):
        hotel_sql = "if exists(select top 1 * from HotelSpider.dbo.Hotel where HId = '%s')" %str(item["HId"]) + \
              " begin update Hotel set Score='%f',Price='%.2f',Phone='%s',UpdateTime='%s',area='%s',RoomCount='%s' where HId='%s' end" %(
            float(str(item["Score"])),float(item["Hprice"]),str(item["Phone"]),str(datetime.datetime.now())[:23],str(item["Area"]),str(item["Roomcount"]),str(item["HId"])
        ) + \
              " else begin INSERT INTO Hotel (Source, HId, City, Name, Cover, [Level], Score, Address, Price, Phone, KYDate," \
                 + "ZXDate, Latitude, Longitude, Url, Description, area,RoomCount) values ('%d','%s','%s','%s','%s','%s','%f','%s','%.2f','%s','%s','%s','%f','%f','%s','%s','%s','%s') end" %(
            int((item["Source"])),item["HId"],str(item["City"]),str(item["Hname"]),str(item["Cover"]),str(item["Level"]),float(item["Score"]),str(item["Address"]),float(item["Hprice"]),str(item["Phone"]),str(item["KYdate"]),\
            str(item["ZXdate"]),float(item["Latitude"]),float(item["Longitude"]),str(item["Hurl"]),str(item["Description"]),str(item["Area"]),str(item["Roomcount"]))

        room_sql = "if exists(select top 1 * from HotelSpider.dbo.Room where RId = '%s')" % str(item["room"]["RId"]) + \
              " begin update Room set Cover='%s',Name='%s',Price='%.2f',Window='%d',UpdateTime='%s' where RId='%s' end" %(str(item["room"]["cover"]),str(item["room"]["name"]),float(item["room"]["price"]),
                                                                                                              item["room"]["window"],str(datetime.datetime.now())[:23],str(item["room"]["RId"]))+ \
              " else begin INSERT INTO Room (Source, HId, RId, Cover, Name, Floor, Area, Price, People, Bed,Window) VALUES ('%d','%s','%s','%s','%s','%s','%s','%.2f','%d','%s','%d') end" %(
            int((item["Source"])),str(item["HId"]),str(item["room"]["RId"]),str(item["room"]["cover"]),str(item["room"]["name"]),
            str(item["room"]["floor"]),str(item["room"]["area"]),float(item["room"]["price"]),int(item["room"]["people"]),str(item["room"]["bed"]),item["room"]["window"]
        )

        price_sql = "if exists(select top 1 * from HotelSpider.dbo.Price where PId = '%s')" %str(item["roomtype"]["PId"]) + \
              " begin update Price set Name='%s',Price='%.2f',UpdateTime='%s' where PId='%s' end" %(str(item["roomtype"]["title"]),float(item["roomtype"]["price"]),
                                                                                                    str(datetime.datetime.now())[:23],str(item["roomtype"]["PId"]))+ \
              " else begin INSERT INTO Price (Source, HId, RId, PId, Name, Meal,[Rule], Price) VALUES ('%d','%s','%s','%s','%s','%s','%s','%.2f') end" %(
            int((item["Source"])),str(item["HId"]),str(item["room"]["RId"]),str(item["roomtype"]["PId"]),str(item["roomtype"]["title"]),str(item["roomtype"]["meal"]), str(item["roomtype"]["rule"]),float(item["roomtype"]["price"])
        )

        try:
            self.cur.execute(hotel_sql)
            self.cur.execute(room_sql)
            self.cur.execute(price_sql)
        except Exception as e:
            print(e)
            pprint(item)
        self.conn.commit()


    def run(self):
        page = 11
        while True:
            hotels = self.request_list(pageToken=page*15)
            print(page)
            for hotel in hotels:
                item = {}
                item["Source"] = "2"
                item["Hname"] = hotel["attrs"]["hotelName"]
                item["Address"] = hotel["attrs"]["hotelAddress"]
                # http://himg3.qunarzz.com/imgs/201605/29/66I5P2-JuXy9ugq66720.jpg
                item["Cover"] = 'http://himg3.qunarzz.com/imgs/'+ hotel["attrs"]["imageUri"] + "720" + ".jpg"
                item["Area"] = hotel["attrs"]["HotelArea"]
                item["Hprice"] = hotel["price"]
                item["Hpoint"] = hotel["attrs"]["bpoint"]
                item["Latitude"] = item["Hpoint"].split(",")[:-1][0]
                item["Longitude"] = item["Hpoint"].split(",")[1:][0]
                item["Score"] = hotel["attrs"]["CommentScore"]
                item["City"] = hotel["cityName"]
                item["HId"] = hotel["id"]
                item["Level"] = hotel['attrs']["dangci"]
                item["Level"] = self.level_dict[item["Level"]]
                print(item["HId"])
                hotel_detail = self.request_A_detail(item["HId"])
                item["Roomcount"] = "0"
                if hotel_detail["bstatus"]["code"] == 0:
                    time.sleep(random.randint(5, 6))
                    try:
                        item["Phone"] = hotel_detail["data"]["dinfo"]["phone"]
                    except Exception as e:
                        pprint(hotel_detail)
                    item["KYdate"] = hotel_detail["data"]["dinfo"]["whenOpen"] if "whenOpen" in hotel_detail["data"]["dinfo"] else ''
                    item["ZXdate"] = hotel_detail["data"]["dinfo"]["whenFitment"] if "whenFitment" in hotel_detail["data"]["dinfo"] else ''
                    item["Hurl"] = "http://hotel.qunar.com/city/{city}/dt-{id}/".format(city=item["HId"].split("_")[:-1][0],id=item["HId"].split("_")[1:][0])
                    item["Description"] = hotel_detail["data"]["dinfo"]["desc"]
                    item["Description"] = item["Description"].replace("/",'').replace("\r\n","").replace("'",'')
                    if "房间数" in item["Description"]:
                        item["Roomcount"] = re.match(r"房间数：(\d+)间",item["Description"]).group(1) if re.match(r"房间数：(\d+)间",item["Description"]).group(1) else 0
                detail = self.request_detail(item["HId"])
                time.sleep(random.randint(5,6))
                rooms = detail["data"]["rooms"]
                if rooms:
                    for room in rooms:
                        item["room"] = {}
                        item["room"]["name"] = room["roomName"]
                        str_date = (str(item["HId"]) + str(item["room"]["name"])).encode("utf-8")
                        item["room"]["RId"] = hashlib.md5(str_date).hexdigest()
                        item["room"]["area"] = room["area"]
                        item["room"]["floor"] = room["floor"]
                        item["room"]["bed"] = room["bedType"]
                        item["room"]["cover"] = [i["url"] for i in room["images"]][0] if [i["url"] for i in room["images"]] != [] else ''
                        try:
                            item["room"]["window"] = room["window"]
                        except Exception as e:
                            try:
                                item["room"]["window"] = room["rtDescInfo"]["window"] if room["rtDescInfo"]["window"] else ''
                            except:
                                item["room"]["window"] = 0
                        if "有" in str(item["room"]["window"]):
                            item["room"]["window"] = 1
                        else:
                            item["room"]["window"] = 0
                        try:
                            item["room"]["people"] = room["rtDescInfo"]["maxCustomers"] if room["rtDescInfo"] else ''
                        except:
                            item["room"]["people"] = "2"
                        item["room"]["price"] = room["mprice"]
                        roomtypes = room["vendors"]
                        for roomtype in roomtypes:
                            item["roomtype"] = {}
                            item["roomtype"]["title"] = roomtype["room"]
                            item["roomtype"]["price"] = roomtype["price"]
                            item["roomtype"]["PId"] = roomtype["roomId"]
                            item["roomtype"]["meal"] = roomtype["breakfastCode"] # 0 无早 2单 3双早
                            item["roomtype"]["meal"] = self.meal_dict[str(item["roomtype"]["meal"])]
                            rule = [i["title"] for i in roomtype["otaSpecialTips"] if "取消" in i["title"]]
                            item["roomtype"]["rule"] = rule[0] if rule else ''
                            self.insert_data(item)
                else:
                    pprint(detail["data"])
            page += 1



if __name__ == '__main__':
    spider = QNspiders()
    spider.run()

# item["Description"]
