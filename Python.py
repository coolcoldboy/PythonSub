# coding=utf-8
import os, sys

print(sys.getdefaultencoding())
import PostGetHttp
import platform
import json
import pymysql
from bs4 import BeautifulSoup
import http.client, urllib, urllib.request
from fdfs_client.client import *
import time
import six
os_sep = '/'



os.chdir(os.path.dirname(sys.argv[0]))


def hello_world():
    print('Hello World!')
    s = '\xe8\xb4\x9d\xe5\xa1\x94'
    s = u'我的天'
    s.encode('utf8')
    print(s)


def mtest():
    form = {'name': ['21我的天', '我的天'],
            'SpotsID': '22',
            'NameEn': 'werf',
            'NameCh': '生命',
            'Status': '1'}

    tupian = {'file': ['C:\\Users\\Public\\Pictures\\Sample Pictures\\Tulips.jpg',
                       'C:\\Users\\Public\\Pictures\\Sample Pictures\\Tulips.jpg'],
              'coverFile': 'C:\\Users\\Public\\Pictures\\Sample Pictures\\Tulips.jpg'}
    dictMerged2 = dict(form, **tupian)
    str = PostGetHttp.posthttp(dictMerged2, 'http://localhost:8080/travel/user/test')
    return json.loads(str)


def applyCash():
    form = {'UserID': '10063',
            'withdrawMoney': '200',
            'remark': 'cash',
            'userNameOfAccount': '王',
            'bankName': '招商银行',
            'accountNum': '622501254862588',
            'commission': '8',
            'payAccountNum': '622825685741',
            'payUserName': '吴',
            'payBankName': '招商银行',
            'feeRate': '0.01',
    }
    str = PostGetHttp.posthttp(form, 'http://localhost:8080/travel/order/applyCash')
    return json.loads(str)


def updateCashStatus():
    form = {'UserID': '10063',
            'cashID': '2',
            'status': '2',
            'commission': '8',
            'payAccountNum': '622825685741',
            'payUserName': '吴',
            'payBankName': '招商银行',
            'feeRate': '0.01',
            'operateUserID': '10055'
    }
    str = PostGetHttp.posthttp(form, 'http://localhost:8080/travel/order/updateCashStatus')
    return json.loads(str)


def mguideorderlist():
    str = PostGetHttp.gethttp('localhost', '8080', '/travel/order/guideorderlist?'
                              + 'userName=2721&mobile=0')
    return json.loads(str)


def mgetadjustmoneylist():
    str = PostGetHttp.gethttp('localhost', '8080', '/travel/order/getadjustmoneylist?'
                              + 'userID=2721&status=0')
    return json.loads(str)


def mgetCashList():
    str = PostGetHttp.gethttp('localhost', '8080', '/travel/order/getCashList?'
                              + 'cashID=1&status=1&guiderID=1')
    return json.loads(str)


def mgetBankList():
    str = PostGetHttp.gethttp('localhost', '8080', '/travel/order/getBankList?'
    )
    return json.loads(str)


def mgetWalletDetail():
    str = PostGetHttp.gethttp('localhost', '8080', '/travel/order/getWalletDetail?'
                              + 'userID=2726&page=1')
    return json.loads(str)


def mgetBankAccountList():
    str = PostGetHttp.gethttp('localhost', '8080', '/travel/order/getBankAccountList?'
                              + 'userID=2726')
    return json.loads(str)


def mgetWalletNumBerItem():
    str = PostGetHttp.gethttp('localhost', '8080', '/travel/order/getWalletNumBerItem?'
                              + 'userID=2726&serialNumber=201608311954115617')
    return json.loads(str)


def mgetCashDetailByCashNo():
    str = PostGetHttp.gethttp('10.101.1.165', '8888', '/travel/order/getCashDetailByCashNo?'
                              + 'cashNo=CA201609201739336992')
    return json.loads(str)


def mgetWalletNumBer():
    str = PostGetHttp.gethttp('10.101.1.165', '8888', '/travel/order/getWalletDetail?'
                              + 'userID=10063&page=1')


def mgettest():
    # form = {'name': '2721'}
    # str = PostGetHttp.posthttp(form,'http://localhost:8080/travel/user/gettest')

    str = PostGetHttp.gethttp('localhost', '8080', '/travel/user/gettest?'
                              + 'name=汪&page=1')
    return json.loads(str)


def mgetMyCalendar():
    str = PostGetHttp.gethttp('localhost', '8080', '/travel/user/getMyCalendar?'
                              + 'guiderID=10023')
    return json.loads(str)


def mcallRefund():
    form = {'orderID': '306',
            'orderNO': '201608311946349669',
            'batchNum': '1',
            'reason': '没有成团',
            'touristRefund': '0.01',
            'ProviderRefund': '0',
            'PlatformRefund': '0',
            'operatorID': '10063',


    }
    str = PostGetHttp.posthttp(form, 'http://10.101.1.165:8888/apply/pay/callRefund')
    return json.loads(str)


