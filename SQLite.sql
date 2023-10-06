-- SQLite
-- select * from df_0;

-- Get Connection Quantity
-- select eventid, src_ip, protocol, count(protocol) from df_0 where protocol != 'nan' group by src_ip order by count(protocol) DESC;

-- Get Session Duration
-- SELECT eventid, src_ip, session, (CAST(duration AS FLOAT)) AS duration_float
-- FROM (
--     SELECT eventid, src_ip, session, duration FROM asia_east2
--     WHERE duration != 'nan' AND eventid != 'cowrie.log.closed' 
--     UNION 
--     SELECT eventid, src_ip, session, duration FROM europe_west3
--     WHERE duration != 'nan' AND eventid != 'cowrie.log.closed'
--     UNION 
--     SELECT eventid, src_ip, session, duration FROM me_west1
--     WHERE duration != 'nan' AND eventid != 'cowrie.log.closed'
--     UNION 
--     SELECT eventid, src_ip, session, duration FROM southamerica_east1
--     WHERE duration != 'nan' AND eventid != 'cowrie.log.closed'
--     UNION 
--     SELECT eventid, src_ip, session, duration FROM us_west2
--     WHERE duration != 'nan' AND eventid != 'cowrie.log.closed'
-- )
-- ORDER BY duration_float DESC;

select * from asia_east2 where eventid = 'cowrie.session.connect' group by dst_ip;

-- select * from asia_east2 where dst_ip LIKE '%2600:%';
-- select * from asia_east2 where dst_ip = '2600:1900:41a0:dd2::';
-- select * from asia_east2 where timestamp LIKE '2023-05-06';