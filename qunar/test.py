import json
import random
import re
import time
from pprint import pprint
from binascii import *
from lxml import etree

import requests
from zlib import adler32, decompress
# 149页
headers1 = {
                "Referer":"http://touch.qunar.com/api/hotel/hotellist?checkInDate=2018-05-12&checkOutDate=2018-05-13&extra=%7B%22L%22%3A%22%22%2C%22DU%22%3A%22%22%2C%22MIN%22%3A0%2C%22MAX%22%3A0%7D&couponsSelected=-1&city=%E5%8C%97%E4%BA%AC&page=1",
                "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
            }
# response1 = requests.get("http://touch.qunar.com/hotel/hoteldetail?city=%E5%8C%97%E4%BA%AC&checkInDate=2018-05-12&checkOutDate=2018-05-13&seq=beijing_city_37451&type=0&extra=%7B%22L%22%3A%22%22%2C%22DU%22%3A%22%22%2C%22MIN%22%3A0%2C%22MAX%22%3A0%7D&sort=0",headers=headers1)
# html1 = etree.HTML(response1.content.decode())
# ret1 = html1.xpath(".//div[@class='text-overflow qt-lh']//span[2]/text()")
# print(ret1)

# 2
# response2 = requests.get("http://touch.qunar.com/api/hotel/hotelprice?seq=beijing_city_37451&checkInDate=2018-05-12&checkOutDate=2018-05-13&type=0&sleepTask=&productId=&fromSource=&reqReferer=",headers=headers1)
# print(response2.)

# if "hotel_cc456b9b7750281d2d52cdca36041dbf_13" == "hotel_cc456b9b7750281d2d52cdca36041dbf_13":
#     print(1)
# else:
#     print(2)
# data = '[{"Impression_Id":"15318150003649279","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_121","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""},{"Impression_Id":"15318150003649570","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_14273","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""},{"Impression_Id":"1531815000364319","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_14581","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""},{"Impression_Id":"15318150003645839","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_19536","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""},{"Impression_Id":"15318150003641124","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_8068","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""},{"Impression_Id":"15318150003641582","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_13546","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""},{"Impression_Id":"15318150003644380","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_14699","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""},{"Impression_Id":"15318150003646567","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_19451","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""},{"Impression_Id":"15318150003642846","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_313","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""},{"Impression_Id":"15318150003649906","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_14665","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""},{"Impression_Id":"1531815000364681","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_12785","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""},{"Impression_Id":"15318150003643645","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_14692","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""},{"Impression_Id":"1531815000364123","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_2019","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""},{"Impression_Id":"15318150003644527","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_5296","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""},{"Impression_Id":"15318150003649612","Impression_Date":"2018-07-17","hotelSEQ":"shenzhen_5591","cookie_ID":"10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364","city_tag":"shenzhen","checkin_Date":"2018-07-17","checkout_Date":"2018-07-18","query":""}]'
# response = requests.post("http://hotel.qunar.com/render/listPageSnapshot.jsp",data=data)
# print(response.cookies.get_dict())

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
# response = requests.get(url.format(city='shenzhen',pageToken='0',randv='246364165452174',timestamp=str(int(time.time() * 1000)),beginDate='2018-07-18',endDate='2018-07-19',size='15'),headers=headers)
# # print(response.cookies.get_dict())
# # print(re.findall(b'\{.*\}', response.content)[0].replace(b"\'", b"\"").decode())
# index_obj = json.loads(re.findall(b'\{.*\}', response.content)[0].replace(b"\'", b"\"").decode())
# hotels = index_obj["hotels"]
# for hotel in hotels:
#     pprint(hotel)
#     break


url2 = "http://te.hotel.qunar.com/render/detailV2.jsp?HotelSEQ=shenzhen_12144&cityurl=shenzhen&fromDate=2018-07-18&toDate=2018-07-19&basicData=1&lastupdate=1531885903257&requestID=a5f1090-ob3sj-12l1&mixKey=0e68764603ac42f90d153188590098523sCcm4OuCNEaGybYxD7wL42hi1f3glZLHMnO&roomId=&filterid=f677c659-2f57-48c2-849d-e44f40e6c173_A&QUFP=ZSS_A20EEA15&isNewBook=1&showRestricted=&ex_track=&v={randv}&cn=2&hotelWzry=34s1e14bc5ehzn249bbeh_nw4&u=XVMNpZmhW1xp1Y9Jt6bCVczOz1136-aC15LHkpOltdKSk7Y2FzZSAzNDppZigyPT09eSYmMT09PWQua5t&__jscallback=jQuery18309808994433576192_1531885855695&_={randv2}"

