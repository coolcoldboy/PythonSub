# coding=utf-8
import random

import PostGetHttp
import json
import pymysql
import http.client, urllib, urllib.request
import os
import time
import pickle

def get_conn_cur_163():
    #外网数据库IP
    dbip = '114.55.139.196'
    conn = pymysql.connect(host=dbip, port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    cur = conn.cursor()
    conn.autocommit(1)
    return conn, cur

def getUpdateshedularplace():
    updateSql = "SELECT sp.spotsid, trim(sp.Address), trim(sp.NameCh), trim(sp.NameEn) FROM traveluserdb.tab_planscheduleplace placeid " \
                "INNER JOIN traveldb.tab_travelspots sp ON (placeid.SpotID = sp.SpotsID) WHERE placeid.spotID != 0 " \
                "ORDER BY placeid.spotid"

    # updateSql = "SELECT sp.spotsid, trim(sp.Address), trim(sp.NameCh), trim(sp.NameEn) FROM  " \
    #             "traveldb.tab_travelspots sp  WHERE sp.spotsID = 1232 "
    return updateSql

#抽取没有图片的城市获国家的列表
def getOhterRegions():
    updateSql = "SELECT region.RegionID, region.RegionCnName " \
                "FROM traveldb.tab_travelregion region " \
                "WHERE ( region.RegionPicUrl IS NULL OR region.RegionPicUrl = '' )"
    conn196, cur196 = get_conn_cur_163()
    try:
        cur196.execute(updateSql)
        countrysOrCities = cur196.fetchall()
        return countrysOrCities
    except Exception:
        print("err")
    finally:
        cur196.close()
        conn196.close()



#更新缺失图片的国家城市的图片url
def addOtherPic():

    conn196, cur196 = get_conn_cur_163()

    cur196.execute(getUpdateshedularplace())
    placeids = cur196.fetchall()
    url= 'https://maps.google.cn/maps/api/geocode/json?address=' \
         '#address' \
         '&key=AIzaSyAKQDsGaqzaoT34JjvpNzhs2POGlEOGbpc'

    updateSql = 'update traveldb.tab_travelspots spots set spots.secondLL = %s ,spots.Longitude = %s ,spots.Latitude=%s WHERE SpotsID = %s '

    if os.path.exists('file/spotidlis'):
        f = open('file/spotidlis', 'rb')
        spotidlis = pickle.load(f)
        f.close()
    else:
        spotidlis = []

    googleCheckNum = 2400

    for placeid in placeids:
        # sp.spotsid, sp.Address, sp.NameCh, sp.NameEn
        spotID = placeid[0]
        address = placeid[1]
        namech=placeid[2]
        nameeh=placeid[3]
        print(spotID,address,namech,nameeh)
        # 已经查过的poi跳过
        if spotID in spotidlis:
            continue

        spotidlis.append(spotID)
        retjsonobj = None

        time.sleep(2)

        if address!=None and address !='':
            addressUrl = url.replace('#address',address)
            retjson = urllib.request.urlopen(urllib.parse.quote(addressUrl,'?&:/=')).read().decode('utf-8')
            retjsonobj = json.loads(retjson)
            googleCheckNum -= 1
        if not (None != retjsonobj and None != retjsonobj['status'] and retjsonobj['status'] == 'OK') and nameeh!=None and nameeh !='' :
            addressUrl = url.replace('#address',nameeh)
            retjson = urllib.request.urlopen(urllib.parse.quote(addressUrl,'?&:/=')).read().decode('utf-8')
            retjsonobj = json.loads(retjson)
            googleCheckNum -= 1
        if not (None != retjsonobj and None != retjsonobj['status'] and retjsonobj['status'] == 'OK') and namech!=None and namech !='' :
            addressUrl = url.replace('#address',namech)
            retjson = urllib.request.urlopen(urllib.parse.quote(addressUrl,'?&:/=')).read().decode('utf-8')
            retjsonobj = json.loads(retjson)
            googleCheckNum -= 1


        #超过谷歌限制次数：退出循环
        if googleCheckNum == 0 :
            break

        if None == retjsonobj:
            continue

        if None != retjsonobj['status'] and retjsonobj['status'] == 'OK':
            longttu = retjsonobj['results'][0]['geometry']['location']['lng']
            lat = retjsonobj['results'][0]['geometry']['location']['lat']
            updateret = cur196.execute(updateSql,('1',longttu,lat,spotID))
            if updateret > 0:
                pass
        else:
            continue

    f = open('file/spotidlis', 'wb+')
    pickle.dump(spotidlis,f)
    f.flush()
    f.close()

    cur196.close()
    conn196.close()

if __name__ == '__main__':

    # addProvincePic()
    addOtherPic()