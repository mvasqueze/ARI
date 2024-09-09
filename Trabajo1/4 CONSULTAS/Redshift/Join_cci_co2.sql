SELECT 
    co2.country_or_area AS country,
    co2.item AS co2_emission_item,
    co2.year AS co2_year,
    co2.value AS co2_value,
    ci.indicator AS climate_indicator,
    ci.unit AS climate_unit,
    ci.source AS climate_source,
    ci.f2003 AS climate_value_2003
FROM 
    co2_emissions4 co2
JOIN 
    climate_indicators2 ci
ON 
    co2.country_or_area = ci.country;