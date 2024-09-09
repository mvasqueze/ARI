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