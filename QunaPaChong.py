# coding=utf-8
import os, sys
import pymysql
import time
from fdfs_client.client import *
import threading
from CommonUtils import CommonUtiles

print(sys.getdefaultencoding())
import PostGetHttp
import platform
import json
from bs4 import BeautifulSoup
import http.client, urllib, urllib.request
from http.cookiejar import CookieJar
import socket

os.chdir(os.path.dirname(sys.argv[0]))

def country_id_get():
    # 通过search栏输入的字来抽取目的地的信息hotel_name
    dest_parent_url = "http://piao.qunar.com/ticket/list.htm?keyword=#{city}&region=&from=mpl_search_suggest&page=#{page}"
    citys =['北京','成都','福州','广州','贵阳','哈尔滨','海口','杭州','合肥','呼和浩特','济南','昆明','拉萨','兰州市','南昌','南京','南宁','上海','深圳','沈阳','石家庄','太原','天津','乌鲁木齐','武汉','西安','西宁','银川','长春','郑州','重庆']
    # citys =['兰州市','南昌','南京','南宁','上海','深圳','沈阳','石家庄','太原','天津','乌鲁木齐','武汉','西安','西宁','银川','长春','郑州','重庆']


#    20559	20908	上海
#    20559	20800	北京
#    20559	21051	广州
#    20559	21062	深圳

    dictcity1 = {'上海': '20908', '北京': '20800', '广州': '21051','深圳': '21062'}
    dictcity2 = {'长春':'20883',
            '成都':'21147',
            '福州':'20965',
            '贵阳':'21168',
            '哈尔滨':'20892',
            '海口':'21086',
            '杭州':'20937',
            '合肥':'20948',
            '呼和浩特':'20857',
            '济南':'20985',
            '昆明':'21177',
            '拉萨':'21193',
            '兰州市':'21210',
            '南昌':'20974',
            '南京':'20924',
            '南宁':'21072',
            '沈阳':'20869',
            '石家庄':'20835',
            '太原':'20846',
            '天津':'20825',
            '乌鲁木齐':'21237',
            '武汉':'21020',
            '西安':'21200',
            '西宁':'21224',
            '银川':'21232',
            '郑州':'21002',
            '重庆':'21117'}
    dictcity = dict(dictcity1,**dictcity2)

    # 模拟chrome登陆
    oppener = get_oppener()

    country_id_list = list();
    reginon_type_list = list();
    reginon_name_list = list();

    insertsoptsql = 'INSERT INTO traveldb.tab_travelspots ( CountryID, CityID, SpotsTypeID, NameCh, PicURL, Address, Tel, Description, Rank, COMMENT, Longitude, Latitude, qunacategory, CreateDate, UpdateDate, IfAudit, ifLocation) ' \
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), 0, 1)'

    insertsoptpicsql =  "INSERT INTO traveldb.tab_travelspotsdetail ( SpotsID, PicURL, CreateDate, UpdateDate,Comment) VALUES (%s, %s, NOW(), NOW(),'quna')"

    selectExist = "select true from traveldb.tab_travelspots where NameCh=%s and Address =%s "


    conn,cur =  get_conn_cur_196()

    for ra in range(2,3):

        for city_item in citys:
            dest_rul = dest_parent_url.replace('#{city}', urllib.parse.quote(city_item)).replace('#{page}',str(ra))
            time.sleep(2)
            html = oppener.open(dest_rul).read().decode('utf-8')
            # dest_json_str = urllib.request.urlopen(dest_url).read().decode('utf-8')
            soup = BeautifulSoup(html, "html.parser")
            hoteltables = soup.find_all(class_="sight_item")
            if hoteltables== None:
                break
            for hoteltable in hoteltables:
                # print('data-id' + hoteltable['data-id'])
                # print('data-point' + hoteltable['data-point'])
                print('data-address' + hoteltable['data-address'])
                Address = hoteltable['data-address'];
                print('data-sight-category' + hoteltable['data-sight-category'])
                qunacategory = hoteltable['data-sight-category']
                print('data-sight-name' + hoteltable['data-sight-name'])
                spotdetailurl = 'http://piao.qunar.com' + hoteltable.h3.a['href']
                time.sleep(1)
                spothtml = oppener.open(spotdetailurl).read().decode('utf-8')

                # dest_json_str = urllib.request.urlopen(dest_url).read().decode('utf-8')
                spotsoup = BeautifulSoup(spothtml, "html.parser")
                Description = spotsoup.find(class_="mp-charact-intro").p.string
                jsonScript = spotsoup.findAll("script")[6].string
                start = jsonScript.index('window.context = ') + len('window.context = ')
                end = jsonScript.index('}\r\n') + 1
                jsonjindian = json.loads(jsonScript[start:end])
                Tel = jsonjindian['sightInfo']['phone']
                sightId = jsonjindian['sightInfo']['sightId']

                NameCh = jsonjindian['sightInfo']['title']
                imagesStr = jsonjindian['images']

                Longitude = None
                Latitude = None

                if len(jsonjindian['locInfo']['googlePoint']) > 0:
                    Longitude = jsonjindian['locInfo']['googlePoint'].split(',')[0]
                    Latitude = jsonjindian['locInfo']['googlePoint'].split(',')[1]
                PicURL = jsonjindian['sightInfo']['img']
                Rank =None
                if hoteltable.find(class_='level') != None :
                    # Rank = hoteltable.find(class_='level').string.replace('A景区', '')
                    Rank = hoteltable.find(class_='level').string[0:1]

                # 景点已经存在
                cur.execute(selectExist,[NameCh,Address])
                fetchallitems = cur.fetchall()
                if len(fetchallitems) >= 1:
                    spotexist = fetchallitems[0][0]
                    if spotexist == 1:
                        continue

                comment = 'quna'+sightId
                ifLocation = ''
                CountryID = '20559'
                CityID = dictcity.get(city_item)
                SpotsTypeID = '1'
                data = [CountryID, CityID, SpotsTypeID, NameCh, getPicUrl(oppener,PicURL), Address, Tel, Description, Rank, comment, Longitude,
                        Latitude, qunacategory]

                cur.execute(insertsoptsql,data)
                cur.execute('SELECT LAST_INSERT_ID() as abc')
                last_insert_id = cur.fetchall()[0][0]

                imagesarray = imagesStr.replace('[', '').replace(']', '').split(',')
                for image in imagesarray :
                    time.sleep(0.05)
                    picurl = getPicUrl(oppener,image)
                    cur.execute(insertsoptpicsql,[last_insert_id,picurl])
                    pass
        pass
    oppener.close()
    conn.close()
    cur.close()

def getPicUrl(oppener,pic_url):
    file_array = oppener.open(pic_url).read()
    tupian = {'file': file_array}
    retstr = PostGetHttp.posthttp_onefile(tupian, 'http://app.dengnilvyou.com.cn/travel/travellingbag/addtupian')
    jsonobj = json.loads(retstr)
    file_id = jsonobj['datas']
    return file_id

def get_oppener():

    opener = CommonUtiles.get_oppener()
    return opener


def get_conn_cur_196():

    ipad = '114.55.139.196'
    userName = 'traveldb'
    porti = 'traveldb'
    passwd = 'traveldb'
    dbname = 'traveldb'
    autocomm = 1

    conn, cur =CommonUtiles.get_conn_cur(ipad,userName,porti,passwd,dbname,autocomm)

    return conn, cur

if __name__ == '__main__':

    country_id_get()
