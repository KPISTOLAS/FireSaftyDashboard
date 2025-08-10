
BEGIN
    RETURN QUERY
    SELECT n.node_id, n.title, n.location
    FROM Nodes n
    JOIN Node_Regions nr ON n.node_id = nr.node_id
    WHERE nr.region_id = region_id_param;
END;

BEGIN
    RETURN QUERY
    SELECT
        n.node_id,
        n.title,
        n.location,
        n.is_parent,
        n.lat,
        n.lng,
        sr.danger_level,
        sr.timestamp as last_updated
    FROM nodes n
    LEFT JOIN LATERAL (
        SELECT danger_level, timestamp
        FROM sensor_readings
        WHERE node_id = n.node_id
        ORDER BY timestamp DESC
        LIMIT 1
    ) sr ON true;
END;


BEGIN
    RETURN QUERY
    SELECT
        n.node_id,
        n.title,
        n.location,
        n.is_parent,
        n.lat,
        n.lng,
        sr.danger_level,
        sr.timestamp as last_updated
    FROM nodes n
    JOIN node_regions nr ON n.node_id = nr.node_id
    LEFT JOIN LATERAL (
        SELECT danger_level, timestamp
        FROM sensor_readings
        WHERE node_id = n.node_id
        ORDER BY timestamp DESC
        LIMIT 1
    ) sr ON true
    WHERE nr.region_id = region_id_param;
END;
