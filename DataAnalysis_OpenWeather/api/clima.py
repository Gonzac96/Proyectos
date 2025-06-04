from dotenv import load_dotenv
import requests 
import os 
from datetime import datetime
import time 
import math 
import pandas as pd 
from pandas import json_normalize
from openpyxl.workbook import Workbook
from database.database import Conexion 
import datetime




load_dotenv()

class ExtractAPIClima(): 
   

    Base_URL='https://api.openweathermap.org/data/2.5/onecall/timemachine?'
    APIKEY=os.getenv('APIKEY')
    key='&appid='+APIKEY
    clima=[]
    def extraerDatos(self, coordList:list, cityList:list):
        fecha=datetime.datetime.now() 
        for i in range(0,len(cityList)): 
            fechaActual=fecha
            for j in range(5): 
                
                fechaActual=fechaActual-datetime.timedelta(days=1)
                dt='&dt='+str(int(datetime.datetime.timestamp(fechaActual)))
                url=self.Base_URL+coordList[i]+dt+'&units=metric'+self.key
                response=requests.get(url) 
                if response.status_code==200: 
                   
                    self.clima.append(response.json())
                
        
        return self.clima


class TransformAPIClima(): 
       
       
       data_original=pd.DataFrame()

       def __init__(self, lista:list): 
        self.data_original=pd.json_normalize(lista)
        
    
       def extraerHourly(self)->pd.DataFrame:
           hourly=pd.json_normalize(self.data_original['hourly'])
           hourly=hourly.iloc[:,0]
           return pd.json_normalize(hourly)

        
       def extraerWeather(self, data:pd.DataFrame)->pd.DataFrame:
           weather=pd.json_normalize(data['weather'])
           weather=weather[0]
           return pd.json_normalize(weather)
       
       def dtUnixADateTime(self, data:pd.DataFrame)->pd.DataFrame:
           lista=[] 
           for i in range(0, len(data)): 
               lista.append(str(datetime.datetime.fromtimestamp(data.iloc[i]['current.dt'])))
            
           data={ 
                "current.dt2":lista
            }
           return pd.DataFrame(data)
         
       
       def eliminarColumnas(self, data:pd.DataFrame)->pd.DataFrame: 
           data.drop(['weather','hourly','current.weather', 'current.dt','current.sunrise', 'current.sunset'], axis=1, inplace=True)
           return data 
       
     
       
       def extraerSunrise(self, data:pd.DataFrame)->pd.DataFrame: 
           lista=[] 
           for i in range(len(data)): 
               lista.append(str(datetime.datetime.fromtimestamp(data.iloc[i]['current.sunrise'])))
           data= { 
              "current.sunrise":lista 
          }
           df=pd.DataFrame(data) 
           return df 
       
       def extraerSunset(self, data:pd.DataFrame)->pd.DataFrame: 
           lista=[]
           for i in range(len(data)): 
               lista.append(str(datetime.datetime.fromtimestamp(data.iloc[i]['current.sunset']))) 
            
           data={ 
                "current.sunset":lista
            }
           return pd.DataFrame(data)
       
       def dataOriginal(self)->pd.DataFrame: 
           return self.data_original
       
       def currentWeather(self, data:pd.DataFrame)->pd.DataFrame: 
           currentWeather= pd.json_normalize(data['current.weather'])
           currentWeather=currentWeather[0]
           currentWeather=pd.json_normalize(currentWeather)
           currentWeather.rename(columns={"id": "current.weather.id", "main":"current.weather.main", 
                                          "description":"current.weather.description", "icon":"current.weather.icon"
                                          }, inplace=True)
           return currentWeather
       
       def modificarTimezone(self, data:pd.DataFrame, cityList:list)->pd.DataFrame: 
           data.replace(to_replace=['Europe/London', 'America/New_York','America/Argentina/Cordoba', 
                                           'Asia/Taipei', 'America/Argentina/Buenos_Aires', 
                                           'America/Mexico_City', 'America/Los_Angeles', 
                                           'Asia/Tbilisi','America/Bogota','Asia/Tokyo' ], value=cityList, inplace=True)
           ciudad=data.rename(columns={"timezone":"ciudad"})
           return ciudad
        
       def modificarColumnas(self, data:pd.DataFrame)->pd.DataFrame: 
           new_data=data.rename(columns={"current.temp":"Temperatura Actual", "lat":"Latitud", "lon":"Longitud", "current.feels_like":"Sensacion termica actual", 
                                "current.pressure":"Presion actual", "current.humedity":"Humedad actual", "current.dew_point":"Punto de Rocio actual", 
                                "current.visibility":"Visibilidad Actual", "current.wind_speed":"Velocidad del viento actual", 
                                "current.wind_deg":"Grados del Viento actual", "current.wind_gust":"Rafaga del viento"})
           return new_data


class LoadAPIClima(): 

    

    def exportarACSV(self, data:pd.DataFrame, file:str): 
        print(file)
        data.to_csv(file, index=False)
        
           
    def exportarAExcel(self, data:pd.DataFrame, file:str): 
        data.to_excel(file, index=False)  
       

    def exportarAJSON(self, data:pd.DataFrame, file:str):
        data.to_json(file,orient='index') 
    
    def exportarASQL(self, data:pd.DataFrame, engine:Conexion): 
        data.to_sql('clima', engine, if_exists='replace', index=False)


                

      