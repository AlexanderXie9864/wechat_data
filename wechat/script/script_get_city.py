#!/usr/bin/env python3
# coding=utf-8
# __author__: Alexander
from xml.etree.ElementTree import parse
from pyecharts.datasets.coordinates import get_coordinate, search_coordinates_by_region_and_keyword
import pymysql as py
from wechat.script.script_get_translation import translateYoudao

conn = py.connect('10.127.105.233', "root", "yuanfang123", "wechat_data", charset='utf8')
cursor = conn.cursor()


def get_chinese_city():
    chinese = open(r"H:\项目\毕业设计\location.xml", encoding='utf8')
    et = parse(chinese)
    root = et.getroot()
    for country in root.iterfind('CountryRegion'):
        # print("国家:"+country.get("Name"))
        if country.get("Name") == "中国":
            for state in country.iterfind('State'):
                print("州、省：" + state.get("Name"))
                for city in state.iterfind('City'):
                    sql = ("""SELECT lng FROM wechat_citylal WHERE city=%s AND province=%s AND country='中国'""")
                    param = (city.get("Name"), state.get("Name"))
                    cursor.execute(sql, param)

                    if not cursor.rowcount:
                        sql = ("""INSERT INTO wechat_citylal(city,province,country,
                         lng,lat)
                         VALUES (%s,%s,'中国',%s,%s)""")
                        lal = (city.get("Name"), state.get("Name"), 0, 0)
                        try:
                            cursor.execute(sql, lal)
                            print("城市：" + city.get("Name")+"    省/行政区/直辖市："+state.get("Name"))
                        except Exception as e:
                            print(e)
                            conn.rollback()
                print("\t")
        break
    conn.commit()


def get_foreign_city():
    english = open(r"H:\项目\毕业设计\location_e.xml", encoding='utf8')
    et_e = parse(english)
    root_e = et_e.getroot()
    for country in root_e.iterfind('CountryRegion'):
        print("国家" + country.get("Name"))
        if country.get("Name") == "China":
            continue
        region = translateYoudao(country.get('Name'))
        region = region[0]
        for state in country.iterfind('State'):
            if state.get("Name"):
                print("州、省：" + state.get("Name"))
            for city in state.iterfind('City'):
                try:

                    sql = ("""SELECT lng FROM wechat_citylal WHERE city=%s AND province=%s AND country=%s """)
                    if state.get("Name"):
                        state_name = state.get("Name")
                    else:
                        state_name = '无'
                    param = (city.get("Name"), state_name, region)
                    cursor.execute(sql, param)
                    if not cursor.rowcount:
                        print(city.get("Name"))
                        sql = ("""INSERT INTO wechat_citylal(city,province,country,
                                                    lng,lat)
                                                    VALUES (%s,%s,%s,%s,%s)""")
                        lal = (city.get("Name"), state_name, region, 0, 0,)
                        try:
                            cursor.execute(sql, lal)  # 可添加特殊字符
                            if state.get("Name"):
                                print("城市：" + city.get("Name") + '   州：'+state.get("Name") + '   国家：'+country.get("Name"))
                            else:
                                print("城市：" + city.get("Name") + '   州：' + '无' + '   国家：' + country.get(
                                    "Name"))
                        except Exception as e:
                            print("error:城市：" + city.get("Name") + " info: " + str(e))
                            conn.rollback()
                except Exception as e:
                    print('error：' + str(e))
                    continue
            print("\t")
            conn.commit()


def get_chinese_city_lal():
    chinese = open(r"H:\项目\毕业设计\location.xml", encoding='utf8')
    et = parse(chinese)
    root = et.getroot()
    for country in root.iterfind('CountryRegion'):
        # print("国家:"+country.get("Name"))
        if country.get("Name") == "中国":
            for state in country.iterfind('State'):
                if state.get("Name") == "香港" \
                        or state.get("Name") == "澳门" \
                        or state.get("Name") == "上海" \
                        or state.get("Name") == "天津" \
                        or state.get("Name") == "重庆" \
                        or state.get("Name") == "北京":
                    print("直辖市/特别行政区： " + state.get("Name"))
                    continue
                print("州、省：" + state.get("Name"))
                for city in state.iterfind('City'):
                    coordinate = get_coordinate(city.get("Name"), "中国")
                    # coordinate = search_coordinates_by_region_and_keyword("中国", city.get("Name"), state.get("Name"))
                    if coordinate:
                        sql = ("""INSERT INTO wechat_citylal(city,province,country,
                         lng,lat)
                         VALUES ('%s','%s','中国','%s','%s')""")
                        lal = (city.get("Name"), state.get("Name"), coordinate[0], coordinate[1])
                        try:
                            cursor.execute(sql % lal)
                            print("城市：" + city.get("Name") + str(coordinate))
                        except Exception as e:
                            print(e)
                            conn.rollback()
                print("\t")
        break
    conn.commit()

