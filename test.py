

#1
# print(type(12334) == int)

#2
# str1 = '36㎡ 双床1.35m 有wifi 可住2人'
# print(str1[-2])
#3
# str2 = "https://userimg.qunarzz.com/imgs/201804/04/C._M0DCii7npL747rPi120.jpg"
# print(len(str2))

#4
str1 = ';'
list1 = ['https://himg1.qunarzz.com/imgs/201804/05/C._M0DCii7CGnUNYb2i480.jpg', 'https://himg1.qunarzz.com/imgs/201804/05/C._M0DCii7CGNtLfBwi480.jpg', 'https://himg2.qunarzz.com/imgs/201804/05/C._M0DCii7CpQeWE3li480.jpg', 'https://himg2.qunarzz.com/imgs/201804/05/C._M0DCii7CGUk0_tgi480.jpg']


str2 = str1.join(list1)

print(str2)