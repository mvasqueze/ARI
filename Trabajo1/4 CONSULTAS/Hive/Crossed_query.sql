SELECT
    t1.country AS country,
    t1.iso2 AS iso_code_2,
    t1.iso3 AS iso_code_3,
    t1.f2003 AS temperature_change_2003,
    t2.value AS co2_emissions_2003
FROM
    rawtotrusteddb. climate_change_indicators_trusted t1
JOIN
    rawtotrusteddb.co2_emissions_trusted t2
ON t1.country = t2.'country_or_area#0'
WHERE
    t2.year = 2003