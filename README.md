## Introduction

This repository contains a set of files and scripts to implement a data pipeline with Docker and PostgreSQL. The pipeline consists of data ingestion, running in Docker containers. The files include a Docker Compose configuration file for easy deployment and integration with other Docker tools, as well as scripts for data ingestion and database configuration. 


## Contents

Introduction to Docker: explaining why Docker is needed and creating a simple data pipeline in Docker.

Ingesting New York Taxi data into PostgreSQL: demonstrated how to ingest New York Taxi data into a PostgreSQL database running in a Docker container.

PostgreSQL and pgAdmin connection using Docker and Docker networking.

Putting the data ingestion script in a Docker container.

Running PostgreSQL and pgAdmin with Docker Compose.

There are also two optional resources covering networking issues and how to perform the above steps on Windows Subsystem Linux. In summary, these are useful for those who want to learn about Docker and how to use it to create containerized applications and services.

## Commands 

Downloading the data

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz 
```

> Note: now the CSV data is stored in the `csv_backup` folder, not `tripe+date` like previously

### Running Postgress with Docker

### Windows

Running Postgress on Windows

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v c:/Users/ivan/git/docker-postgresql-pipeline/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

If you have the following error:

```
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v e:/docker-postgresql-pipeline/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
docker: Error response from daemon: invalid mode: \Program Files\Git\var\lib\postgresql\data.
See 'docker run --help'.
```

Change the mounting path. Replace it with the following:

```
-v /e/docker-postgresql-pipeline/...:/var/lib/postgresql/data
```

#### Linux and MacOS :3

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

If you see that `ny_taxi_postgres_data` is empty after running the cointainer, try these:

* Deleting the folder and running Docker again (Docker will re-create the folder)

* Adjust the permissions of the folder by running `sudo chmod a+rwx ny_taxi_postgres_data` # ejecutar antes de correr el docker parece que funciona o despues de correrlo aparece :D probar primero el de despues

### CLI for Postgres

Installing `pgcli`

```bash
pip install pgcli
```

If you have problems installing `pgcli` with the command above, try this:

```bash
conda install -c conda-forge pgcli
pip install -U mycli
```

Using `pgcli` to connect to Postgres

```bash
pgcli -h localhost -p 5432 -U root -d ny_taxi
```


### NY Trips Dataset

Dataset:

* https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page
* https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

> According to the [TLC data website](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page),
> from 05/13/2022, the data will be in ```.parquet``` format instead of ```.csv```
> The website has provided a useful [link](https://www1.nyc.gov/assets/tlc/downloads/pdf/working_parquet_format.pdf) with sample steps to read ```.parquet``` file and convert it to Pandas data frame.

```
$ aws s3 ls s3://nyc-tlc
                           PRE csv_backup/
                           PRE misc/
                           PRE trip data/
```

### pgAdmin

Running pgAdmin

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```

It is also possible to use DBeaver it has the advantage of being able to connect to many different DBMS/DW from the same UI (Postgres, MySQL, BigQuery, Snowflake, etc). 

### Running Postgres and pgAdmin together

Create a network

```bash
docker network create pg-network
```

Run Postgres windows

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v c:/Users/ivan/git/docker_postgresql-pipeline/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
```

Linux and MacOS

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v /home/ivan/data/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
  ```

  Run pgAdmin

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
```

### Data ingestion

Running locally

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=${URL}
```

Build the image
It very important permission in docker xd

```bash
sudo docker build -t taxi_ingest:v001 .
```

On Linux you may have a problem building it:

```
error checking context: 'can't stat '/home/name/ny_taxi_postgres_data''.
```

You can solve it with `.dockerignore`:

* Create a folder `data`
* Move `ny_taxi_postgres_data` to `data` (you might need to use `sudo` for that)
* Map `-v $(pwd)/data/ny_taxi_postgres_data:/var/lib/postgresql/data`
* Create a file `.dockerignore` and add `data` there

Run the script with Docker

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```


### Docker-Compose 

Run it:

```bash
docker-compose up
```

Run in detached mode:

```bash
docker-compose up -d
```

Shutting it down:

```bash
docker-compose down
```

Note: Most of the errors are permissions errors eithers postgres o pgAdmin.
Example for change permissions:
```bash
sudo chmod -R 777 /home/...
```
To make pgAdmin configuration persistent, create a folder `data_pgadmin`. Change its permission via

```bash
sudo chown 5050:5050 data_pgadmin
```
and mount it to the `/var/lib/pgadmin` folder:



