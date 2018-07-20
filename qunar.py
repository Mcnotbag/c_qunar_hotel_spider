# coding=utf-8
from Api.nanqizhang.common.func import decorate_get, try_helper, StatusError, url2req, content_format, time_exchange, \
    random_str
from util.TornadoBaseUtil import TornadoBaseHandler
from Api.nanqizhang.common.template import get_hotel_object
from tornado import web, gen, httpclient, escape
from zlib import adler32, decompress
import random
from binascii import *
from hashlib import md5
from lxml import etree

import json
import re
import time
import chardet

INFO_URL = 'https://touch.qunar.com/api/hotel/hoteldetail/info?seq={id}'
PC_INFO_URL = "http://hotel.qunar.com/city/%s/dt-%s/"
NEARD_URL = 'http://hotel.qunar.com/render/detailRecommend.jsp?hotelSEQ={id}&startTime={beginDate}&endTime={endDate}'

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

TEST_URL = "http://te.hotel.qunar.com/render/renderAPIList.jsp?attrs=0FA456A3,L0F4L3C1,ZO1FcGJH,J6TkcChI,HCEm2cI6,08F7hM4i,8dksuR_,YRHLp-jc,pl6clDL0,HFn32cI6,vf_x4Gjt,2XkzJryU,vNfnYBK6,TDoolO-H,pk4QaDyF,x0oSHP6u,z4VVfNJo,5_VrVbqO,VAuXapLv,U1ur4rJN,px3FxFdF,xaSZV4wU,ZZY89LZZ,ZYCXZYHIRU,sYWEvpo,er8Eevr,ha6ozyf,d90e9bb,HGYGeXFY,ownT_WG6,0Ie44fNU,yYdMIL83,MMObDrW4,dDjWmcqr,Y0LTFGFh,6X7_yoo3,8F2RFLSO,U3rHP23d,cGlja1Vw,7b4bfd15,yamiYIN,6bf51de0" \
           "&showAllCondition=1&showBrandInfo=1&showNonPrice=1&showFullRoom=1&showPromotion=1&showTopHotel=1&showGroupShop=1" \
           "&useCommend=1&output=json1.1&v=0.{randv}&requestTime={timestamp}" \
           "&mixKey=1171bc836e4c6215b220d150089069984417o3Fk1gOwGfy2LiuElZURia9&requestor=RT_HSLIST&cityurl={city}" \
           "&fromDate={beginDate}&toDate={endDate}&limit={pageToken}%2C{size}&filterid=e40bdeca-0e4d-4b96-9769-971b3b30cd1f_A" \
           "&isFirstPage=0&u=NS1zIpPh2j*-qSQ8t6bCVczOz466-ODc6aCh0KHIuY2hhckF0KHYrKykpKHAoKSxwKCkpKTticmVhhpm" \
           "&u=NS1zIpPh2j*-qSQ8t6bCVczOz466-ODc6aCh0KHIuY2hhckF0KHYrKykpKHAoKSxwKCkpKTticmVhhpm&__jscallback=XQScript_5"

TEST = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "QN99=5227; QN601=5619c26a1a707b58e7c550223c200227; QunarGlobal=10.86.213.138_-25ad7a65_15cf2da82c7"
              "_7ed4|1498724394342; pgv_pvi=5830361088; QN48=tc_90f6ef1566df4b14_15cf2ef8384_d662; QN235=2017-06-29; "
              "QN9=localSearch%3D%26level%3D%26sort%3D%26checkInDate%3D2017-06-30%26keywords%3D%26filterValue%3D%26"
              "checkOutDate%3D2017-07-01%26location%3D%26pr%3D%26filter%3D%26city%3D%E5%8C%97%E4%BA%AC; "
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


def get_body(jsonstr, string1):
    result = ""
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

level_dict = {
    "1": "经济型",
    "2": "三星级/舒适",
    "3": "四星级/高档",
    "4": "五星级/豪华",
    "5": "二星级/其他",
}


