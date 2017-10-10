# coding=utf-8
from http.cookiejar import CookieJar, urllib
import pymysql

__author__ = 'zhwang.kevin'

class CommonUtiles(object):

    @classmethod
    def get_oppener(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
            'Accept': 'text/html;q=0.9,*/*;q=0.8', 'Accept-Charset': 'utf-8;q=0.7,*;q=0.3',
            'Connection': 'close'}

        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener.addheaders = headers.items()

        return opener

    @classmethod
    def get_conn_cur(self,ipad,porti,userName,password,dbname,autocomm):

        #inner net or outer net
        conn = pymysql.connect(host=ipad, port=porti, user=userName, passwd=password, db=dbname,
                           charset='UTF8')
        # conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
        #                        charset='UTF8')
        cur = conn.cursor()
        conn.autocommit(autocomm)
        return conn, cur
