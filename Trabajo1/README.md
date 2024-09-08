# Trabajo #1 Fuentes de datos, Ingesta y Datalake en AWS, Procesamiento 

## 1. Fuentes de Datos y Preparación

### Identificación de Fuentes

Se comenzaron a buscar datasets relacionados con el cambio climático y el calentamiento global en diferentes niveles (local, nacional e internacional). Las fuentes seleccionadas fueron:

- **Climate Change Indicators:** [Kaggle Dataset](https://www.kaggle.com/datasets/tarunrm09/climate-change-indicators?select=climate_change_indicators.csv)
- **Climate Change Video Set / NASA:** [Kaggle Dataset](https://www.kaggle.com/datasets/brsdincer/climate-change-video-set-nasa)
- **Global Average Absolute Sea Level Change, 1880-2014:** [DataHub Dataset](https://datahub.io/core/sea-level-rise#data)
- **CO2 Emissions:** [World Bank Dataset](https://data.worldbank.org/indicator/EN.ATM.CO2E.PC)

### Ingesta de Datos

La ingesta de los datos hacia la zona RAW del Data Lake fue automatizada utilizando scripts de Python que descargaron los datasets desde las diferentes fuentes. Estos datos fueron posteriormente almacenados en la ruta S3 correspondiente a la zona RAW.

#### Fuentes de Datos y Ubicación en S3

- **Climate Change Indicators:**
  - Ubicación en S3: `s3://climate-change-datalake/Raw/Climate-Change-Indicators/`
  
- **Climate Change Videos:**
  - Ubicación en S3: `s3://climate-change-datalake/Raw/Climate-change-videos/`

- **CO2 Emissions:**
  - Ubicación en S3: `s3://climate-change-datalake/Raw/CO2-Emissions/`

- **Sea Level Change:**
  - Ubicación en S3: `s3://climate-change-datalake/Raw/Sea-level-change/`

### Retos

- **Dataset CO2 Emissions:** 
  - Los datos estaban en un archivo comprimido en formato ZIP que contenía un archivo XML. Se descomprimió y luego se convirtió en formato CSV para su procesamiento.
  ![Retos](Img/image-5.png)

- **Dataset Climate Change Indicators y Climate Change Videos:**
  - Estos datasets fueron descargados desde Kaggle, lo que requirió un token de autenticación debido a las restricciones de acceso a los datos.
  ![Autenticación](Img/image-6.png)

## 2. Diseño del Data Lake

### Zonificación del Data Lake

Se definieron las siguientes zonas:

- **Raw:** Se almacenaron los datos originales tal como se descargaron.
- **Trusted:** Los datos fueron procesados y transformados para análisis.

### Almacenamiento

Los datos fueron organizados y almacenados en S3 siguiendo una estructura jerárquica:

```s3://climate-change-datalake/Raw/```

![Estructura de Almacenamiento](Img/image-1.png)

## 3. ETL con AWS Glue

Se usaron Glue Crawlers para catalogar los datos en la zona RAW, creando metadatos en el Data Catalog que permitieron el acceso a los datos desde Athena y Redshift.

### Crawler

Se creó un Crawler con las siguientes especificaciones:
![Crawler](Img/image-9.png)

## 4. ETL AWS Glue hacia Zona Trusted

Después de tener los datos correctamente en la zona RAW, se construyeron y ejecutaron los scripts de ETL en AWS Glue.

### Especificaciones del ETL Job

- **Nombre del ETL Job:** rawtotrusted
- **IAM Role:** LabRole
- **Tipo:** Spark
- **Versión de Glue:** Glue 4.0 (Soporta Spark 3.3, Scala 2, Python 3)
- **Lenguaje:** Python 3
- **Tipo de Trabajador:** G.1X

Los scripts ejecutados se pueden encontrar en el repositorio [GitHub](https://github.com/mvasqueze/ARI/tree/main/Trabajo1/AWS%20ETL%20GLUE%20TRUSTED), y su estatus para cada dataset terminó en "Succeeded". Luego de esto, se crearon las tablas correspondientes en nuestra base de datos.
![ETL Job](Img/image-8.png)

> [!IMPORTANT]
> En el contexto de este proyecto, se tomó la decisión inicial de trabajar con datos no estructurados, como archivos de video, para capturar diversas fuentes de información sobre el cambio climático. Sin embargo, después de evaluar las complejidades inherentes al manejo de este tipo de datos, se ha decidido proceder con datos estructurados en formato CSV por las diferentes razones.

## 5. Consultas y Modelado de Datos

### Consultas en Athena

Una vez que los datos estuvieron catalogados, se usó Athena para realizar consultas SQL sobre los datos en S3. Aquí algunos ejemplos:

- **Consulta 1:** Recupera las emisiones de CO2 desde el año 2000, ordenadas de mayor a menor, y muestra los 10 registros más altos.
  ```sql
  SELECT 
      "country or area", 
      item, 
      year, 
      value
  FROM "co2_emissions"
  WHERE year >= 2000
  ORDER BY value DESC
  LIMIT 10;

![alt text](Img/image-11.png)

- **Consulta 2:** Extrae datos sobre indicadores de temperatura específicos para Colombia para los años 1967, 1968, 1969, 1970, 2020, 2021 y 2022.

    ```sql
    SELECT 
        Country,
        ISO2,
        ISO3,
        Source,
        F1967,
        F1968,
        F1969,
        F1970,
        F2020,
        F2021,
        F2022
    FROM 
        "climate_change_indicators_83cc632aa7b85365d4cd8a18b81dc435"
    WHERE 
        Country = 'Colombia'
        AND Indicator LIKE '%Temperature%'  
    ORDER BY 
        Country ASC
    LIMIT 10;

![alt text](Img/image-10.png)

- **Consulta 3:** Consulta 3: Extrae datos sobre el nivel del mar ajustado por CSIRO y NOAA para el rango de años de 2000 a 2010, ordenados por año.


    ```sql
        SELECT 
            year AS Year,
            CAST(NULLIF("CSIRO - Adjusted sea level (inches)", '') AS DOUBLE) AS CSIRO_Adjusted_Sea_Level,
            CAST(NULLIF("CSIRO - Lower error bound (inches)", '') AS DOUBLE) AS CSIRO_Lower_Error_Bound,
            CAST(NULLIF("CSIRO - Upper error bound (inches)", '') AS DOUBLE) AS CSIRO_Upper_Error_Bound,
            CAST(NULLIF("NOAA - Adjusted sea level (inches)", '') AS DOUBLE) AS NOAA_Adjusted_Sea_Level
        FROM 
            "sea_level_change"
        WHERE 
            year BETWEEN '2000' AND '2010' 
        ORDER BY 
            year ASC
        LIMIT 10;

![alt text](Img/image-12.png)



