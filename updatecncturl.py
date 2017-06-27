__author__ = 'zhwang.kevin'
import pymysql
import csv

def get_conn_cur_163():
    #inner net or outer net
    # conn = pymysql.connect(host='114.55.139.196', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
    #                        charset='UTF8')
    conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    cur = conn.cursor()
    conn.autocommit(0)
    return conn, cur

def get_conn_cur_196():
    #inner net or outer net
    conn = pymysql.connect(host='114.55.139.196', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
                           charset='UTF8')
    # conn = pymysql.connect(host='10.101.1.163', port=3306, user='traveldb', passwd='traveldb', db='traveldb',
    #                        charset='UTF8')
    cur = conn.cursor()
    conn.autocommit(1)
    return conn, cur

def getUpdateSql():
    sql = 'update traveldb.tab_travelregion region ' \
          'set region.RegionPicUrl = %s WHERE region.RegionID = %s '
    return sql

def updateQYpic2Null():

    # SELECT
    # region.RegionCnName,
    # parent.RegionCnName parentName
    # FROM
    # traveldb.tab_travelregion region,
    # traveldb.tab_placeicon_copy icon,
    # traveldb.tab_travelregion parent
    # WHERE
    # region.RegionCnName = icon.PlaceName
    # AND region.ParentID = parent.RegionID
    # AND icon.PlaceParent = parent.RegionCnName
    # AND region.RegionCnName != ''
    # AND icon.qypicurl = 'http://static.qyer.com/images/place/no/poi_80_80.png'
    # UNION ALL
    # SELECT
    # region.RegionCnName,
    # null parentName
    # FROM
    # traveldb.tab_travelregion region,
    # traveldb.tab_placeicon_copy icon
    # WHERE
    # region.RegionCnName = icon.PlaceName
    # AND ParentID = 0
    # AND region.RegionCnName != ''
    # AND icon.qypicurl = 'http://static.qyer.com/images/place/no/poi_80_80.png'


    updateSql = "update traveldb.tab_travelregion region,traveldb.tab_travelregion parent " \
                "set region.RegionPicUrl = null " \
                " WHERE ((region.ParentID = parent.RegionID  and parent.RegionCnName = %s) ) and " \
                "region.RegionCnName = %s"


    updateSql = "update traveldb.tab_travelregion region " \
                "set region.RegionPicUrl = null " \
                " WHERE region.ParentID=0 and " \
                " region.RegionCnName = %s"

    # OR region.ParentID = 0
    import csv
    conn196,cur196 = get_conn_cur_196()

    with open("file\qingyoutupian.csv") as f:
        temp = csv.reader(f)
        for row in temp:
            count = cur196.execute(updateSql, (row[0], ))
            print(row[0])
            print(count)
        cur196.close()
        conn196.close()

if __name__ == '__main__':


    updateQYpic2Null()
    # conn163, cur163 = get_conn_cur_163()
    # with open("file\countrycityurl.csv") as f:
    #     temp = csv.reader(f)
    #     for row in temp:
    #         cur163.execute(getUpdateSql(), (row[3], row[0]))
    # conn163.commit()
    # conn163.close()


#     UPDATE traveldb.tab_travelregion region,
# traveldb.tab_placeicon icon,
# traveldb.tab_travelregion parent
# SET region.RegionPicUrl = icon.PlacePicUrl
# WHERE
# region.RegionCnName = icon.PlaceName
# AND region.ParentID = parent.RegionID
# AND icon.PlaceParent = parent.RegionCnName
# AND region.RegionCnName != ''
# AND (
#     region.RegionPicUrl = ''
# OR region.RegionPicUrl IS NULL
# )
# AND (
#     INSTR(
#         region.RegionCnName,
#         icon.PlaceName
#     ) > 0
# OR INSTR(
#     icon.PlaceName,
#     region.RegionCnName
# ) > 0
# );

