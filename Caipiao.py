# coding=utf-8
from bs4 import BeautifulSoup

__author__ = 'zhwang.kevin'

import CommonRequest
import zlib

opener = CommonRequest.get_oppener()

response = opener.open("http://datachart.500.com/dlt/?expect=100",)

# response.info().get('Content-Encoding')

decompressed_data = zlib.decompress(response.read(), 16+zlib.MAX_WBITS)
hotelHtml = decompressed_data.decode('gb2312')
# hotelHtml = hotelHtml.encode('raw_unicode_escape')
hotelHtmlSoup = BeautifulSoup(hotelHtml, "html.parser")
menuitem = hotelHtmlSoup.findAll(id='menuitem')[0]
tds_center = menuitem.find_all('td', align='center')
for tdcenter in menuitem:
    print(repr(tdcenter))
    pass
# hotel_address = hotelHtmlSoup.find(itemprop="address").get_text("", strip=True)