#!/usr/bin/env python
# coding: utf-8

import os
import json
from time import time

import pandas as pd
from sqlalchemy import create_engine


def main():
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db = os.getenv('DB_NAME')
    data_sources = []
    with open('sources.json', 'r') as f:
        data_sources = json.load(f)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    for data_source in data_sources:
        url = data_source['url']
        table_name = data_source['table_name']

        if url.endswith('.csv.gz'):
            csv_name = 'output.csv.gz'
        else:
            csv_name = 'output.csv'

        os.system(f"wget {url} -O {csv_name}")

        df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

        df = next(df_iter)

        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

        df.to_sql(name=table_name, con=engine, if_exists='append')

        while True:
            try:
                t_start = time()

                df = next(df_iter)

                df.to_sql(name=table_name, con=engine, if_exists='append')

                t_end = time()

                print('inserted another chunk, took %.3f second' % (t_end - t_start))

            except StopIteration:
                print("Finished ingesting data into the postgres database")
                break

if __name__ == '__main__':
    main()
