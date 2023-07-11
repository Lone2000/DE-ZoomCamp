#  Where all the scripts / Dependencies will show

from time import time

import os
import argparse
import pandas as pd

from sqlalchemy import create_engine



def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    # zip_format = params.zip_format
    url = params.url

    csv_name = "output.csv"
    zip_name = "output.csv.gz"


    # Check for url format Download
    if url.__contains__(".gz"):
        #Download csv and unzip
        os.system(f"wget {url} -O {zip_name}")
        # unzip and save
        os.system(f"gzip -d -c {zip_name} > {csv_name}")
    else:
        os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)


    while True:
        start_t = time()


        df = next(df_iter)

        # Formate TimeStamp Column to Date
        if url.__contains__(".gz"):
            df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
            df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
            

        # Create Table outline in db
        df.head(n=0).to_sql(name=table_name,con=engine, if_exists="replace")

        # Add Data into table
        df.to_sql(name=table_name, con=engine, if_exists='append')
        
        end_t = time()

        print(f"Interval of time {end_t - start_t}")





if __name__ == '__main__':



    # We create paremeters passing from the bash into our pipeline
    parser = argparse.ArgumentParser(
                        description='Creates pg table in database',
                        )

    # user password host port database_name tablename url_of_csv

    parser.add_argument('--user', help="user name for postgresql")
    parser.add_argument('--password', help="password for postgresql")
    parser.add_argument('--host', help="host for postgresql")
    parser.add_argument("--port", help="port for postgresql")
    parser.add_argument("--db", help="database name for postgresql")
    parser.add_argument("--table_name", help="table name for postgresql")
    parser.add_argument('--url', help="url of the csv file")
    # parser.add_argument("--zip_format", type=bool,help="Boolean value if it's a zip format")

    args = parser.parse_args()


    main(args)







