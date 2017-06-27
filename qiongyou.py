#coding=utf-8
__author__ = 'zhwang.kevin'


import os,sys
import pymysql
import time
from fdfs_client.client import *
from http.cookiejar import CookieJar
import json
from bs4 import BeautifulSoup
import http.client, urllib, urllib.request
import PostGetHttp
import traceback

import DataConvert

client_file = 'fdfs_client.conf'
client = Fdfs_client(client_file);

def get_oppener():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Accept': 'text/html;q=0.9,*/*;q=0.8', 'Accept-Charset': 'utf-8;q=0.7,*;q=0.3',
        'Connection': 'close'}

    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = headers.items()

    return opener


def uploadepic(picurl,oppener):
    # if 0==0:
    #     return picurl
    # print(picurl)
    tempi = 1
    while True:
        try:
            tempi = tempi+1
            file_array = oppener.open(picurl).read()
            tupian = {'file': file_array}
            #inner net or outer net
            # retstr = PostGetHttp.posthttp_onefile(tupian, 'http://101.37.21.161/travel/travellingbag/addtupian')
            retstr = PostGetHttp.posthttp_onefile(tupian, 'http://10.101.1.165:8888/travel/travellingbag/addtupian')
            jsonobj = json.loads(retstr)
            file_id = jsonobj['datas']
            # ret_upload = client.upload_by_buffer(file_array, pic_name.split('.')[1], {"fileName": pic_name})
            # # print (ret_upload)
            #
            # file_id = ret_upload['Remote file_id'].replace('\\', '/')  #

            return file_id
        except Exception as err:

            print("error:")
            print(err.__traceback__)
            traceback.print_exc()
            if tempi == 4:
                return picurl
            time.sleep(6)
            continue
        finally:
            pass


def get_conn_cur_163():
    #inner net or outer net
    # conn = pymysql.connect(host='114.55.139.196', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
    #                        charset='UTF8')
    conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    cur = conn.cursor()
    conn.autocommit(0)
    return conn, cur

def get_conn_cur_196():
    #inner net or outer net
    conn = pymysql.connect(host='114.55.139.196', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    # conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
    #                        charset='UTF8')
    cur = conn.cursor()
    conn.autocommit(1)
    return conn, cur

def getInsertSql():
    sql = 'INSERT INTO `traveldb`.`tab_placeicon_copy` (`PlaceName`, `PlaceEnName`, ' \
          '`PlaceID`, `PlacePicUrl`, `PlaceHot`, `PlaceType`,`PlaceParentID`,`PlaceParent`,`qypicurl`) ' \
          'VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s);'
    return sql

# 内网数据导入外网DB
def innerToOuter():
    sql = "SELECT region.regionPicUrlNew, region.hot, region.regionID, region.regionCnName, " \
          "region.parentID, parentregion.RegionCnName parentName FROM traveldb.tab_travelregion region " \
          "LEFT JOIN traveldb.tab_travelregion parentregion on (region.ParentID = parentregion.RegionID ) " \
          "WHERE (region.regionPicUrlnew IS not NULL and region.regionPicUrlNew != '') and region.ParentID = 0"

    updateSql = "update traveldb.tab_travelregion region,traveldb.tab_travelregion parent " \
                "set region.RegionPicUrl = %s, region.Hot = %s " \
                "WHERE ((region.ParentID = parent.RegionID  and parent.RegionCnName = %s) OR region.ParentID = 0   ) " \
                "and (region.RegionPicUrl is null or region.RegionPicUrl='') and region.RegionCnName = %s"

    conn163,cur163 = get_conn_cur_163()
    conn196,cur196 = get_conn_cur_196()
    cur163.execute(sql)
    regions = cur163.fetchall()
    try:
        for region in regions:
            out_net_fileid = DataConvert.uploade_pic(region[0])
            print(region[3])
            print(region[5])
            region = list(region)  # 将外网的HotelID保存到外网的数据库中
            region[0] = out_net_fileid
            cur196.execute(updateSql,(region[0],region[1],region[5],region[3]));
            pass
    except Exception as error:
        print("error:")
        print ('e.message:\t', error.message)
        traceback.print_exc()
    finally:
        cur163.close()

        conn163.close()
        cur196.close()
        conn196.close()
        pass
    pass


def qiongYouDownLoad():
    print('qiongyou')
    opener = get_oppener()
    # urlcountry2city = "http://plan.qyer.com/api/ra.php?action=country2city&countryid=10&page=100"
    # country2cityJsonStr = opener.open(urlcountry2city).read().decode('utf-8')
    # country2cityJson = json.loads(country2cityJsonStr)
    # picurl = country2cityJson['data']["list"][0]["pic"]
    # fileOpen = opener.open(picurl).read()
    #
    # exit(0)

    #
    # http://plan.qyer.com/api/place.php?action=getcountrylist&continent_id=0
    #
    #
    # http://plan.qyer.com/api/ra.php?action=country2city&countryid=10&page=1

    # urlcountry2city = "http://plan.qyer.com/api/ra.php?action=country2city&countryid=10&page=1"
    urlcountry2city = "http://plan.qyer.com/api/ra.php?action=country2city&"
    urlhotCountry = "http://plan.qyer.com/api/place.php?action=getcountrylist&continent_id=0"

    for index in range(1,14):
        urlhotCountry = "http://plan.qyer.com/api/place.php?action=getcountrylist&continent_id=0"
        urlhotCountry = urlhotCountry+'&'+'page='+str(index)
        hotCountryJsonStr = opener.open(urlhotCountry).read().decode('utf-8')
        hotCountryJson = json.loads(hotCountryJsonStr)
        if hotCountryJson['data']["list"] == False or hotCountryJson['data']["list"] == None:
            break
        #guojia
        for index2 in range(len(hotCountryJson['data']["list"])):
            country = hotCountryJson['data']["list"][index2]
            countryID = country['id']
            if(None == countryID):
                continue
            countryName = country['catename']
            countryEnName = country['catename_en']
            countryPicUrl = country['piclist']['120']
            parentid = country['parentid']
            parentName = ''
            picID = uploadepic(countryPicUrl,opener)
            # picID = 'dafds'
            type=1 #country
            print(countryName)
            conn163, cur163 = get_conn_cur_163()
            cur163.execute(getInsertSql(), (countryName, countryEnName, countryID,
                                            picID,str(index)+str(index2),type,parentid,parentName,countryPicUrl))
            conn163.commit()
            conn163.close()

            time.sleep(2)
            #chengshi
            for index3 in range(1,59):
                print(index3)
                # http://plan.qyer.com/api/ra.php?action=country2city&countryid=10&page=2
                urlcountry2city = "http://plan.qyer.com/api/ra.php?action=country2city&"
                conn1632, cur1632 = get_conn_cur_163()
                urlcountry2city = urlcountry2city+"countryid="+str(countryID)+"&page="+str(index3)
                country2cityJsonStr = opener.open(urlcountry2city).read().decode('utf-8')
                country2cityJson = json.loads(country2cityJsonStr)
                if country2cityJson['data']["list"] == False or country2cityJson['data']["list"] == None:
                    break
                for index4 in range(len(country2cityJson['data']["list"])):
                    city = country2cityJson['data']["list"][index4]
                    cityID = city['cityid']
                    if(None == cityID):
                        continue
                    cityName = city['cityname']
                    cityEnName = city['cityname_en']
                    cityPicUrl = city['piclist']['120']
                    parentid = city['countryid']
                    parentName = city['countryname']
                    picID = uploadepic(cityPicUrl,opener)
                    # picID = 'city'
                    type=2 #city

                    cur1632.execute(getInsertSql(), (cityName, cityEnName, cityID,
                                                     picID,str(index)+str(index2)+str(index3)+str(index4),
                                                     type,parentid,parentName,cityPicUrl))
                conn1632.commit()
                conn1632.close()

    opener.close()

def updateQYpic2Null():

# SELECT
# region.RegionCnName,
# parent.RegionCnName parentName
# FROM
# traveldb.tab_travelregion region,
# traveldb.tab_placeicon_copy icon,
# traveldb.tab_travelregion parent
# WHERE
# region.RegionCnName = icon.PlaceName
# AND region.ParentID = parent.RegionID
# AND icon.PlaceParent = parent.RegionCnName
# AND region.RegionCnName != ''
# AND icon.qypicurl = 'http://static.qyer.com/images/place/no/poi_80_80.png'
# UNION ALL
# SELECT
# region.RegionCnName,
# null parentName
# FROM
# traveldb.tab_travelregion region,
# traveldb.tab_placeicon_copy icon
# WHERE
# region.RegionCnName = icon.PlaceName
# AND ParentID = 0
# AND region.RegionCnName != ''
# AND icon.qypicurl = 'http://static.qyer.com/images/place/no/poi_80_80.png'


    updateSql = "update traveldb.tab_travelregion region,traveldb.tab_travelregion parent " \
                "set region.RegionPicUrl = null" \
                "WHERE ((region.ParentID = parent.RegionID  and parent.RegionCnName = %s) ) " \
                "region.RegionCnName = %s"

    # OR region.ParentID = 0
    import csv
    conn196,cur196 = get_conn_cur_196()

    with open("file\qingyoutupian.csv") as f:
        temp = csv.reader(f)
        for row in temp:
            cur196.execute(updateSql, (row[1], row[0]))



if __name__ == '__main__':
    # qiongYouDownLoad()

    # 内网数据导入外网DB
    innerToOuter()

    # updateQYpic2Null()

