__author__ = 'zhwang.kevin'

#coding=utf-8
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

def get_conn_cur_196():
    #inner net or outer net
    # conn = pymysql.connect(host='114.55.139.196', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
    #                        charset='UTF8')
    conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    cur = conn.cursor()
    conn.autocommit(0)
    return conn, cur

def getInsertSql():
    sql = 'INSERT INTO `traveldb`.`tab_placeicon` (`PlaceName`, `PlaceEnName`, ' \
          '`PlaceID`, `PlacePicUrl`, `PlaceHot`, `PlaceType`,`PlaceParentID`,`PlaceParent`) ' \
          'VALUES (%s, %s, %s, %s, %s, %s,%s,%s);'
    return sql

if __name__ == '__main__':
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
            countryPicUrl = country['piclist']['80']
            parentid = country['parentid']
            parentName = ''
            # picID = uploadepic(countryPicUrl,opener)
            # picID = 'dafds'
            type=1 #country
            print(countryName)
            # conn196, cur196 = get_conn_cur_196()
            # cur196.execute(getInsertSql(), (countryName, countryEnName, countryID,
            #                                 picID,str(index)+str(index2),type,parentid,parentName))
            # conn196.commit()
            # conn196.close()

            time.sleep(2)
            #chengshi
            for index3 in range(50,58):
                print(index3)
                # http://plan.qyer.com/api/ra.php?action=country2city&countryid=10&page=2
                urlcountry2city = "http://plan.qyer.com/api/ra.php?action=country2city&"
                conn1962, cur1962 = get_conn_cur_196()
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
                    cityPicUrl = city['pic']
                    parentid = city['countryid']
                    parentName = city['countryname']
                    picID = uploadepic(cityPicUrl,opener)
                    # picID = 'city'
                    type=2 #city

                    cur1962.execute(getInsertSql(), (cityName, cityEnName, cityID,
                                                  picID,str(index)+str(index2)+str(index3)+str(index4),type,parentid,parentName))
                conn1962.commit()
                conn1962.close()

    opener.close()
