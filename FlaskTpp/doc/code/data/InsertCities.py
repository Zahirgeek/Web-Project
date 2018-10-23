import json

import pymysql

# 读取json文件
def load_data():
    with open("./json/cities.json", "r") as cities_json_file:
        cities_json_str = cities_json_file.read()
        cities_json = json.loads(cities_json_str)

    return cities_json


def insert_cities(cities_json):
    # 获取地址
    cities = cities_json.get("returnValue")

    keys = cities.keys()
    # 连接mysql数据库
    db = pymysql.Connect(host="localhost", port=3306, user="root", password="sunck1999", database="GP1FlaskTpp", charset="utf8")

    # 使用cursor()方法获取操作游标
    cusor = db.cursor()

    # 遍历每一个字母
    for key in keys:

        # 使用execute方法执行SQL语句
        cusor.execute("INSERT INTO letter(letter) VALUES ('%s');" % key)

        # 提交到数据库执行
        db.commit()

        cusor.execute("SELECT letter.id FROM letter WHERE letter='%s'" % key)
        # 使用 fetchone() 方法获取一条数据
        letter_id = cusor.fetchone()[0]

        cities_letter = cities.get(key)

        for city in cities_letter:

            c_id = city.get("id")
            c_parent_id = city.get("parentId")
            c_region_name = city.get("regionName")
            c_city_code = city.get("cityCode")
            c_pinyin = city.get("pinYin")

            cusor.execute("INSERT INTO city(letter_id, c_id, c_parent_id, c_region_name, c_city_code, c_pinyin) VALUES (%d, %d, %d, '%s', %d, '%s');" % (letter_id, c_id, c_parent_id, c_region_name, c_city_code, c_pinyin))
            db.commit()


if __name__ == '__main__':
    cities_json = load_data()
    insert_cities(cities_json)
