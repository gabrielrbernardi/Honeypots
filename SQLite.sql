-- SQLite
-- select * from df_0;

-- Get Connection Quantity
-- select eventid, src_ip, protocol, count(protocol) from df_0 where protocol != 'nan' group by src_ip order by count(protocol) DESC;

-- Get Session Duration
SELECT eventid, src_ip, session, (CAST(duration AS FLOAT)) AS duration_float
FROM (
    SELECT eventid, src_ip, session, duration FROM df_0
    WHERE duration != 'nan' AND eventid != 'cowrie.log.closed' 
    UNION 
    SELECT eventid, src_ip, session, duration FROM df_1
    WHERE duration != 'nan' AND eventid != 'cowrie.log.closed'
)
ORDER BY duration_float DESC;