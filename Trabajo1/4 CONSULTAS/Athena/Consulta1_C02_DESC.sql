SELECT 
    "country or area", 
    item, 
    year, 
    value
FROM "co2_emissions"
WHERE year >= 2000
ORDER BY value DESC
LIMIT 10;