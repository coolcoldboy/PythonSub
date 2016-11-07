# coding=utf-8
__author__ = 'zhwang.kevin'

import os, sys
import pymysql
from fdfs_client.client import *
import threading

print(sys.getdefaultencoding())
import http.client, urllib, urllib.request
from http.cookiejar import CookieJar

os.chdir(os.path.dirname(sys.argv[0]))


def get_conn_cur_163():
    conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    cur = conn.cursor()
    conn.autocommit(0)
    return conn, cur


def get_oppener():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Accept': 'text/html;q=0.9,*/*;q=0.8', 'Accept-Charset': 'utf-8;q=0.7,*;q=0.3',
        'Connection': 'close'}

    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = headers.items()

    return opener


def get_conn_cur_47():
    conn = pymysql.connect(host='123.59.144.47', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    cur = conn.cursor()
    conn.autocommit(0)
    return conn, cur


def get_insert_city_sql():
    abc = "INSERT INTO `traveldb`.`tab_travelregion` ( " \
          " `ParentID`, " \
          " `RegionCnName`, " \
          " `ShortCnName`, " \
          " `RegionEnName`, " \
          " `RegionPicUrl`, " \
          " `CreateTime`, " \
          " `UPdateTime`, " \
          " `Sequence`, " \
          " `IfLeaf`, " \
          " `RegionType`," \
          " `comment` " \
          ") SELECT " \
          " reg.RegionID, " \
          " %s, " \
          " '', " \
          " '', " \
          " '', " \
          " NOW(), " \
          " NOW(), " \
          " '', " \
          " '1', " \
          " NULL," \
          " 'booking' " \
          "FROM " \
          " `traveldb`.`tab_travelregion` reg " \
          "WHERE " \
          " reg.RegionCnName = %s " \
          "AND ( " \
          " SELECT " \
          "  count(*) " \
          " FROM " \
          "  `traveldb`.`tab_travelregion` city " \
          " WHERE " \
          "  city.ParentID IN ( " \
          "   SELECT " \
          "    pare.RegionID " \
          "   FROM " \
          "    `traveldb`.`tab_travelregion` AS pare " \
          "   WHERE " \
          "    pare.RegionCnName = %s " \
          "  ) " \
          " AND city.RegionCnName = %s " \
          ") != 1;"
    return abc


def get_hotel_to_spot_sql(country):
    abc = "SELECT " \
          " '10067', " \
          " country.RegionID, " \
          " city.RegionID, " \
          " '3', " \
          " SUBSTR(hotel.Abstract,1,40), " \
          " NOW(), " \
          " '2', " \
          " hotel.HotelName, " \
          " hotel.HotelNameCH, " \
          " '1', " \
          " NOW(), " \
          " NULL, " \
          " hotel.HotelCoverPic, " \
          " hotel.Address, " \
          " hotel.Postcode, " \
          " NULL, " \
          " '', " \
          " hotel.Abstract, " \
          " hotel.Star, " \
          " NULL, " \
          " NULL, " \
          " NULL, " \
          " NULL, " \
          "  CONCAT('booking',hotelid)  " \
          "FROM " \
          " traveldb.tab_hotel hotel LEFT JOIN tab_travelregion country on ( " \
          "hotel.Country = " \
          "\'" + country + "\' " \
                           "AND " \
                           "country.RegionCnName = hotel.Country " \
                           ") " \
                           "LEFT JOIN tab_travelregion city on (city.RegionCnName = hotel.City) " \
                           "WHERE hotel.Country = " \
                           "\'" + country + "\'"
    return abc


def get_insert_hotel_sql(country):
    abc = "INSERT INTO `traveldb`.`tab_travelspots` (  " \
          "  `UserID`,`CountryID`,  " \
          "  `CityID`,`SpotsTypeID`,  " \
          "  `CommondReason`,`CreateDate`,  " \
          "  `SpotsType`,`NameEn`,  " \
          "  `NameCh`,`Status`,  " \
          "  `UpdateDate`,`Flavor`,  " \
          "  `PicURL`,`Address`,  " \
          "  `ZipCode`,`ZoneCode`,  " \
          "  `Tel`,`Description`,  " \
          "  `Rank`,`Price`,`Score`,  " \
          "  `LocalName`,`Alias`,`comment`  " \
          ")  " \
          "VALUES  " \
          "(  " \
          "%s,%s,%s,%s,%s,%s,%s,  " \
          "%s,%s,%s,%s,%s,%s,%s,  " \
          "%s,%s,%s,%s,%s,%s,%s,  " \
          " %s,%s,%s  " \
          ")"
    return abc
    pass


def import_city_to_47(country):
    conn47, cur47 = get_conn_cur_47()
    conn163, cur163 = get_conn_cur_163()

    cur163.execute('SELECT DISTINCT City from traveldb.tab_hotel where Country = \'' + country + '\' order by city')
    citys = cur163.fetchall()
    if (0 == len(citys)):
        return 0

    cur47.execute('SELECT RegionID from traveldb.tab_travelregion where RegionCnName = \'' + country + '\'')
    country = cur47.fetchall()
    if (0 == len(country)):
        print("外网 NO Country")
        return 0

    # 24760
    insert_city_sql = get_insert_city_sql()

    for city in citys:
        cur47.execute(insert_city_sql, (city[0], country, country,
                                        city[0]))
        pass
    conn47.commit()
    cur47.close()
    conn47.close()

    conn163.close()
    cur163.close()

    return len(citys)


def uploade_pic(url):
    if True:
        return 1

    main_url = 'http://10.101.1.165:8097/'
    pic_url = main_url + url

    oppener = get_oppener()

    client_file = 'fdfs_client_waiwang.conf'
    client = Fdfs_client(client_file)

    try:
        file_array = oppener.open(pic_url).read()
        oppener.close()
        pic_name = pic_url.split('/').pop()

        if None == file_array:
            return 'error'
        ret_upload = client.upload_by_buffer(file_array, pic_name.split('.')[1], {"fileName": pic_name})
        # print (ret_upload)

        file_id = ret_upload['Remote file_id'].replace('\\', '/')  # 新版本文件存放Remote file_id格式变化

        return file_id
    except Exception as err:
        print("error:")
        print(err.__traceback__)
        return "error"
        pass
    finally:
        pass
    pass


def import_hotel_pic_to_47(cur163, cur47, hotel_id, last_spots_id):
    cur163.execute('select Url,CONCAT( \'' + 'booking' + '\',HotelPicID) from traveldb.tab_hotel_pic where HotelID = \'' + str(hotel_id) + '\' order by HotelPicID ')
    pics = cur163.fetchall()

    if len(pics)==0:
        return 0

    insert_hotel_pic_sql = "INSERT INTO `traveldb`.`tab_travelspotsdetail` (`SpotsID`, `PicURL`, `Summary`, `CreateDate`, `UpdateDate`)  " \
                           "VALUES  " \
                           "(%s, %s, %s, NOW(), NOW())"

    for pic in pics:
        out_net_fileid = uploade_pic(pic[0])
        cur47.execute(insert_hotel_pic_sql,(last_spots_id,out_net_fileid,pic[1]))

        pass
    print("hotel_id:"+str(hotel_id))
    print("last_spots_id:"+str(last_spots_id))
    print("pics counts:"+str(len(pics)))
    return len(pics)
    pass


def import_hotel_to_47(country):
    conn47, cur47 = get_conn_cur_47()
    conn163, cur163 = get_conn_cur_163()

    hotel_to_spot_sql = get_hotel_to_spot_sql(country)
    insert_hotel_sql = get_insert_hotel_sql(country)

    # 内网的hotel的数据取得
    cur163.execute(hotel_to_spot_sql)
    hotels = cur163.fetchall()
    try:
        for hotel in hotels:
            # 内网的文件上传到外网并得到ID
            out_net_fileid = uploade_pic(hotel[12])
            hotel = list(hotel)
            # 将外网的HotelID保存到外网的数据库中
            hotel[12] = out_net_fileid
            hotel = tuple(hotel)
            # hotelID抽取
            hotel_id = hotel[23][7:]
            # 导入外网数据库
            count = cur47.execute(insert_hotel_sql, hotel)
            # 最后一个插入的spotsid抽取
            cur47.execute('SELECT LAST_INSERT_ID() as lastspotsID')

            last_spots_id = cur47.fetchone()[0]
            # 图片导入到外网
            count = import_hotel_pic_to_47(cur163, cur47, hotel_id, last_spots_id)
        conn47.commit()
    except Exception as error:
        print("error:")
        print(error.__traceback__)
        conn47.rollback()
        conn163.rollback()
    finally:
        cur163.close()
        cur47.close()
        conn47.close()
        conn163.close()
        pass

    pass


if __name__ == '__main__':
    country = '澳大利亚'
    # city_count = import_city_to_47(country)
    # print("citys sum: " + str(city_count))
    import_hotel_to_47(country)

    pass


