# coding=utf-8
from CommonUtils import CommonUtiles

__author__ = 'zhwang.kevin'

if __name__ == '__main__':
    opener = CommonUtiles.get_oppener()
    html = opener.open("http://www.simuwang.com/?utm_source=8#B_vid=8257970197254429750").read().decode('utf-8')
    print(html)
    pass


