__author__ = 'zhwang.kevin'
import os, sys
import http.client, urllib, urllib.request


def encode_multipart_formdata(fields):
    '''''
            该函数用于拼接multipart/form-data类型的http请求中body部分的内容
            返回拼接好的body内容及Content-Type的头定义
    '''
    import random
    import os

    BOUNDARY = '----------%s' % ''.join(random.sample('0123456789abcdef', 15))
    CRLF = b'\r\n'
    L = []
    for key, value in fields.items():
        if (type(value) == type(['abc', 'der'])):
            pass
        else:
            value = [value]
        for item in value:
            filepath = isfiledata(item)
            if filepath:
                L.append(('--' + BOUNDARY).encode('UTF8'))
                L.append(('Content-Disposition: form-data; name="%s"; filename="%s"' % (
                key, os.path.basename(filepath))).encode('UTF8'))
                L.append(('Content-Type: %s' % get_content_type(filepath)).encode('UTF8'))
                L.append(''.encode('UTF8'))
                L.append(ReadFileAsContent(filepath))
            else:
                L.append(('--' + BOUNDARY).encode('UTF8'))
                L.append(('Content-Disposition: form-data; name="%s"' % key).encode('UTF8'))
                L.append(''.encode('UTF8'))
                L.append(item.encode('UTF8'))
    L.append(('--' + BOUNDARY + '--').encode('UTF8'))
    L.append(''.encode('UTF8'))

    # for abcd in L:
    # body=body+abcd+CRLF

    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


def encode_multipart_formdata_onefile(fields):
    '''''
            该函数用于拼接multipart/form-data类型的http请求中body部分的内容
            返回拼接好的body内容及Content-Type的头定义
    '''
    import random
    import os

    BOUNDARY = '----------%s' % ''.join(random.sample('0123456789abcdef', 15))
    CRLF = b'\r\n'
    L = []
    for key, value in fields.items():
        if (type(value) == type(['abc', 'der'])):
            pass
        else:
            value = [value]
        for item in value:
            L.append(('--' + BOUNDARY).encode('UTF8'))
            L.append(
                ('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, 'spots.jpg')).encode(
                    'UTF8'))
            L.append(('Content-Type: image/jpeg' ).encode('UTF8'))
            L.append(''.encode('UTF8'))
            L.append(item)

    L.append(('--' + BOUNDARY + '--').encode('UTF8'))
    L.append(''.encode('UTF8'))

    # for abcd in L:
    # body=body+abcd+CRLF

    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


def get_content_type(filename):
    import mimetypes

    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def isfiledata(p_str):
    # import re
    rert = os.path.exists(p_str)
    # r_c = re.compile("^f'(.*)'$")
    # rert = r_c.search(str(p_str))
    # rert = re.search("^f'(.*)'$", p_str)
    if rert:
        return p_str
    else:
        return None


def ReadFileAsContent(filename):
    # print filename
    try:
        with open(filename, 'rb') as f:
            filecontent = f.read()
    except Exception as e:
        print('The Error Message in ReadFileAsContent(): ' + e.message)
        return ''
    return filecontent


def gethttp(host, port, url):
    httpClient = None
    try:
        httpClient = http.client.HTTPConnection(host, port, timeout=300)
        httpClient.request('GET', url, None, {'Content-Type': 'text/html; charset=utf-8'})
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        # print(response.status)
        # print(response.reason)
        # #此处很重要，decode必不可少
        strrespose = response.read().decode('utf-8')
        # print(strrespose)
        return strrespose
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


def posthttp(form, url):
    httpClient = None

    try:
        contenttype, body = encode_multipart_formdata(form)
        headers = {"Content-type": contenttype,
                   "Accept": "application/json;charset=UTF-8"}
        req = urllib.request.Request(url=url, data=body, headers=headers)
        # print(req)
        res_data = urllib.request.urlopen(req)
        jsonstr = res_data.read().decode('utf-8')
        # print(jsonstr)
        # print(res_data.status)
        # print(res_data.reason)
        # print(res_data.getheaders())  # 获取头信息
        return jsonstr
    except Exception as e:
        print(e)

    finally:
        if httpClient:
            httpClient.close()

def posthttp_onefile(form, url):
    httpClient = None

    try:
        contenttype, body = encode_multipart_formdata_onefile(form)
        headers = {"Content-type": contenttype,
                   "Accept": "application/json;charset=UTF-8"}
        req = urllib.request.Request(url=url, data=body, headers=headers)
        res_data = urllib.request.urlopen(req)
        jsonstr = res_data.read().decode('utf-8')
        return jsonstr
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
