from datetime import datetime
import requests
import xmltodict
import time
import pygame

weather_code = 0
imgSnow = pygame.image.load('img/snow_.png')
#imgSnow2 = pygame.image.load('img/snow2.png').convert_alpha()
imgRain = pygame.image.load('img/rain_.png')
#imgRain2 = pygame.image.load('img/rain2.png').convert_alpha()

# baseDate
def get_current_date_string():
    current_date = datetime.now().date()
    return current_date.strftime("%Y%m%d")

# baseTime
def get_current_hour_string():
    now = datetime.now()
    if now.minute<45: # base_time와 base_date 구하는 함수
        if now.hour==0:
            base_time = "2330"
        else:
            pre_hour = now.hour-1
            if pre_hour<10:
                base_time = "0" + str(pre_hour) + "30"
            else:
                base_time = str(pre_hour) + "30"
    else:
        if now.hour < 10:
            base_time = "0" + str(now.hour) + "30"
        else:
            base_time = str(now.hour) + "30"

    return base_time

keys = 'yZS7b9ev4+on01NqwTnd1op1VGrA3mal//baVXD5UW3FYM7Fw7NUPeqZy7HwajA3B99UKBB1YEEyl+ZQJkiLuQ=='
url = 'https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
params ={'serviceKey' : keys, 
         'pageNo' : '1', 
         'numOfRows' : '1000', 
         'dataType' : 'XML', 
         'base_date' : get_current_date_string(), 
         'base_time' : get_current_hour_string(), 
         'nx' : '62', 
         'ny' : '89' }

#날씨 필터
def weather_filter(bg, num):
    global alpha, weather_code
    
    #비
    if weather_code == 1:
        if num == 0:
            bg.blit(imgRain2, [0 - tmr, 0])
            imgRain2.set_alpha(alpha)
        elif num == 1:
            bg.blit(imgRain, [0, 0])
            #draw_para(bg, fnt)
        elif num == 2:
            for a in range(0, 256):
                alpha -= 1
                imgRain2.set_alpha(alpha)
    #구름            
    if weather_code == 2:
        if num == 0:
            imgCloud.set_alpha(alpha)
        elif num == 1:
            draw_para(bg, fnt)
        elif num == 2:
            for a in range(0, 256):
                alpha -= 1
                imgCloud.set_alpha(alpha)
    # 눈
    if weather_code == 3:
        if num == 0:
            bg.blit(imgSnow2, [0 - tmr, 0])
            imgSnow2.set_alpha(alpha)
        elif num == 1:
            bg.blit(imgSnow, [0, 0])
            #draw_para(bg, fnt)
        elif num == 2:
            for a in range(0, 256):
                alpha -= 1
                imgSnow2.set_alpha(alpha)

def forecast():
    # 값 요청 (웹 브라우저 서버에서 요청 - url주소와 파라미터)
    res = requests.get(url, params)

    #XML -> 딕셔너리
    xml_data = res.text
    dict_data = xmltodict.parse(xml_data)

    #값 가져오기
    weather_data = dict()
    
    for item in dict_data['response']['body']['items']['item']:
        # 기온
        if item['category'] == 'T1H':
            weather_data['tmp'] = item['fcstValue']
        # 습도
        if item['category'] == 'REH':
            weather_data['hum'] = item['fcstValue']
        # 하늘상태: 맑음(1) 구름많은(3) 흐림(4)
        if item['category'] == 'SKY':
            weather_data['sky'] = item['fcstValue']
        # 강수형태: 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
        if item['category'] == 'PTY':
            weather_data['sky2'] = item['fcstValue']

    return weather_data

def proc_weather():
    global weather_code
    
    dict_sky = forecast()

    str_sky = ""
    
    if dict_sky['sky'] != None and dict_sky['sky2'] != None:
        str_sky = str_sky + "Weather : "
        if dict_sky['sky2'] == '0':
            if dict_sky['sky'] == '1':
                str_sky = str_sky + "Fine."
            elif dict_sky['sky'] == '3':
                str_sky = str_sky + "Mostly Cloudy."
            elif dict_sky['sky'] == '4':
                str_sky = str_sky + "Cloudy."
        elif dict_sky['sky2'] == '1':
            str_sky = str_sky + "Rain."
            weather_code = 1
        elif dict_sky['sky2'] == '2':
            str_sky = str_sky + "Rain/Snow."
        elif dict_sky['sky2'] == '3':
            str_sky = str_sky + "Snow."
            weather_code = 3
        elif dict_sky['sky2'] == '5':
            str_sky = str_sky + "RainDrop."
        elif dict_sky['sky2'] == '6':
            str_sky = str_sky + "RainDrop/SnowDrifting."
        elif dict_sky['sky2'] == '7':
            str_sky = str_sky + "SnowDrifting."
        str_sky = str_sky
    if dict_sky['tmp'] != None:
        str_sky = str_sky + "Temperature : " + dict_sky['tmp'] + 'ºC.'
    if dict_sky['hum'] != None:
        str_sky = str_sky + "Humidity : " + dict_sky['hum'] + '%.'

    return str_sky
    