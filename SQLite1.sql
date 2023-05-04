-- SQLite

SELECT eventid, src_ip, session, sensor, (CAST(duration AS FLOAT)) AS duration_float
FROM (
    select eventid, src_ip, session, duration, sensor, dst_ip, protocol
    FROM df_0
    UNION

    select eventid, src_ip, session, duration, sensor, dst_ip, protocol
    FROM df_1
    UNION

    select eventid, src_ip, session, duration, sensor, dst_ip, protocol
    FROM df_2
    UNION

    select eventid, src_ip, session, duration, sensor, dst_ip, protocol
    FROM df_3
    UNION

    select eventid, src_ip, session, duration, sensor, dst_ip, protocol
    FROM df_4
);
-- where dst_ip LIKE '%2600:190%';
-- where protocol = 'ssh' and eventid = 'cowrie.session.connect';
-- where sensor LIKE '%instance-01' and eventid = 'cowrie.session.closed'
-- GROUP BY session;
-- ORDER BY duration_float DESC;

-- select * from df_0 where dst_ip LIKE '%2600:190%';

-- select * from df_0 where sensor='asia-east2-instance-02';