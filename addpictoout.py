# coding=utf-8
import json
import PostGetHttp
import os
__author__ = 'zhwang.kevin'

def addSingnalPic(picLocation):
    # C:\\Users\\Public\\Pictures\\Sample Pictures\\Tulips.jpg
    #外网图片上传服务器
    outhost =  'http://app.dengnilvyou.com.cn';
    # outhost = 'http://10.101.1.165:8096'
    tupian = {'file': picLocation}
    str = PostGetHttp.posthttp(tupian, outhost+'/travel/travellingbag/addtupian')
    # print(str)
    picID = json.loads(str)['datas']
    return picID

def getPicsFromDisk(filesPath):
    pathDir = os.listdir(filesPath)
    files = []
    for allDir in pathDir:
        child = os.path.join('%s\%s' % (filesPath, allDir))
        files.append(child)
    return files

if __name__ == '__main__':

    filesPath = 'D:\\DNYSVN\\999_工具\\003_系统随机头像\系统随机头像库\\100个'
    fils = getPicsFromDisk(filesPath)
    for file in fils:

        fileName = file.split('\\').pop()
        print(fileName+'#'+addSingnalPic(file))

    pass




