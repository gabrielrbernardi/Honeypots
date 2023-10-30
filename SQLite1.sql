-- SQLite

SELECT eventid, src_ip, dst_ip, session, sensor, protocol, timestamp, avg(CAST(duration AS FLOAT)) AS duration_float
FROM (
    select eventid, src_ip, session, duration, sensor, dst_ip, protocol, timestamp
    FROM asia_east2
    UNION

    select eventid, src_ip, session, duration, sensor, dst_ip, protocol, timestamp
    FROM europe_west3
    UNION

    select eventid, src_ip, session, duration, sensor, dst_ip, protocol, timestamp
    FROM me_west1
    UNION

    select eventid, src_ip, session, duration, sensor, dst_ip, protocol, timestamp
    FROM southamerica_east1
    UNION

    select eventid, src_ip, session, duration, sensor, dst_ip, protocol, timestamp
    FROM us_west2
)
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
where eventid = 'cowrie.session.closed';
-- ORDER BY duration_float desc;


-- where session = 'b3e8d6706097';
-- where dst_ip LIKE '%2600:190%';
-- where eventid LIKE 'cowrie.login.success' and sensor LIKE '%-instance-02';
-- where protocol = 'ssh' or protocol = 'telnet' and eventid = 'cowrie.session.connect';
-- where protocol = 'ssh' or protocol = 'telnet';
-- where sensor LIKE '%instance-02' and eventid = 'cowrie.session.closed';
-- GROUP BY session;
-- where eventid = 'cowrie.session.closed'
-- where session = '38dd1b42686d';
-- ORDER BY duration_float ASC;

-- select * from df_0 where dst_ip LIKE '%2600:190%';

-- select * from df_0 where sensor='asia-east2-instance-02';