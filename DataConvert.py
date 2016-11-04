__author__ = 'zhwang.kevin'

# coding=utf-8
import os, sys
import pymysql

os.chdir(os.path.dirname(sys.argv[0]))

def get_conn_cur_163():
    conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    cur = conn.cursor()
    return conn,cur

def get_conn_cur_163():
    conn = pymysql.connect(host='123.59.144.47', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    cur = conn.cursor()
    return conn,cur