class SearchHandle(TornadoBaseHandler):
    @decorate_get(cityid='', pageToken='0', kw='', beginDate='', endDate='', cityName='null', size='5', type="", id='')
    def get(self):
        pass

    @try_helper()
    @gen.coroutine
    def get_objects(self, parameter):
        self.itemList, self.hasNext, self.pageToken = [], False, None
        self.http_asy = httpclient.AsyncHTTPClient()
        self.parameter = parameter
        self.brandDict = {}

        if not self.parameter["cityid"] and not self.parameter["id"]:
            raise StatusError.Missing_param
        if not self.parameter["beginDate"] or not self.parameter["endDate"]:
            self.parameter["beginDate"] = time_exchange(time.time(), int2string=1)
            self.parameter["endDate"] = time_exchange(time.time() + 86400, int2string=1)

        try:
            int(self.parameter["size"])
            int(self.parameter["pageToken"])
        except:
            raise StatusError.Missing_param

        if self.parameter["type"] == "flat" and self.parameter["id"]:
            yield self.get_flat()
        elif self.parameter["type"] == "index" and self.parameter["cityid"]:
            yield self.get_index()
        else:
            yield self.apistart()

        if not self.itemList:
            raise StatusError.Succeed.EmptyResult

        raise StatusError.Succeed({
            'data': self.itemList,
            'hasNext': self.hasNext,
            'pageToken': self.pageToken
        })

    @gen.coroutine
    def apistart(self):
        index = yield self.get_index_obj()
        async_list = []
        for hotel in index:
            async_list.append(self.get_object(hotel))
        yield async_list

    @gen.coroutine
    def get_object(self, obj):

        request_list = [
            self.get_flat_obj(
                obj["id"], cityName=escape.url_escape(obj["cityName"]),
                star=obj["attrs"]["hotelStars"] if obj["attrs"].get("hotelStars") else "0",
                price=obj["price"]
            ),
            self.get_detail_obj(obj["id"], cityName=escape.url_escape(obj["cityName"]), star=obj["attrs"]["hotelStars"],
                                price=obj["price"])
            # url2req(NEARD_URL.format(id=obj["seqNo"], endDate=self.parameter["endDate"],
            #                          beginDate=self.parameter["beginDate"]), PC_WEB_HEADER)
        ]
        flat_detail = yield request_list
        # print len(flat_detail[0])
        # nearby_json = json.loads(response[1].body)["data"]["neighbors"]
        if flat_detail[1]:
            flat_detail[1]["flatOptions"] = flat_detail[0] if flat_detail[0] else None
            flat_detail[1].update({
                'id': obj["id"],
                'district': obj["attrs"]["HotelArea"],
                'star': int(obj["attrs"]["hotelStars"])
                if obj["attrs"].get("hotelStars") and obj["attrs"]["hotelStars"] != "0" else None,

                'brandName': self.brandDict[obj["attrs"]["hotelBrand"]]
                if obj["attrs"]["hotelBrand"] in self.brandDict else None,
                'imageUrls': [obj["attrs"]["imageID"]] if obj["attrs"].get("imageID") else None,

                'level': level_dict[obj["attrs"]["dangci"]]
                if obj["attrs"].get("dangci") and obj["attrs"]["dangci"] in level_dict else None
            })
            self.itemList.append(flat_detail[1])

    @gen.coroutine
    def get_index(self):
        index = yield self.get_index_obj()
        for hotel in index:
            self.itemList.append({
                'id': hotel["id"],
                'district': hotel["attrs"]["HotelArea"],
                'star': int(hotel["attrs"]["hotelStars"])
                if hotel["attrs"].get("hotelStars") and hotel["attrs"]["hotelStars"] != "0" else None,
                'city': hotel["cityName"],
                'brandName': self.brandDict[hotel["attrs"]["hotelBrand"]] if hotel["attrs"][
                                                                                 "hotelBrand"] in self.brandDict else None,
                'imageUrls': [hotel["attrs"]["imageID"]] if hotel["attrs"].get("imageID") else None,
                'level': level_dict[hotel["attrs"]["dangci"]]
                if hotel["attrs"].get("dangci") and hotel["attrs"]["dangci"] in level_dict else None
            })

    @gen.coroutine
    def get_flat(self):
        # self.count = 0
        request_list = []
        detail = yield self.get_detail_obj(self.parameter["id"],
                                       cityName=self.parameter["cityName"])
        response_list = yield self.get_flat_obj(self.parameter["id"], cityName=self.parameter["cityName"],
                                                  beginDate=self.parameter["beginDate"],
                                                  endDate=self.parameter["endDate"])
        detail["flatOptions"] = response_list if response_list else [{"checkinDate": self.parameter["beginDate"]}]
        minPrice = 0
        for flat in response_list:
            if minPrice != 0 and minPrice > flat["price"]:
                minPrice = flat["price"]
            elif minPrice == 0:
                minPrice = flat["price"]
        detail["minPrice"] = minPrice
        # print self.count
        self.itemList.append(detail)

    @gen.coroutine
    def get_index_obj(self):
        if self.parameter["kw"]:
            kw = "&q={}".format(escape.url_escape(self.parameter["kw"]))
        else:
            kw = ''
        index = yield self.http_asy.fetch(
            TEST_URL.format(city=self.parameter["cityid"], pageToken=self.parameter["pageToken"],
                            endDate=self.parameter["endDate"], beginDate=self.parameter["beginDate"],
                            randv=random_str(17, random_type="num"), timestamp=str(int(time.time() * 1000)),
                            size=self.parameter["size"]
                            )+kw,
            headers=TEST
        )
        # print re.findall('\{.*\}', index.body)[0].replace("\'", "\"")
        index_json = json.loads(re.findall(b'\{.*\}', index.body)[0].replace(b"\'", b"\""))
        # print(re.findall(b'\{.*\}', index.body)[0].replace(b"\'", b"\"").decode())

        for d in index_json["info"]["brands"]:
            self.brandDict[d] = index_json["info"]["brands"][d]["name"]

        hotel_list = []
        for hotel in index_json["hotels"]:
            hotel_list.append(hotel)

        if int(self.parameter["pageToken"]) + int(self.parameter["size"]) < index_json["info"]["count"]:
            self.hasNext, self.pageToken = True, str(int(self.parameter["pageToken"]) + int(self.parameter["size"]))
        raise gen.Return(hotel_list)

    @gen.coroutine
    def get_flat_obj(self, ID, cityName="null", star="0", price="182.0", beginDate='', endDate=''):
        if not beginDate:
            beginDate = self.parameter["beginDate"]
            endDate = self.parameter["endDate"]
        flat_list = []
        city = "_".join(ID.split('_')[:-1])
        T = str(int(time.time() * 1000))
        b = get_body(
            b_str % {"city": city, "cityName": cityName, "star": star, "beginDate": beginDate,
                     "ids": ID, "price": price, "endDate": endDate}
            , T
        )
        c = get_body(c_str % (T, random.choice(wifi_list)), c_key)
        response = yield self.http_asy.fetch(url2req(APP_URL, APP_HEADER, body=APP_BODY.format(b=b, c=c)))

        raw_response = parseResponse(response.body, T)
        response_json = json.loads(raw_response)
        try:
            for data in response_json["data"]["rooms"]:
                for i, vendor in enumerate(data["vendors"], start=1):
                    # self.count += 1
                    keyValues = []
                    if vendor.get("rtDesc1") and isinstance(vendor["rtDesc1"], list):
                        keyValues += vendor["rtDesc1"]
                    if vendor.get("rtDesc2") and isinstance(vendor["rtDesc2"], list):
                        keyValues += vendor["rtDesc2"]
                    flat_id = vendor["wrapperid"] + vendor["wrapperName"] + \
                              vendor["roomId"] + vendor["room"] + response_json["data"]["fromDate"] + vendor["price"]+data.get("roomInfoDesc", '')
                    flat_list.append({
                        # wrapperid+wrapperName+roomId+room
                        "id": md5(flat_id.encode("utf-8")).hexdigest(),
                        "description": data.get("roomInfoDesc"),
                        "imageUrls": [img["url"] for img in data["images"]] if data.get("images") else None,
                        "type": data["roomName"],
                        "unitName": vendor["room"],
                        'sortId': i,
                        "checkinDate": response_json["data"]["fromDate"],
                        "price": float(vendor["price"]),
                        "saleStatus": '可预订' if vendor["payable"] else '已订完',
                        "referId": ID,
                        "marketPrice": float(vendor["showPrice"]),
                        "promotions": [pro["text"] for pro in vendor["preferentialDescArr"]]
                        if vendor["preferentialDescArr"] else None,

                        # "isLowestPrice": vendor["lowestPrice"],
                        "priceUnit": vendor.get("currencySign"),
                        "keyValues": [
                            {
                                "key": keyValue["title"],
                                "value": keyValue["content"]
                            }
                            for keyValue in keyValues
                            ] if keyValues else None
                    })
        except:
            if self.parameter["type"] == "flat":
                raise StatusError.Unknown
        raise gen.Return(flat_list)

    @gen.coroutine
    def get_detail_obj(self, ID, cityName="深圳", star="0", price="182.0"):
        timestamp = str(int(time.time() * 1000))
        b = get_body(
            b_str % {"city": "_".join(ID.split('_')[:-1]), "cityName": cityName, "star": star,
                     "beginDate": self.parameter["beginDate"],
                     "ids": ID, "price": price, "endDate": self.parameter["endDate"]}
            , timestamp
        )
        c = get_body(c_str % (timestamp, random.choice(wifi_list)), c_key)
        response = yield self.http_asy.fetch(url2req(APP_DETAIL_URL, APP_HEADER, body=APP_BODY.format(b=b, c=c)))
        raw_response = parseResponse(response.body, timestamp)
        if "系统异常" in raw_response:
            raise StatusError.Succeed.EmptyResult
        detail = json.loads(raw_response)
        detail = detail["data"]["dinfo"]
        assistServices, infrastructures = [], []
        for facilitie in detail["facilities"]:
            if facilitie["type"] == u"服务项目":
                assistServices.extend(server["item"] for server in facilitie["datas"] if server.get("item"))
            else:
                infrastructures.extend(infrast["item"] for infrast in facilitie["datas"] if infrast.get("item"))

        raise gen.Return(get_hotel_object(
            rating=float(detail["score"])
            if detail.get("score") else None,

            description=detail["desc"]
            if detail.get("desc") else None,

            telephones=[detail["phone"]]
            if detail.get("phone") else None,

            commentCount=int(detail["commentCount"])
            if detail.get("commentCount") else None,

            # minPrice=obj["price"],
            # imageUrls=None,
            Id=detail["hotelSeq"],
            title=detail.get("name"),
            url=PC_INFO_URL % ("_".join(detail["hotelSeq"].split('_')[:-1]),
                               detail["hotelSeq"].split('_')[-1]),
            address=detail.get("add"),
            city=detail.get("city"),
            businessDistrict=detail["area"]
            if detail.get("area") else None,

            infrastructures=infrastructures
            if infrastructures else None,

            assistServices=assistServices
            if assistServices else None,

            # level=int(obj["hotelStars"])
            # if obj.get("hotelStars") and obj["hotelStars"] != "0" else None,

            # flatOptions=flatOptions
            # if flatOptions else None,

            # ratingDist=[
            #     {
            #         "key": "好评",
            #         "value": comment_json["commentData"]["goodTotal"]
            #     },
            #     {
            #         "key": "中评",
            #         "value": comment_json["commentData"]["mediumTotal"]
            #     },
            #     {
            #         "key": "差评",
            #         "value": comment_json["commentData"]["badTotal"]
            #     },
            # ]
            # if comment_json["commentData"]["mediumTotal"] or comment_json["commentData"]["goodTotal"]
            #    or comment_json["commentData"]["badTotal"] else None,

            # nearbyHotels=[
            #     {
            #         "id": hotel_id,
            #         "title": hotel_info["hotelName"],
            #         # "price": hotel_info.get("price"),
            #         "level": hotel_info.get("stars") if hotel_info.get("stars") != 0 else None,
            #         "distance": "距离%0.2f千米" % hotel_info["distance"],
            #         "url": PC_INFO_URL % ("_".join(hotel_id.split('_')[:-1]), hotel_id.split('_')[-1])
            #     }
            #     for hotel_id, hotel_info in nearby_json.items()
            #     ] if nearby_json else None,
            geoPoint={
                "lat": float(detail["gpoint"].split(",")[0]), "lon": float(detail["gpoint"].split(",")[1])
            }
            if detail.get("gpoint") and len(detail["gpoint"].split(",")) == 2 else None
        ))
