SELECT 
    r.timestamp AT TIME ZONE 'UTC' as "Time", 
    r.city as "City", 
    w.temperature as "Temp", 
    w.description as "Weather"
FROM 
    requests_log r
JOIN 
    weather_data w ON r.id = w.request_id
ORDER BY 
    r.timestamp DESC;