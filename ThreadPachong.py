# coding=utf-8
import os, sys
import pymysql
import time
from fdfs_client.client import *
import threading

print(sys.getdefaultencoding())
import PostGetHttp
import platform
import json
from bs4 import BeautifulSoup
import http.client, urllib, urllib.request
from http.cookiejar import CookieJar
import socket

os.chdir(os.path.dirname(sys.argv[0]))

def get_conn_cur():
    conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    cur = conn.cursor()
    return conn,cur

booking_dest_name = '中国'
booking_dest_type = 'country'

global star_is_3
star_is_3 = False


def country_id_get():
    # 通过search栏输入的字来抽取目的地的信息hotel_name
    dest_parent_url = "http://www.booking.com/autocomplete_2?v=1&lang=zh-cn&sid=b3ec9d4281ab3b1075e2df549a93ff52&" \
                      "aid=304142&pid=151908280f490126&stype=1&src=searchresults&eb=4&e_obj_labels=1&" \
                      "context_dest_type=country&context_dest_id=106&e_tclm=1&add_themes=1&themes_match_start=1&" \
                      "include_synonyms=1&gpf=1&" \
                      "term="


    # 欧洲：德国，法国，英国，瑞典，瑞士，梵蒂冈，丹麦，挪威，芬兰，荷兰，西班牙，爱尔兰
    # 澳新：澳大利亚，新西兰
    # 东南亚：新加坡，泰国，马来西亚，印度尼西亚
    # 北美：加拿大，美国
    # 日韩：日本，韩国
    # 肯尼亚

    countrys = {'德国', '法国', '英国', '瑞典', '瑞士', '意大利', '丹麦', '挪威', '芬兰', '荷兰', '西班牙', '爱尔兰',
                '澳大利亚', '新西兰', '新加坡', '泰国', '马来西亚', '印尼', '加拿大', '美国', '日本', '韩国', '肯尼亚'}

    # 未导入完成
    countrys = []
    # 导入完成
    countrys = ['法国']
    # 导入完成
    countrys = ['芬兰']
    # 导入完成
    countrys = ['德国','英国']
    # 导入完成
    countrys = ['澳大利亚','新西兰']

    # 导入完成
    countrys = ['瑞典','瑞士']

    countrys ={'丹麦','挪威','荷兰','西班牙','爱尔兰','新加坡','泰国', '马来西亚', '加拿大', '美国', '韩国'}

    # 印尼导入完成，日本导入中
    countrys =('印尼','日本')

    countrys =('意大利')
    countrys =['日本']

    # 模拟chrome登陆
    oppener = get_oppener()

    country_id_list = list();
    reginon_type_list = list();
    reginon_name_list = list();

    for countr in countrys:
        reginon_name_list.append(countr)
        dest_url = dest_parent_url + urllib.parse.quote(countr)
        dest_json_str = oppener.open(dest_url).read().decode('utf-8')
        # dest_json_str = urllib.request.urlopen(dest_url).read().decode('utf-8')
        dest_json = json.loads(dest_json_str)

        for city_item in dest_json['city']:
            # 国家的id取出
            if (city_item['dest_type'] == 'country'):
                reginon_type_list.append(city_item['dest_type'])
                country_id_list.append(city_item['dest_id'])
                break

    opener.close()
    return country_id_list,reginon_name_list,reginon_type_list

