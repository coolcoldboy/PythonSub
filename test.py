import re
# coding=utf-8
__author__ = 'zhwang.kevin'

import os, sys
import pymysql
import time
from fdfs_client.client import *


print(sys.getdefaultencoding())
import PostGetHttp
import platform
import json
from bs4 import BeautifulSoup
import http.client, urllib, urllib.request
import threading


def get_conn_cur_163():
    conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    cur = conn.cursor()
    conn.autocommit(0)
    return conn, cur


def get_conn_cur_47():
    conn = pymysql.connect(host='123.59.144.47', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    cur = conn.cursor()
    conn.autocommit(0)
    return conn, cur


def ab2c():
    conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')

    abc = 'jiayou'.replace('a', 'z')

    cur = conn.cursor()
    cur.execute("SELECT b.HotelCoverPic from tab_hotel_bak b where b.Country='日本'")

    data = cur.fetchall()
    cur.execute(
        "select a.Url from tab_hotel_pic_bak a where a.HotelID in (SELECT b.HotelID from tab_hotel_bak b where b.Country='日本')")
    data = data + cur.fetchall()

    client_file = 'fdfs_client.conf'
    client = Fdfs_client(client_file)

    for url in data:
        try:
            ret_delete = client.delete_file(url[0])
        except Exception as error:
            continue
        pass

    cur.close()
    conn.close()
    print('sql wancheng')


def abc():
    conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')

    abc = 'jiayou'.replace('a', 'z')

    cur = conn.cursor()
    cur.execute("SELECT b.HotelCoverPic from tab_hotel_bak b")

    data = cur.fetchall()
    cur.execute("select a.Url from tab_hotel_pic_bak a")
    data = data + cur.fetchall()

    client_file = 'fdfs_client.conf'
    client = Fdfs_client(client_file)

    for url in data:
        try:
            ret_delete = client.delete_file(url[0])
        except Exception as error:
            continue
        pass

    cur.close()
    conn.close()
    print('sql wancheng')


def cde(hoteltable):
    time.sleep(5)
    print(hoteltable)

    pass


def shoudongshan():
    client_file = 'fdfs_client.conf'
    client = Fdfs_client(client_file)
    pics = {
        'group1/M00/08/26/CmUBpVgILFWAYQ0EAAH-dlKEB64417.jpg',
        'group1/M00/08/26/CmUBpVgIK8KALapdAAA3VXq3quk302.jpg'
    }

    for url in pics:
        ret_delete = client.delete_file(url)

    print('shoudong wancheng')


def update_hotel_city_to_47():
    conn47, cur47 = get_conn_cur_47()
    conn163, cur163 = get_conn_cur_163()
    cur47.execute(
        "SELECT  SUBSTR(`comment`,8),SpotsID from traveldb.tab_travelspots  where cityid is NULL and SpotsTypeID=3 and `comment` like '%book%' ")
    hotelids = cur47.fetchall()

    for hotelid in hotelids:
        cur163.execute('SELECT  City from traveldb.tab_hotel where HotelID = \'' + hotelid[0] + '\' ')
        city = cur163.fetchone()
        city = city[0]
        updatesql = "UPDATE traveldb.tab_travelspots spot " \
                    "SET CityID =  " \
                    " ( " \
                    "  SELECT " \
                    "   r.RegionID " \
                    "  FROM " \
                    "   tab_travelregion r " \
                    "  WHERE " \
                    "   r.RegionCnName = %s " \
                    "  LIMIT 0, " \
                    "  1 " \
                    " ) " \
                    " WHERE " \
                    "  spot.SpotsID = %s "
        cur47.execute(updatesql,(city,hotelid[1]))
        conn47.commit()

    cur47.close()
    conn47.close()
    cur163.close()
    conn163.close()

    pass


if __name__ == '__main__':
    # update_hotel_city_to_47()
    print('woshi %d，%s'%(1,'洪'))
    hotel_id = 123234
    print("导入ID=%d的酒店图片到47 start"%(hotel_id))


    list = 'Rådhusesplanaden 14, 903 28 于默奥, 瑞典'.split(', ')
    postCode = list[len(list)-2]
    print(postCode.split('于默奥')[0].strip())

    match = re.search(r'（.*（.*））', 'Clayton Whites Hotel (formerly Whites of Wexford)（克莱顿怀特酒店（前韦克斯福德怀特酒店））')

    print(match.group(0))

    pass
    'shoudong wancheng'.split('shoudong')
    # ab2c()

    # for hotel_star_class in ['b-sprite', 'stars', 'ratings_stars_4_half', 'star_track']:
    # if 'ratings_stars' in hotel_star_class \
    #             or 'ratings_circles'  in hotel_star_class :
    #         hotel_star=int(hotel_star_class.split('_')[2])
    #         if len(hotel_star_class.split('_')) > 3:
    #             hotel_star= hotel_star + 0.5
    #         break
    #         pass
    #     pass
    # if hotel_star <4:
    #     pass
    # print('星级:' + str(hotel_star))
    # hotel_star_class = "wode_2.5"
    #
    # print('wode' in hotel_star_class)
    # print(hotel_star_class.split('_')[1])



    # hoteltables = {1,2,3}
    # threads =[]
    # for hoteltable in hoteltables:
    #     t = threading.Thread(target=cde,args=(hoteltable,))
    #     t.setDaemon(True)
    #     threads.append(t)
    # for tread in threads:
    #     tread.start()
    # for tread in threads:
    #     tread.join()
    #
    # print('wanliao')

    # shoudongshan()

