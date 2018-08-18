# -*- coding: utf-8 -*-
import serial
import time
import requests


URL = "https://clova.ctws.jp/sensor" # get

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout = 0.5)
elementName = ["temperture", "relativeHumidity", "ambientLight", "uvIndex", "pressure", "soundNoise", "discomfortIndex", "heatStroke", "rfu", "batteryVoltage"]

try:
    while True:
        line = ser.read(500)
        element = line.split("\n")
        try:
            element.remove("\x00")

        except:
            pass

        valueDict = {}
        print element

        if len(element) < 5:
            continue
        for e in element:
            if(e=='/\x00'):
                continue
            if(e=='Backtrace'):
                continue
            e = e.replace(" ","")
            e = e.replace(":", " ")
            
            splitedList = e.split()
            print(splitedList)
            if(len(splitedList)<2):
                continue
            valueDict[splitedList[0]] = round(float(splitedList[1]), 2) 

        for i in elementName:
            try:
                print i + " : " + str(valueDict[i])

            except:
                continue
        print "Data GET"

        try:
            if(valueDict["temperture"] > 50): 
                continue
        except:
            continue

        payload = {'tm': valueDict["temperture"],
                   'rh': valueDict["relativeHumidity"],
                   'al': valueDict["ambientLight"],
                   'uv': valueDict["uvIndex"],
                   'pr': valueDict["pressure"],
                   'so': valueDict["soundNoise"]
                }

        r = requests.get(URL, params=payload)
        r.text
        time.sleep(1.0)

except KeyboardInterrupt:
    ser.close()


