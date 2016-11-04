__author__ = 'zhwang.kevin'

# coding=GBK
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

def ab2c():
    conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')

    abc = 'jiayou'.replace('a', 'z')

    cur = conn.cursor()
    cur.execute("SELECT b.HotelCoverPic from tab_2_hotel b where b.Country='日本'")

    data = cur.fetchall()
    cur.execute("select a.Url from tab_hotel_2_pic a where a.HotelID in (SELECT b.HotelID from tab_2_hotel b where b.Country='日本')")
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
    cur.execute("SELECT b.HotelCoverPic from tab_hotel b")

    data = cur.fetchall()
    cur.execute("select a.Url from tab_hotel_pic a")
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
        ret_delete=client.delete_file(url)

    print('shoudong wancheng')


if __name__ == '__main__':

    ab2c()

    # for hotel_star_class in ['b-sprite', 'stars', 'ratings_stars_4_half', 'star_track']:
    #     if 'ratings_stars' in hotel_star_class \
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

