from django.shortcuts import render 
from django.http import HttpResponse
import requests
from django.urls import path
from datetime import datetime
import json
def obtener_lat_lon(request):
    buscador = request.GET.get('ciudad','')
    res = {
        "resultados": []
    }
    repetido = {}
    datasoft = requests.get('https://public.opendatasoft.com/api/records/1.0/search/?dataset=worldwide-pollution&rows=10000&q=' +buscador)
    # print(res.content)
    res_json = datasoft.json()
    for calculo in res_json['records']:
        lat = str(calculo['geometry']['coordinates'][0])
        lng = str(calculo['geometry']['coordinates'][1])
        if (lat + lng) not in repetido:
            repetido[lat + lng] = sacar_datos_opendata(calculo)
        else:
            temp = sacar_datos_opendata(calculo)
            if volver_datetime_fecha_opendata(temp['fecha']) > volver_datetime_fecha_opendata(repetido[lat + lng]['fecha']):
                repetido[lat + lng] = temp
    
    for localizacion in repetido.items():
        for datos in localizacion:
            if type(datos) != str:
                res['resultados'].append(datos)
    print(res_json['nhits'])
    return HttpResponse(json.dumps(res))


def sacar_datos_opendata(req):
    res = {}
    
    fields = req['fields']
    res['coordenadas'] = req['geometry']['coordinates']
    #conseguimos la fecha
    res['fecha'] = fields['data_dates'][2:12] + " " + fields['data_dates'][13:21]
    #conseguimos el NO2
    res['NO2'] = fields['value_no2']
    #conseguimos el O3
    res['O3'] = fields['value_o3']
    #conseguimos el CO
    res['CO'] = fields['value_co']
    
    #conseguimos el PM2.5
    key = fields['data_pollutants_pm25_aqi_epa'].find('values')
    res['PM2.5'] = fields['data_pollutants_pm25_aqi_epa'][key+10]
    #conseguimos el PM5
    res['PM5'] = fields['value_pm5']
    #conseguimos el PM10
    key_inicial = fields['data_pollutants'].find('PM10')
    key = fields['data_pollutants'][key_inicial:].find('values')
    res['PM10'] = fields['data_pollutants'][key+10]
    return res

def volver_datetime_fecha_opendata(fecha):
    return datetime(
        int(fecha[0:4]),
        int(fecha[5:7]),
        int(fecha[8:10]),
        int(fecha[11:13]),
        int(fecha[14:16]),
        int(fecha[17:19])
        )