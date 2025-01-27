# Week 01 - Docker and Terraform
---
Below are the SQL Queries and other commands used in week 1 homework.

#### Question 1. Run docker with the python:3.12.8 image in an interactive mode, use the entrypoint bash. What's the version of pip in the image?
Answer: It gives the pip version `24.3.1`
```
user@system % docker run -it python:3.12.8 bash
root@5e0acf32e65b:/# pip -V
pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
```

#### Question 2. Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?
```
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```
Answer: pgadmin can connect to postgres at `postgres:5432`. The postgres can be reached at service name `db` but since the container_name was mentioned, it replaces the hostname.

#### Question 3. During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:
**- Up to 1 mile**
**- In between 1 (exclusive) and 3 miles (inclusive)**
**- In between 3 (exclusive) and 7 miles (inclusive)**
**- In between 7 (exclusive) and 10 miles (inclusive)**
**- Over 10 miles**
Answer: The result is `104,802; 198,924; 109,603; 27,678; 35,189` using dropoff time in filter. Using pickup time did not produce any result from given options.
```
# SQL Query
SELECT
	SUM(CASE WHEN trips.trip_distance <= 1 THEN 1 ELSE 0 END) AS "Up to 1 mile",
	SUM(CASE WHEN trips.trip_distance > 1 AND trips.trip_distance <=3 THEN 1 ELSE 0 END) AS "In between 1 (exclusive) and 3 miles (inclusive)",
	SUM(CASE WHEN trips.trip_distance > 3 AND trips.trip_distance <=7 THEN 1 ELSE 0 END) AS "In between 3 (exclusive) and 7 miles (inclusive)",
	SUM(CASE WHEN trips.trip_distance > 7 AND trips.trip_distance <=10 THEN 1 ELSE 0 END) AS "In between 7 (exclusive) and 10 miles (inclusive)",
	SUM(CASE WHEN trips.trip_distance > 10 THEN 1 ELSE 0 END) AS "Over 10 miles"
FROM
	public.green_taxi_trips trips
WHERE
	trips.lpep_dropoff_datetime >= '2019-10-01'
	AND trips.lpep_dropoff_datetime < '2019-11-01'
```

#### Question 4. Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.
Answer. The result is `2019-10-31`
```
# SQL Query
SELECT
	DATE(trips.lpep_pickup_datetime) AS "DATE_WITH_LONGEST_TRIP"
FROM
	public.green_taxi_trips trips
GROUP BY
	DATE(trips.lpep_pickup_datetime)
ORDER BY
	MAX(trips.trip_distance) DESC
LIMIT 1
```

#### Question 5. Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18? Consider only lpep_pickup_datetime when filtering by date.
**- East Harlem North, East Harlem South, Morningside Heights**
**- East Harlem North, Morningside Heights**
**- Morningside Heights, Astoria Park, East Harlem South**
**- Bedford, East Harlem North, Astoria Park**
Answer: The answer is `East Harlem North, East Harlem South, Morningside Heights`
```
# SQL Query
SELECT
	zones."Zone"
FROM
	public.green_taxi_trips trips
INNER JOIN 
	public.taxi_zones zones
ON
	trips."PULocationID" = zones."LocationID"
WHERE
	DATE(trips.lpep_pickup_datetime) = '2019-10-18'
GROUP BY
	zones."Zone"
HAVING
	SUM(trips.total_amount) > 13000
LIMIT 3
```

#### Question 6. For the passengers picked up in October 2019 in the zone named "East Harlem North" which was the drop off zone that had the largest tip?
Answer: The result is `East Harlem North`.
```
# SQL Query

SELECT
	do_zones."Zone"
FROM
	public.green_taxi_trips trips
INNER JOIN 
	public.taxi_zones pu_zones
ON
	trips."PULocationID" = pu_zones."LocationID"
INNER JOIN 
	public.taxi_zones do_zones
ON
	trips."DOLocationID" = do_zones."LocationID"
WHERE
	DATE(trips.lpep_pickup_datetime) >= '2019-10-01'
	AND DATE(trips.lpep_pickup_datetime) < '2019-11-01'
	AND pu_zones."Zone" = 'East Harlem North'
GROUP BY
	do_zones."Zone"
ORDER BY
	max(trips.tip_amount) DESC
LIMIT 1
```

#### Question 7. Which of the following sequences, respectively, describes the workflow for:
**- Downloading the provider plugins and setting up backend,**
**- Generating proposed changes and auto-executing the plan**
**- Remove all resources managed by terraform**
Answer: The answer is `terraform init, terraform apply -auto-approve, terraform destroy`.