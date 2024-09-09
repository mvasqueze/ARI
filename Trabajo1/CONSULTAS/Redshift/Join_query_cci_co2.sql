SELECT 
    co2.country_or_area AS country,
    co2.item AS co2_emission_item,
    co2.year AS co2_year,
    co2.value AS co2_value,
    ci.indicator AS climate_indicator,
    ci.unit AS climate_unit,
    ci.source AS climate_source,
    CASE co2.year
        WHEN 2000 THEN ci.f2000
        WHEN 2001 THEN ci.f2001
        WHEN 2002 THEN ci.f2002
        WHEN 2003 THEN ci.f2003
        WHEN 2004 THEN ci.f2004
        WHEN 2005 THEN ci.f2005
        WHEN 2006 THEN ci.f2006
        WHEN 2007 THEN ci.f2007
        WHEN 2008 THEN ci.f2008
        WHEN 2009 THEN ci.f2009
        WHEN 2010 THEN ci.f2010
        WHEN 2011 THEN ci.f2011
        WHEN 2012 THEN ci.f2012
        WHEN 2013 THEN ci.f2013
        WHEN 2014 THEN ci.f2014
        WHEN 2015 THEN ci.f2015
        WHEN 2016 THEN ci.f2016
        WHEN 2017 THEN ci.f2017
        WHEN 2018 THEN ci.f2018
        WHEN 2019 THEN ci.f2019
        WHEN 2020 THEN ci.f2020
    END AS climate_value
FROM 
    co2_emissions4 co2
JOIN 
    climate_indicators2 ci
ON 
    co2.country_or_area = ci.country
WHERE 
    co2.year BETWEEN 2000 AND 2020
    AND co2.country_or_area IN ('Colombia', 'United States')
ORDER BY 
    co2.country_or_area, co2.year;