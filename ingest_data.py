#!/usr/bin/env python
# coding: utf-8
import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
# the backup files are gzipped, and it's important to keep the correct extension
# for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
    
    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')
    
# https://docs.python.org/es/3/library/argparse.html
    while True: 

        try:
            t_start = time()
            
            df = next(df_iter)

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break
        except Exception as e:
            print('An exception occurred:', e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgress')

    parser.add_argument('--user', type=str, default='postgres', help='Postgres user')
    parser.add_argument('--password', type=str, default='postgres', help='Postgres password')
    parser.add_argument('--host', type=str, default='localhost', help='Postgres host')
    parser.add_argument('--port', type=str, default='5432', help='Postgres port')
    parser.add_argument('--db', type=str, default='postgres', help='Postgres database')
    parser.add_argument('--table_name', type=str, default='taxi', help='Postgres table name')
    parser.add_argument('--url', type=str, default='https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2019-01.csv', help='URL to download CSV data')

    args = parser.parse_args()

    main(args)