def get_UK_city_lal():
    sql = ("""SELECT city,lng FROM wechat_citylal WHERE country='英国' """)
    cursor.execute(sql)
    result = list(cursor.fetchall())
    for data in result:

        coordinate = get_coordinate(data[0], "英国")
        if coordinate:
            sql = ("""UPDATE wechat_citylal SET lng=%s,lat=%s WHERE country='英国' AND city=%s""")
            lal = (coordinate[0], coordinate[1], data[0])
            try:
                cursor.execute(sql, lal)
                print("城市：" + data[0] + str(coordinate))
            except Exception as e:
                print(e)
                conn.rollback()
        else:
            sql = ("""UPDATE wechat_citylal SET lng=0, lat=0 WHERE country='英国' AND city=%s""")
            lal = (data[0])
            try:
                cursor.execute(sql, lal)
                print("城市：" + data[0] + str(coordinate))
            except Exception as e:
                print(e)
                conn.rollback()

    conn.commit()
    # print(result)
def get_foreign_city_lal():
    english = open(r"H:\项目\毕业设计\location_e.xml", encoding='utf8')
    et_e = parse(english)
    root_e = et_e.getroot()
    for country in root_e.iterfind('CountryRegion'):
        print("国家" + country.get("Name"))
        if country.get("Name") == "China":
            continue
        for state in country.iterfind('State'):
            if state.get("Name"):
                print("州、省：" + state.get("Name"))
            for city in state.iterfind('City'):
                try:
                    region = translateYoudao(country.get('Name'))
                    region = region[0]
                    coordinate = get_coordinate(city.get("Name"), region=region)
                    if coordinate:
                        print(city.get("Name"))
                        sql = ("""INSERT INTO wechat_citylal(city,province,country,
                                                lng,lat)
                                                VALUES (%s,%s,%s,%s,%s)""")

                        if state.get("Name"):
                            lal = (city.get("Name"), state.get("Name"), region, coordinate[0], coordinate[1],)
                        else:
                            lal = (city.get("Name"), '无', region, coordinate[0], coordinate[1],)
                        try:
                            cursor.execute(sql, lal)  # 可添加特殊字符
                            print("城市：" + city.get("Name") + str(coordinate))
                        except Exception as e:
                            print("error:城市：" + city.get("Name") + str(coordinate)+str(e))
                            conn.rollback()
                except Exception as e:
                    print('error：'+str(e))
                    continue
            print("\t")
            conn.commit()

def revoke_before():
    english = open(r"H:\项目\毕业设计\location_e.xml", encoding='utf8')
    et_e = parse(english)
    root_e = et_e.getroot()
    for country in root_e.iterfind('CountryRegion'):
        if country.get("Name") == "United States":
            for state in country.iterfind('State'):
                if state.get("Name") == "Delaware":
                    for city in state.iterfind('City'):
                        coordinate = get_coordinate(city.get("Name"), region='美国')
                        if coordinate:
                            sql = ("""INSERT INTO wechat_citylal(city,province,country,
                                                                            lng,lat)
                                                                            VALUES (%s,%s,'美国',%s,%s)""")

                            lal = (city.get("Name"), state.get("Name"), coordinate[0], coordinate[1])
                            try:
                                cursor.execute(sql, lal)
                                conn.commit()
                                print("城市：" + city.get("Name") + state.get("Name")+ str(coordinate))
                            except Exception as e:
                                print("error:"+str(e))
                                conn.rollback()


            break


# for e in root.findall('City'):
#     print(e)
if __name__ == '__main__':
    # get_chinese_city_lal()# 获取国内城市经纬度
    # get_foreign_city_lal()# 获取国外城市经纬度
    # get_chinese_city()# 获取中国未查到经纬度的城市
    # get_foreign_city()# 获取国外未查到经纬度的城市
    get_UK_city_lal()
    # revoke_before()
    conn.close()