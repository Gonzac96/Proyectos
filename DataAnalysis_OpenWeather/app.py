from database.database import Conexion 
from sqlalchemy.ext.declarative import declarative_base 
import pandas as pd 
from api.clima import ExtractAPIClima
from api.clima import TransformAPIClima
from api.clima import LoadAPIClima
import requests
import os 
import datetime 

pd.options.display.max_columns=30



Base=declarative_base()
conexion=Conexion()
conexion.get_conexion(conexion.get_engine(), Base)
engine=conexion.get_engine()
conexion.get_Session()
session=conexion.get_Session() 







if __name__=='__main__': 
    cityList = ["Londres", "New York", "Cordoba", "Taipei", "Buenos Aires", "Mexico DF", "Dublin", "Tiflis" ,"Bogota", "Tokio"]
    coordList=["lat=51.5085&lon=-0.1257","lat=40.7143&lon=-74.006", "lat=-31.4135&lon=-64.1811", "lat=25.0478&lon=121.5319", "lat=-34.6132&lon=-58.3772", "lat=19.4285&lon=-99.1277", "lat=37.7021&lon=-121.9358", "lat=41.6941&lon=44.8337","lat=4.6097&lon=-74.0817","lat=35.6895&lon=139.6917" ]
    extractAPI=ExtractAPIClima() 
    lista=extractAPI.extraerDatos(coordList=coordList, cityList=cityList)
    
    transformApi=TransformAPIClima(lista)
    dataHourly=transformApi.extraerHourly()
    dataWeather=transformApi.extraerWeather(dataHourly)
    data=pd.concat([dataHourly, dataWeather], axis=1)
    dataOriginal=transformApi.dataOriginal()
    data=pd.concat([dataOriginal, data], axis=1) 
    dataCurrentWeather=transformApi.currentWeather(data)
    data=pd.concat([data, dataCurrentWeather], axis=1)
    dataDT=transformApi.dtUnixADateTime(data)
    data=pd.concat([data, dataDT], axis=1)
    dataSunrise=transformApi.extraerSunrise(data)
    
    data=pd.concat([data, dataSunrise], axis=1)
    dataSunset=transformApi.extraerSunset(data)
    data=transformApi.eliminarColumnas(data)
    data=pd.concat([data, dataSunset], axis=1)

    data.rename(columns={ "current.dt2":"current.dt"}, inplace=True)

    data=transformApi.modificarTimezone(data, cityList)
    data=transformApi.modificarColumnas(data)
    print(data)
    ##Retorna la media de la temperatura agrupado por ciudad
    df_ciudad=data.groupby(by='ciudad', as_index=False)['Temperatura Actual'].mean()
    df_ciudad.rename(columns={"Temperatura Actual": "Temperatura media"}, inplace=True)
    path=os.path.dirname(os.path.abspath(__file__)) 
    
    fechaActual=datetime.datetime.now() 
    fecha=str(fechaActual.day)+ "-"+str(fechaActual.month) + "-"+str(fechaActual.year)
    file = path +"\DataAnalysis"+"_"+fecha+"_clima.csv"
    
    
    
    loadApi=LoadAPIClima() 
    loadApi.exportarACSV(data, file) 
    
    file=path + "\DataAnalysis"+"_"+fecha+"_clima.xlsx"
    loadApi.exportarAExcel(data, file)
    file=path+ "\DataAnalysis"+"_"+fecha+"_clima.json"
    loadApi.exportarAJSON(data, file)
    loadApi.exportarASQL(data=data, engine=engine)
    
    
    
    

   

    
    
    

   
    
    
    
   
        


    



