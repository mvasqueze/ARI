# Trabajo #1 Fuentes de datos, Ingesta y Datalake en AWS


## DATASETS
- [Climate Change Indicators](https://www.kaggle.com/datasets/tarunrm09/climate-change-indicators?select=climate_change_indicators.csv)
- [Climate Change Video Set / NASA](https://www.kaggle.com/datasets/brsdincer/climate-change-video-set-nasa)
- [Global Average Absolute Sea Level Change, 1880-2014](https://datahub.io/core/sea-level-rise#data)
- [Green Domain](https://www.thegreenwebfoundation.org/tools/green-web-dataset/)

## Ingesta de datos y Almacenamiento

La ingesta de datos se realizo por medio de scripts de python


![alt text](Img/image-4.png)


con el archivo xml tuvimos que descomprimirlo y luego subirlo 

![alt text](Img/image-5.png)

con el dataset descargado de kaggle tuvimos que agregar un token para poder hacer la descarga 

![alt text](Img/image-6.png)
AWS

![alt text](Img/image-1.png)

## ETL

Creamos en Glue el crawler con las siguientes especificaciones

- especificaciones


Se hizo un proceso de limpieza editando algunos nombres de columnas en los diferentes datasets

![alt text](Img/image-2.png)

Resultado

![alt text](Img/image-3.png)


### ETLs AWS GLUE hacia zona RAW


ETL_SEA_LEVEL_CHANGE