headers2 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "QN99=7054; QunarGlobal=10.86.213.151_384865ce_1634e0b9a29_36f9|1526023866364; QN601=ab46bbdc370eba7477f153bd40bb032b; _i=RBTKSajz1DUxKyfR625Dq0RnUhUx; QN48=tc_c05705ee8bf79cfc_1634e1c4a44_cd8c; flowidList=.2-3.3-1.4-1.1-3.; QN57=15260270953600.253144139826301; QN58=1526027095359%7C1526027095359%7C1; _RSG=TEKspDQxhG9SDvbkIHyi38; _RDG=28fb6b5876871c29b8109011a3b7705d7b; _RGUID=942beda3-73d9-439d-80ec-f114ae97935c; QN235=2018-05-14; QN300=auto_4e0d874a; RT_CACLPRICE=1; csrfToken=324df6136b18d70bfad6ae0cfd25bb69; _RF1=119.137.62.211; QN205=organic; QN277=organic; QN163=0; QN269=B17E4500529411E887C7FA163E9DCB6D; Hm_lvt_75154a8409c0f82ecd97d538ff0ab3f3=1530686021,1531797986; QN25=c09ef174-e399-4598-a4ca-9ad50a345c15-9f992f90; QN1=dXrgjVtNidymd7omGA62Ag==; Hm_lpvt_75154a8409c0f82ecd97d538ff0ab3f3=1531810151; QN70=14706be7e164a700c707; __utmc=183398822; _jzqc=1; _jzqckmp=1; Hm_lvt_8fa710fe238aadb83847578e333d4309=1530686075,1531810185; __utmz=183398822.1531814888.12.5.utmcsr=hotel.qunar.com|utmccn=(referral)|utmcmd=referral|utmcct=/city/shenzhen/; _vi=J_9_RQJE8csA8axMvjAsvka8nQn9Q4JARgw4r-2K3-WKyXn3Jok_u2iGfrNi0_3ppDShuH_R_P1mMONUWZQJi27CjcCIqT0_lCOUsbb-44QB8vecrEOlBlu_9PZw7NJgqcHbCE9Tmj_qB4MZQi4vH8jFfhxvh7GX39_j3HPQl8AA; __utma=183398822.1649481530.1526023868.1531814888.1531885442.13; __utmt=1; QN73=3212-3213; _jzqa=1.3003862510100039000.1526023870.1531814904.1531885469.17; _jzqx=1.1526023870.1531885469.6.jzqsr=hotel%2Equnar%2Ecom|jzqct=/city/shenzhen/.jzqsr=hotel%2Equnar%2Ecom|jzqct=/city/shenzhen/; Qs_lvt_55613=1528712038%2C1528775356%2C1530686074%2C1531810184%2C1531885789; QN267=1531885900930_bf9b68af65d86018; QN268=1531885900930_bf9b68af65d86018|1531885902953_17ce3faf6039185a; Qs_pv_55613=4060083321614328000%2C2443607541543674000%2C3225679175490219000%2C3747453710993506000%2C4360567282271276500; Hm_lpvt_8fa710fe238aadb83847578e333d4309=1531885857; __utmb=183398822.5.10.1531885442; _jzqb=1.8.10.1531885469.1",
    # "Host": "te.hotel.qunar.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/59.0.3071.115 Safari/537.36",
}

# response = requests.get(url2.format(randv=str(int(time.time() * 1000)),randv2=str(int(time.time() * 1000)+2)),headers=headers2)
# print(response.content.decode())
# print(re.findall(b'\{.*\}', response.content)[0].replace(b"\'", b"\"").decode())


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

T = str(int(time.time() * 1000))
b = get_body(
            b_str % {"city": "shenzhen", "cityName": "null", "star": "0", "beginDate": "2018-07-20",
                     "ids": "shenzhen_13731", "price": "0.0", "endDate": "2018-07-21"}
            , T
        )
c = get_body(c_str % (T, random.choice(wifi_list)), c_key)

response = requests.post(APP_DETAIL_URL,headers=APP_HEADER,data=APP_BODY.format(b=b, c=c))
ret = parseResponse(response.content,T)
ret = json.loads(ret)
pprint(ret)
# with open("detail.json","w",encoding="utf-8") as f:
#     f.write(ret)