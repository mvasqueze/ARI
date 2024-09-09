SELECT 
    objectid,
    country,
    iso2,
    iso3,
    indicator,
    unit,
    f1990,
    f2000,
    f2010,
    f2020
FROM 
    "dev"."public"."climate_indicators2"
WHERE 
    country IN ('United States', 'China', 'India');