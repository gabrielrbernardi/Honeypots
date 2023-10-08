-- SQLite

select eventid, src_ip, session, duration, sensor, dst_ip, protocol, timestamp, (CAST(duration AS FLOAT)) AS duration_float
FROM us_west2
-- ;
-- where dst_ip LIKE '%::';
-- where sensor LIKE 'southamerica%';
-- where timestamp LIKE '2023-05-04%';
-- where eventid = 'cowrie.session.connect';
-- where protocol = 'ssh' and eventid = 'cowrie.session.connect';
-- where protocol = 'telnet' and eventid = 'cowrie.session.connect';
-- where eventid LIKE 'cowrie.login.success';
-- where eventid LIKE 'cowrie.login.success' and sensor LIKE '%-instance-01';
-- where eventid LIKE 'cowrie.login.success' and sensor LIKE '%-instance-02';
-- where eventid LIKE 'cowrie.login.failed';
-- where eventid LIKE 'cowrie.login.failed' and sensor LIKE '%-instance-01';
-- where eventid LIKE 'cowrie.login.failed' and sensor LIKE '%-instance-02';
where eventid = 'cowrie.session.closed'
-- ORDER BY duration_float desc;
ORDER BY duration_float asc;