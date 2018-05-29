from lxml import etree

import requests

# 1
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

if "hotel_cc456b9b7750281d2d52cdca36041dbf_13" == "hotel_cc456b9b7750281d2d52cdca36041dbf_13":
    print(1)
else:
    print(2)