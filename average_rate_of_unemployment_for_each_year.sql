SELECT
  extract(year from observation_date) AS year,
  AVG(unemployment_rate) avg_unemployment_rate
FROM FRED_SERIES.US_Civilian_Unemployment_Rate
WHERE extract(year from observation_date)  >= 1980 AND extract(year from observation_date) <= 2015
GROUP BY extract(year from observation_date)
ORDER BY extract(year from observation_date) DESC;