def msetShieldMyCalendar():
    form = {'GuideID': '10063',
    }
    str = PostGetHttp.posthttp(form, 'http://localhost:8080/travel/user/setShieldMyCalendar')
    return json.loads(str)


def mgetVerifyImf():
    str = PostGetHttp.gethttp('10.101.1.165', '8888', '/travel/user/getVerifyImf?' +
                              'userID=2726'
    )
    return json.loads(str)


def mgetbooking():
    str = PostGetHttp.gethttp('www.booking.com', None, "/hotel/jp/the-windsor-toya-resort-spa.zh-cn.html?label=gen173nr-1FCAQoggJCC2NvdW50cnlfMTA2SCtiBW5vcmVmaDGIAQGYATLCAQNhYm7IAQzYAQHoAQH4AQOoAgQ;sid=718527c0a27d241dded2b9240b0355b8;ucfs=1;room1=A,A;dest_type=country;dest_id=106;srfid=b3812e3e0e7d34f30972e7b91c257c0fc6b91a57X13"
    )
    return json.loads(str)

def mvisitororderdetail():
    # form = {'name': '2721'}
    # str = PostGetHttp.posthttp(form,'http://localhost:8080/travel/user/gettest')

    str = PostGetHttp.gethttp('localhost', '8080', '/travel/order/visitororderdetail?'
                              + 'orderId=571')
    return json.loads(str)

def msearchUserByZonAndMob():
    # form = {'name': '2721'}
    # str = PostGetHttp.posthttp(form,'http://localhost:8080/travel/user/gettest')

    str = PostGetHttp.gethttp('localhost', '8080', '/travel/order/searchUserByZonAndMob?'
                              + 'zoneCode=0086&mobile=7177')
    return json.loads(str)

def mupdateOrderTest():
    form = {'orderid': ['10063','10064'],
            'status': ['0','1']
            }
    str = PostGetHttp.posthttp(form, 'http://localhost:8080/travel/order/updateOrderTest')
    return json.loads(str)


