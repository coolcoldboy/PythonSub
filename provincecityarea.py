# coding=utf-8
import json
import os

__author__ = 'zhwang.kevin'


print(os.getcwd())
with open("file\district.json",'r', encoding='UTF-8') as load_f:
    load_dict = json.load(load_f)
    # print(load_dict)
    provinces = {}
    provincecitys = {}
    cityareas = {}
    for key, value in load_dict.items():
        keyInt = int(key)
        if keyInt%10000 == 0:
            provinces.update({key:value})

        elif keyInt%10000 !=0 and  keyInt%100 == 0:
            proKey = round(keyInt//10000*10000)
            proKey = str(proKey)
            if provincecitys.get(proKey) == None:
                provincecitys[proKey] = {key:value}
            else:
                provincecitys[proKey].update({key:value})
        else:
            cityKey = round(keyInt//100*100)
            cityKey = str(cityKey)
            proKey = round(keyInt//10000*10000)
            proKey = str(proKey)
            if load_dict.get(cityKey) == None:
                if provincecitys.get(proKey) == None:
                    provincecitys[proKey] = {key:value}
                else:
                    provincecitys[proKey].update({key:value})
            else:
                if cityareas.get(cityKey) == None:
                    cityareas[cityKey] = {key:value}
                else:
                    cityareas[cityKey].update({key:value})

    print(provinces)
    print(provincecitys)
    print(cityareas)
