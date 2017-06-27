# coding=utf-8

import PostGetHttp
import json
import pymysql
import http.client, urllib, urllib.request
import os


def addSingnalPic(picLocation):
    # C:\\Users\\Public\\Pictures\\Sample Pictures\\Tulips.jpg
    tupian = {'file': picLocation}
    str = PostGetHttp.posthttp(tupian, 'http://10.101.1.165:8096/travel/travellingbag/addtupian')
    # print(str)
    picID = json.loads(str)['datas']
    return picID


def get_conn_cur_163():
    conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    cur = conn.cursor()
    conn.autocommit(1)
    return conn, cur


def getUpdateSql():
    updateSql = "update traveldb.tab_travelprovince prov set ProvincePicUrl = %s WHERE ProvinceCnName = %s "
    return updateSql


def updateProvincPicID(pPicID, provinceName):
    conn163, cur163 = get_conn_cur_163()
    cur163.execute(getUpdateSql(), (pPicID, provinceName))
    pass


def getPicsFromDisk(filesPath):
    pathDir = os.listdir(filesPath)
    files = []
    for allDir in pathDir:
        child = os.path.join('%s\%s' % (filesPath, allDir))
        files.append(child)
    return files


def addProvincePic():
    filesPath = 'D:\workspace\中国城市列表整理\特色图\中国省-特色图'
    fils = getPicsFromDisk(filesPath)

    for file in fils:
        fileName = file.split('\\').pop()
        province = fileName.split('-')[0]
        fileID = addSingnalPic(file)
        updateProvincPicID(fileID, province)


if __name__ == '__main__':
    addProvincePic()