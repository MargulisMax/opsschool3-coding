"""
Usage:
    python3 exercise2.py
"""

import json
from urllib.request import urlopen, quote

def GetLocationByIP():
    with urlopen('http://ip-api.com/json') as jsonrsp_ip:
        utfdata_ip = jsonrsp_ip.read(493).decode('utf-8')
        loadjson_ip = json.loads(utfdata_ip)
        return loadjson_ip['city'], loadjson_ip['countryCode']

def GetWeatherByLocation(mycity, mycountrycode):
    urlconc = 'http://api.openweathermap.org/data/2.5/weather?q=' + quote(mycity) + ',' + mycountrycode + '&units=metric&APPID=9c8b160816fc48b0288a6136e0989b2a'
    with urlopen(urlconc) as jsonrsp_wr:
        utfdata_wr = jsonrsp_wr.read(843).decode('utf-8')
        loadjson_wr = json.loads(utfdata_wr)
        return loadjson_wr

def main():
    mylocation = GetLocationByIP()
    myweather = GetWeatherByLocation(mylocation[0], mylocation[1])
    textfile = open('myweather.txt', 'w')
    textfile.write('Weather Description Is: ' + str(myweather['weather'][0]['description']) + '\n')
    textfile.write('Temperature Will Be: ' + str(myweather['main']['temp']) + ' degrees Celsius' + '\n')
    textfile.write('Humidity Will Be: ' + str(myweather['main']['humidity']) + '%' + '\n')
    textfile.write('Wind Speed Will Be: ' + str(myweather['wind']['speed']) + ' Meter/sec')
    textfile.close()
    cities = ['jerusalem', 'berlin', 'moscow', 'london', 'paris', 'vienna', 'amsterdam', 'brasilia', 'havana', 'athens']
    countries = ['IL-Israel', 'DE-Germany', 'RU-Russia', 'UK-England', 'FR-France', 'AT-Austria', 'NL-Netherland', 'BR-Brazil', 'CU-Cuba', 'GR-Greece']
    count = 0
    for city in cities:
            globalweather = GetWeatherByLocation(city, countries[count].split('-')[0])
            print('The weather in ' + city + ',' + countries[count].split('-')[1] + ' is ' + str(globalweather['main']['temp']) + ' degrees.')
            count += 1


if __name__ == '__main__':
    main()