def mgettest():
    form = {'Name': '2721',
            'Name':'wang'}
    headers = {'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
               "Accept": "application/json;charset=UTF-8",
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
    url = 'http://localhost:8080/travel/user/gettest'

    req = urllib.request.Request(url=url, data=urllib.parse.urlencode(form).encode('utf-8'), headers=headers,method='POST')
    str = urllib.request.urlopen(req).read().decode('utf-8')
    # str = PostGetHttp.posthttp(form,'http://localhost:8080/travel/user/gettest')
    pass

def mgettestjson():
    form = {'hasLanguage': '英语,日语',
            'hasLanguageForshow':[{'item1':'英语','item2':'fa'},{'item1':'ri','item2':'he'}],
            'picurls':['swooefe/dkd.jpg','swodddae/dcd.jpg']}
    headers = {'Content-Type':'application/json',
               "Accept": "application/json;charset=UTF-8",
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
    url = 'http://localhost:8080/travel/user/gettestjson'
    form = json.dumps(form)
    req = urllib.request.Request(url=url, data=form.encode("utf-8"), headers=headers,method='POST')
    str = urllib.request.urlopen(req).read().decode('utf-8')
    # str = PostGetHttp.posthttp(form,'http://localhost:8080/travel/user/gettest')
    pass

    print(str)
    return json.loads(str)

def mexecuteRefund():
    str = urllib.request.urlopen('http://localhost:8080/travel/aptest/executeRefund').read().decode('utf-8')

def mgetPlannerName():
    str = urllib.request.urlopen('http://localhost:8080/travel/user/getPlannerName?mobileNum=13671771921').read().decode('utf-8')
    print(str)

def mgettravellingbag():
    str = urllib.request.urlopen('http://localhost:8080/travel/travellingbag/gettravellingbag?userID=10063').read().decode('utf-8')
    print(str)

if __name__ == '__main__':

    mgettravellingbag()

    exit()
    # PostGetHttp.gethttp('localhost','8080','/travel/order/orderDetailForBKM?'
    # +'orderID=324&orderType=2')
    # PostGetHttp.gethttp('10.101.1.165','8888','/travel/order/visitororderlist?'
    # +'userID=2721&status=0&page=1')
    #


    # jsonobj= mguideorderlist()
    # jsonobj = mtest()
    # jsonobj = mgetbooking()
    # print(jsonobj)


    # conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
    #                        charset='UTF8')
    # cur = conn.cursor()
    # cur.execute("select version()")
    # conn.commit()
    # for i in cur:
    #     print(i)
    # cur.close()
    # conn.close()
    #
    # hotel_picscr='http://r-cc.bstatic.com/images/hotel/square200/139/13918842.jpg'
    #
    # cover = urllib.request.urlopen(hotel_picscr)
    # pic_name = hotel_picscr.split('/').pop()
    # path = 'D:/Download'+'/'+'123'+'/'+'2321'+'/'
    # os.makedirs(path,exist_ok=True)
    # f = open(path+pic_name,'wb+')
    # f.write(cover.read())
    # f.flush()
    # f.close()
    # cover.close()

    hotel_picscr = '222840x4603333'
    hotel_picscr.replace('840x460','max1024x768')
    hotel_picscr.replace('max1024x768','max400')

    send_buffer = struct.pack('!Q Q c 16s', 44,21,b'0',b'group1')

    send_buffer = struct.pack('!Q Q c 16s 44s 21s', 44,21,b'0',b'group1',
                              b'M00/06/E8/CmUBpVf_Q76AS3jhAABO9Nigqbg929.jpg',
                              b'fileName43062953.jpg')


    file = urllib.request.urlopen('http://r-cc.bstatic.com/images/hotel/max400/430/43062953.jpg')

    client_file='fdfs_client.conf'
    test_file='test.txt'
    download_file='test2.txt'

    try:
        client = Fdfs_client(client_file)
        #upload

        ret_upload = client.upload_by_buffer(file.read(),'jpg',{"fileName":"43062953.jpg"})
        print (ret_upload)

        time.sleep(1)   #等待5s，否则下载时会报错文件不存在
        file.close()
        file_id=ret_upload['Remote file_id'].replace('\\','/')  #新版本文件存放Remote file_id格式变化

        #download
        # ret_download=client.download_to_file(download_file,file_id)
        # print (ret_download)

        #delete
        ret_delete=client.delete_file(file_id)

        print (ret_delete)

    except Exception as ex:
        print (ex)

    # path = 'D:/Download'+'/'+'123'+'/'+'45'+'/'
    # os.makedirs(path,exist_ok=True)
    # f = open(path+'1.jpg','wb')
    #
    # f.close()
    # 模拟chrome登陆
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    #     'Accept': 'text/html;q=0.9,*/*;q=0.8', 'Accept-Charset': 'utf-8;q=0.7,*;q=0.3',
    #     'Connection': 'close'}
    #
    # opener = urllib.request.build_opener()
    # opener.addheaders = headers.items()
    #
    # hotelHtml = opener.open(
    #     'http://www.booking.com/hotel/jp/keio-plaza-tokyo.zh-cn.html?label=gen173nr-1FCAQoggJCC2NvdW50cnlfMTA2SCtiBW5vcmVmaDGIAQGYATLCAQNhYm7IAQzYAQHoAQH4AQOoAgQ;sid=b23ba36a407c172ed759586ddb142cea;ucfs=1;room1=A,A;dest_type=country;dest_id=106;srfid=b3812e3e0e7d34f30972e7b91c257c0fc6b91a57X3').read().decode(
    #     'utf-8')
    # hotelHtmlSoup = BeautifulSoup(hotelHtml, "html.parser")
    #
    # # 地址
    # hotel_address = hotelHtmlSoup.find(itemprop="address").string
    # photos_distinct = hotelHtmlSoup.find(id='photos_distinct')
    # if None != photos_distinct:
    #     photos_a_ss = photos_distinct.find_all('a')
    # elif None == photos_distinct:
    #     photos_a_ss = hotelHtmlSoup.find_all('a', class_='bh-photo-grid-item')
    # photo_dict = {}
    # for photos_a in photos_a_ss:
    #
    #     if photos_a.has_attr('data-photoid'):
    #         photo_id = photos_a['data-photoid']
    #     elif photos_a.has_attr('data-id'):
    #         photo_id = photos_a['data-id']
    #
    #     photo_dict[photo_id] = photos_a['href']
    #
    # hotel_desc_summary = hotelHtmlSoup.find(id='summary')
    # hotel_desc_main=hotel_desc_summary.get_text()
    #
    # deleteitme = hotel_desc_summary.find('span',class_='city_centre_map_link')
    # if(None != deleteitme):
    #     # 移除文档树
    #     deleteitme.decompose()
    #
    # deleteitme = hotel_desc_summary.find('span',class_='city_centre_map_link')

    # PostGetHttp.gethttp('10.101.1.165','8888','/travel/order/visitororderlist?'
    #         +'userID=2721&status=0')
    # hello_world()
# hello_world()
# print ('"Hello World!"')
#     a=3
#     if a==2:
#         print('2')
#     elif a==3:
#         print('3')
#     a=5
#     while a>0:
#         a=a-1
#         print(a)
#     for i  in  range(6,10):
#         print(i)
#     array = {'China',
#              'America','England'}
#
#     for aitem  in  array:
#         print(aitem)
#
#     f=open('Python.py','r+')
#     print(f.readlines())
#     path1=os.getcwd()
#     path2=sys.argv[0]
#     print(path2)
#
#     name = input("Name:\n")
#     print(name)












