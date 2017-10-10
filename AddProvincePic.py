# coding=utf-8
import random

import PostGetHttp
import json
import pymysql
import http.client, urllib, urllib.request
import os


def addSingnalPic(picLocation):
    # C:\\Users\\Public\\Pictures\\Sample Pictures\\Tulips.jpg
    #外网图片上传服务器
    outhost =  'http://app.dengnilvyou.com.cn';
    tupian = {'file': picLocation}
    str = PostGetHttp.posthttp(tupian, outhost+'/travel/travellingbag/addtupian')
    # print(str)
    picID = json.loads(str)['datas']
    return picID


def get_conn_cur_163():
    #外网数据库IP
    dbip = '114.55.139.196'
    conn = pymysql.connect(host=dbip, port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    cur = conn.cursor()
    conn.autocommit(1)
    return conn, cur


#省的图片上传
def getUpdateSql():
    updateSql = "update traveldb.tab_travelprovince prov set ProvincePicUrl = %s WHERE ProvinceCnName = %s "
    return updateSql

#hot city 图片上传
def getUpdateSqlHotCity():
    updateSql = "update traveldb.tab_travelregion region set RegionPicUrl = %s WHERE RegionCnName = %s "
    return updateSql



#
def updateProvincPicID(pPicID, regionName):
    conn163, cur163 = get_conn_cur_163()
    cur163.execute(getUpdateSqlHotCity(), (pPicID, regionName))
    pass


def getPicsFromDisk(filesPath):
    pathDir = os.listdir(filesPath)
    files = []
    for allDir in pathDir:
        child = os.path.join('%s\%s' % (filesPath, allDir))
        files.append(child)
    return files


def addProvincePic():

    filesPath = 'D:\workspace\中国城市列表整理\热门目的地缺失图片\热门目的地缺失图片'
    # filesPath = 'D:\workspace\中国城市列表整理\特色图\中国省-特色图'
    fils = getPicsFromDisk(filesPath)
    filIDs = [];

    for file in fils:

        #省图片整理出省的名字
        # fileName = file.split('\\').pop()
        # province = fileName.split('-')[0]

        #hotcity的图片中整理出城市名字
        fileName = file.split('\\').pop()
        province = fileName.split('.')[0]


        fileID = addSingnalPic(file)
        updateProvincPicID(fileID, province)

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

#其他无图片的城市国家图片上传
def updateSqlOtherCity(pPicID,regionID,conn196, cur196):
    updateSql = "update traveldb.tab_travelregion region set RegionPicUrl = %s WHERE RegionID = %s "

    try:
        updatecount = cur196.execute(updateSql, (pPicID, regionID))
        print("更新成功：",updatecount>0)
        #正确
        return updatecount
    except Exception:
        print("err")
        #错误
        return 0

#更新缺失图片的国家城市的图片url
def addOtherPic():
    filesPath = 'D:\DNYSVN\999_工具\当地特色图\缺失的城市图片'
    fils = getPicsFromDisk(filesPath)
    filIDs = [];
    dictionary = {}
    conn196, cur196 = get_conn_cur_163()
    countrysOrCities = getOhterRegions()

    for ctrcty in countrysOrCities:
        ranint = random.randint(0, 870)
        print("城市或国家 %s randomID %s",(ctrcty[1],ranint,ctrcty[0]))

        #判断图片是否已经上传至服务器，如果上传，就直接用上传后的id
        if(dictionary.__contains__(ranint)):
            # fileID = dictionary[ranint]
            pass
        else:
            ##图片上传至服务器
            dictionary[ranint] = addSingnalPic(fils[ranint])
        #更新图片url
        updateSqlOtherCity(dictionary[ranint],ctrcty[0],conn196, cur196)

    cur196.close()
    conn196.close()

if __name__ == '__main__':

    # addProvincePic()
    addOtherPic()