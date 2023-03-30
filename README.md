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

* Adjust the permissions of the folder by running `sudo chmod a+rwx ny_taxi_postgres_data`

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
