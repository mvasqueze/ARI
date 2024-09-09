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