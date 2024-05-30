import clickhouse_connect
from datetime import datetime

def get_client():
    return clickhouse_connect.get_client(host='localhost')

def create_table():
    client = get_client()
    client.command('''
    CREATE TABLE IF NOT EXISTS traffic_data (
        timestamp DateTime,
        source_ip String,
        destination_ip String,
        bytes_transferred UInt64
    ) ENGINE = MergeTree()
    ORDER BY timestamp
    ''')

def insert_traffic_data(timestamp, source_ip, destination_ip, bytes_transferred):
    client = get_client()
    client.command('''
    INSERT INTO traffic_data (timestamp, source_ip, destination_ip, bytes_transferred) VALUES
    (%(timestamp)s, %(source_ip)s, %(destination_ip)s, %(bytes_transferred)s)
    ''', {'timestamp': timestamp, 'source_ip': source_ip, 'destination_ip': destination_ip, 'bytes_transferred': bytes_transferred})

def query_traffic_data():
    client = get_client()
    return client.query('SELECT * FROM traffic_data').result_rows

def delete_traffic_data(timestamp=None, source_ip=None, destination_ip=None):
    client = get_client()
    conditions = []
    params = {}

    if timestamp:
        conditions.append("timestamp = %(timestamp)s")
        params['timestamp'] = timestamp
    if source_ip:
        conditions.append("source_ip = %(source_ip)s")
        params['source_ip'] = source_ip
    if destination_ip:
        conditions.append("destination_ip = %(destination_ip)s")
        params['destination_ip'] = destination_ip

    if conditions:
        where_clause = " AND ".join(conditions)
        client.command(f'ALTER TABLE traffic_data DELETE WHERE {where_clause}', params)
    else:
        client.command('TRUNCATE TABLE traffic_data')
