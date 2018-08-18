# -*- coding: utf-8 -*-
# Sorry this file is python"2" ;-(
# If you get angry with this, I apologizede to you

import serial
import time
import requests


URL = "YOUR-URL" # get

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout = 0.5)
elementName = ["temperture", "relativeHumidity", "ambientLight", "uvIndex", "pressure", "soundNoise", "discomfortIndex", "heatStroke", "rfu", "batteryVoltage"]

try:
    while True:
        # シリアルモニタから500文字取得
        line = ser.read(500)

        element = line.split("\n")

        try:
            # NULL文字を消去
            element.remove("\x00")
        except:
            pass

        valueDict = {}
        print element

        if len(element) < 5:
            continue

        for e in element:
            if(e=='Backtrace'):
                continue

            # 文字列から連想配列の key と val を取得するため
            # フォーマットを整形する
            e = e.replace(" ","")
            e = e.replace(":", " ")
            
            splitedList = e.split()

            print(splitedList)
            
            if(len(splitedList)<2):
                continue
            
            # valはfloatのままなので、小数点以下が冗長になる
            # そのため、小数点第二位で丸めて保存する
            valueDict[splitedList[0]] = round(float(splitedList[1]), 2) 

        # 確認用
        for i in elementName:
            try:
                print i + " : " + str(valueDict[i])

            except:
                continue

        print "Data GET"

        # センサーの値がバグると何故か値が100℃を超える
        # 今の日本では多分50℃を超えることはないと思うので
        # 50℃を超えるときにはエラーということでデータを送らないことにする。
        try:
            if(valueDict["temperture"] > 50): 
                continue

        except:
            continue

        # URLの末尾のparamを設定
        payload = {'tm': valueDict["temperture"],
                   'rh': valueDict["relativeHumidity"],
                   'al': valueDict["ambientLight"],
                   'uv': valueDict["uvIndex"],
                   'pr': valueDict["pressure"],
                   'so': valueDict["soundNoise"]
                }

        # GETリクエストでデータを上げる
        r = requests.get(URL, params=payload)
        r.text
        time.sleep(1.0)

except KeyboardInterrupt:
    ser.close()