def get_oppener():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Accept': 'text/html;q=0.9,*/*;q=0.8', 'Accept-Charset': 'utf-8;q=0.7,*;q=0.3',
        'Connection': 'close'}

    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = headers.items()

    return opener

def pics_url_open(hotel_picscr,change=False):

    oppener= get_oppener()
    try:
        if change :
            hotel_picscr_a = hotel_picscr.replace('max400', '840x460')
            pass
        else: hotel_picscr_a = hotel_picscr

        file_array = oppener.open(hotel_picscr_a).read()
        oppener.close()
        return file_array, hotel_picscr_a
    except Exception as err:
        try:
            hotel_picscr_a = hotel_picscr.replace('max400', 'max1024x768')
            fileOpen = oppener.open(hotel_picscr_a).read()
            oppener.close()
            return fileOpen, hotel_picscr_a
        except Exception as err:
            print('图片大小调整为小图')
            try:
                fileOpen = oppener.open(hotel_picscr).read()
                oppener.close()
                return fileOpen, hotel_picscr
            except  Exception as err:
                print(err)
                return None, hotel_picscr
        finally:
            pass
    finally:
        pass
    return None, hotel_picscr


def pics_download(hotel_dest_id, hotel_id, hotel_picscr, type):
    cover, hotel_picscr = pics_url_open(hotel_picscr)

    pic_name = hotel_picscr.split('/').pop()
    path = 'D:/Download' + '/' + hotel_dest_id + '/' + hotel_id + '/'
    cover_path = path + type + '/'
    os.makedirs(cover_path, exist_ok=True)
    f = open(cover_path + pic_name, 'wb+')
    f.write(cover)
    f.flush()
    f.close()

    pass

# 多线程时用
# retrun 0:4星级已经爬完，4:详情页面重试4次退出
def hoteltable_crow(hoteltable):

    conn,cur = get_conn_cur()
    opener = get_oppener()
    global star_is_3
    star_is_3 = False
    try:
        # 酒店名称
        hotel_name = hoteltable.find('span', class_='sr-hotel__name').get_text("", strip=True)
        if len(hotel_name.split('（')) == 2:
            hotel_en_name = hotel_name.split('（')[0]
            hotel_cn_name = hotel_name.split('（')[1]
            hotel_cn_name = hotel_cn_name[0:hotel_cn_name.index('）')]
        else:
            hotel_cn_name = ''
            hotel_en_name = hotel_name

        # 星级
        hotel_star_classes = hoteltable.find('i', class_='star_track')['class']
        hotel_star_class = hotel_star_classes[2]

        hotel_star=int(hotel_star_class.split('_')[2])
        if len(hotel_star_class.split('_')) > 3:
            hotel_star= hotel_star + 0.5

        # if hotel_star!=4.5:
        #     print("星级:" + str(hotel_star))
        #     return 0

        if hotel_star <4:
            print("星级:" + str(hotel_star))
            print("酒店:" + hotel_name)
            print(hotel_star_classes)
            print('结束<><><><><>')
            star_is_3 = True
            # 4星级后的时候，停止循环
            return 0

        # 酒店封面图片
        hotel_picscr = hoteltable.find('img')['src']
        # 酒店点击用标签 a
        hotel_taga = hoteltable.find(class_='sr_item_photo_link')
        hotel_taga_href = hotel_taga['href']

        start = hotel_taga_href.find("dest_id") + 8
        end = hotel_taga_href[start:].find(';')

        hotel_dest_id = hotel_taga_href[start:start + end]

        # 酒店简介
        hotel_desc = hoteltable.find('p', class_='hotel_desc').string
        # 酒店ID
        hotel_id = hoteltable.find('a', class_='jq_tooltip')['id']

        # hotel的详情页面
        hotelclick = "http://www.booking.com" + hotel_taga_href

        print('--------------------------------------------')

        print("详情页面URL:" + str(hotelclick))

        xunhuan=1
        while True:
            try:
                hotelHtml = opener.open(hotelclick,).read().decode('utf-8')
                break
            except Exception as error:
                print("hotelHtml read error")
                print(error)
                xunhuan = xunhuan+1
                if xunhuan == 4:
                    break
                continue
            finally:
                pass
        if xunhuan == 4:
            return 4

        hotelHtmlSoup = BeautifulSoup(hotelHtml, "html.parser")

        # 地址
        hotel_address = hotelHtmlSoup.find(itemprop="address").get_text("", strip=True)
        address_list = hotel_address.split(',')
        country = address_list.pop().strip()

        if country == '日本':
            postcode_city = address_list[0]
            postcode = postcode_city.split(' ')[0]
            city = postcode_city.split(' ')[len(postcode_city.split(' ')) - 1]
            pass
        elif country == '美国':
            city_postcode = address_list.pop()
            city_en_short = city_postcode.split(' ')[0]
            postcode = city_postcode.split(' ')[len(city_postcode.split(' ')) - 1]
            city = address_list.pop()
            pass
        else:
            postcode_city = address_list.pop().strip()
            postcode = postcode_city.split(' ')[0]
            city = postcode_city.split(postcode)[1].strip()

        #
        address_details_html = hotelHtmlSoup.find_all(property="itemListElement")
        address_detail = ''
        for index in range(1, len(address_details_html) - 1):
            if index == len(address_details_html) - 2:
                address_detail = address_detail + address_details_html[index].find('meta', property='name')['content']
                address_detail = address_detail.split('的酒店')[0]
            else:
                address_detail = address_detail \
                                 + address_details_html[index].find('meta', property='name')['content'] \
                                 + ','

            pass

        photos_distinct = hotelHtmlSoup.find(id='photos_distinct')
        if None != photos_distinct:
            photos_a_ss = photos_distinct.find_all('a')
        elif None == photos_distinct:
            photos_a_ss = hotelHtmlSoup.find_all('a', class_='bh-photo-grid-item')

        insert_pic_sql = 'INSERT INTO `traveldb`.`tab_hotel_2_pic` ( `HotelID`, `Url`, `booking_pic_id`, ' \
                         '`booking_pic_url`,`CreateTime`,`UpdateTime`) ' \
                         'VALUES ( %s, %s, %s, %s,NOW(),NOW())'

        insert_sql = "INSERT INTO `traveldb`.`tab_2_hotel` (" \
                     "`HotelName`,`HotelNameCH`,`Address`," \
                     "`Country`,`City`,`Postcode`," \
                     "`ProvidedService`,`Star`,`Abstract`," \
                     "`Source`,`HotelCoverPic`," \
                     "`booking_dest_name`,`booking_dest_id`,`booking_dest_type`," \
                     "`booking_hotel_id`,`booking_hotel_url`,`CreateTime`," \
                     "`UpdateTime`,`AddressDetail`" \
                     ")" \
                     " VALUES" \
                     "(%s,%s,%s," \
                     "%s,%s,%s," \
                     "%s,%s,%s," \
                     "%s,%s," \
                     "%s,%s,%s," \
                     "%s,%s,NOW()," \
                     "NOW(),%s)"

        #介绍的html节点
        hotel_desc_summary = hotelHtmlSoup.find(id='summary')
        hp_desc_important_facilities = hotelHtmlSoup.find(class_='hp_desc_important_facilities')
        if None != hp_desc_important_facilities:
            facilities_strings = hp_desc_important_facilities.get_text(',', strip=True)
        else:
            facilities_strings = ''
        delete_itme = hotel_desc_summary.find('span', class_='city_centre_map_link')
        if None != delete_itme:
            # 移除文档树
            delete_itme.decompose()
        # 简介详情
        hotel_desc_main = hotel_desc_summary.get_text("\n", strip=True)

        # pics_download(hotel_dest_id, hotel_id, hotel_picscr, 'cover')
        cover_id, hotel_picscr = file_upload(hotel_picscr)
        # print("图片url：" + cover_id)
        cur.execute(insert_sql, (hotel_en_name, hotel_cn_name, hotel_address,
                                 country, city, postcode,
                                 facilities_strings, str(hotel_star), hotel_desc_main,
                                 'www.booking.com', cover_id,
                                 reginon_name, hotel_dest_id, reginon_type,
                                 hotel_id, hotelclick, address_detail))

        cur.execute('SELECT LAST_INSERT_ID() as abc')
        last_insert_id = cur.fetchall()[0][0]

        photo_dict = {}
        for photos_a in photos_a_ss:

            if photos_a.has_attr('data-photoid'):
                photo_id = photos_a['data-photoid']

                # 取得是小图的地址
                photo_dict[photo_id] = photos_a['href']
                #将小图片换成大图片
                #大图： http://r-cc.bstatic.com/images/hotel/840x460/139/13918168.jpg

                #小图： http://q-cc.bstatic.com/images/hotel/max400/139/13918842.jpg
                if 'http' not in photo_dict[photo_id]:
                    photo_dict.pop(photo_id)
                else:
                    # 下载到本地的功能
                    # pics_download(hotel_dest_id, hotel_id, photo_dict[photo_id], 'pics')
                    file_id, pic_url = file_upload(photo_dict[photo_id],True)
                    # print("图片url：" + file_id)
                    cur.execute(insert_pic_sql, (last_insert_id, file_id, photo_id, pic_url))


            elif photos_a.has_attr('data-id'):
                photo_id = photos_a['data-id']
                photo_dict[photo_id] = photos_a['href']
                # 下载到本地的功能
                # pics_download(hotel_dest_id, hotel_id, photo_dict[photo_id], 'pics')
                file_id, pic_url = file_upload(photo_dict[photo_id])
                # print("图片url：" + file_id)
                cur.execute(insert_pic_sql, (last_insert_id, file_id, photo_id, pic_url))

        print('酒店:' + hotel_name)
        # print('酒店封面图片:' + hotel_picscr)
        # print('酒店简介:')
        # print(hotel_desc)
        # print('酒店简介详情:')
        # print(hotel_desc_main)
        # print('酒店ID:' + hotel_id)
        print('星级:' + str(hotel_star))
        # print('酒店地址:' + hotel_address)
        # print("图片：")
        # print(photo_dict)
        print("目的地ID：" + hotel_dest_id)

        print('--------------------------------------------')

    except Exception as err:
        print('hoteltable_crow:')
        print(err)
        return 0
    finally:
        sys.stdout.flush()
        opener.close()
        conn.commit()
        cur.close()
        conn.close()

    return 1

def detail_crow(html):
    soup = BeautifulSoup(html, "html.parser")

    hoteltables = soup.find_all(class_="sr_item_new")
    threads =[]
    for hoteltable in hoteltables:
        t = threading.Thread(target=hoteltable_crow,args=(hoteltable,))
        t.setDaemon(True)
        threads.append(t)

    for tread in threads:
        tread.start()
    for tread in threads:
        tread.join()

    return 1


def file_upload(hotel_picscr,change=False):
    # return 'group/test','http:/ddedd'
    photoOpen, pic_url = pics_url_open(hotel_picscr,change)
    pic_name = pic_url.split('/').pop()

    client_file = 'fdfs_client.conf'
    client = Fdfs_client(client_file)

    try:
        # upload
        if None == photoOpen:
            return 'error', pic_url

        ret_upload = client.upload_by_buffer(photoOpen, pic_name.split('.')[1], {"fileName": pic_name})
        # print (ret_upload)

        file_id = ret_upload['Remote file_id'].replace('\\', '/')  # 新版本文件存放Remote file_id格式变化

        # download
        # ret_download=client.download_to_file(download_file,file_id)
        # print (ret_download)

        #delete
        # ret_delete=client.delete_file(file_id)

        # print (ret_delete)
        return file_id, pic_url
    except Exception as ex:
        print(ex)
        return 'error', pic_url
    pass

if __name__ == '__main__':

    opener = get_oppener()
    socket.setdefaulttimeout(5)

#     html = opener.open('http://www.booking.com/searchresults.zh-cn.html?label=gen173nr-1FCAQoggJCC2NvdW50cnlfMTUySCtiBW5vcmVmaDGIAQGYATLCAQNhYm7IAQzYAQHoAQH4AQOoAgQ;sid=672bf07805ce688dd2968ac88752939a;class_interval=1;dest_id=152;dest_type=country;hlrd=0;label_click=undef;order=class;review_score_group=empty;room1=A%2CA;sb_price_type=total;score_min=0;ssb=empty;rows=15;offset=750').read().decode('utf-8')
#     # 到达3星级酒店的时候，跳到下一个国家
#     soup = BeautifulSoup(html, "html.parser")
#
#     hoteltables = soup.find_all(class_="sr_item_new")
# # 爬取信息
#     _break = hoteltable_crow(hoteltables[0])
#     reginon_type = 'cdcc'
#     reginon_name = 'dfsfd'
#     sys.exit(0)

    # 国家ID取得
    country_id_list,country_name_list,country_type_list = country_id_get()

    # 全局变量 目的地名，目的地类型
    index = 0

    for country_id in country_id_list:
        global star_is_3
        star_is_3 = False
        reginon_type = country_type_list[index]
        reginon_name = country_name_list[index]
        index = index+1
        # 通过国家ID来抽取酒店的列表信息
        next_page_url = 'http://www.booking.com/searchresults.zh-cn.html?dest_id=' \
                        + country_id + \
                        '&dest_type=country&order=class'
        # 按星级抽取
        # &nflt=class=4
        sys.stdout = open(reginon_name+'.detail2.txt', 'a+', encoding='utf8')
        print("page:" + str(1) + ':' + next_page_url)
        sys.stdout.flush()
        page = 1
        while True:
            html = opener.open(next_page_url).read().decode('utf-8')
            # 到达3星级酒店的时候，跳到下一个国家
            if star_is_3 == True:
                break
            # 爬取信息
            _break = detail_crow(html)
            # 如果过了要求的星级，就停止循环
            if _break == 0:
                opener.close()
                sys.stdout.close()
                break

            page = page + 1

            soup = BeautifulSoup(html, "html.parser")
            page_result = soup.find(class_="results-paging")
            next = page_result.find(class_='paging-next')
            if next == None: break
            next_page_url = 'http://www.booking.com' + page_result.find(class_='paging-next')['href']
            print("page:" + str(page) + ':' + next_page_url)
            sys.stdout.flush()

        sys.stdout.close()
    # 通过城市ID来取得酒店列表信息
    # url='http://www.booking.com/searchresults.zh-cn.html?dest_id=-1353149&dest_type=city&order=class&rows=15'
    opener.close()
    sys.stdout.close()
