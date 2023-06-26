# Cars

## How to run
1. `docker build -t cars .`
2. `docker run -p 8000:8000 cars`
3. Visit http://localhost:8000/docs for Swagger documentation
4. Basic functionality can be tested by running `api_test/automated_test.py` file

## Basic info about architecture
- The app is written in the FastAPI framework using Python 3.11.
- It uses a local SQLite database for data storage.
- Deployment is done via a simple Dockerfile.
- There is no need for Docker Compose since a file-system database is used. If a database like PostgreSQL were used, it would have its own Docker image and would be orchestrated with Docker Compose.
- For the reservations it uses UTC time

## Example usage
### Create a new car
```bash
curl --location --request POST 'localhost:8000/car/add' \
--header 'Content-Type: application/json' \
--data-raw '{
    "maker": "volvo",
    "model": "v60",
    "uid": "C123"
}'
```
Response:
```
HTTP/1.1 201 Created
Content-Type: application/json
{"detail":"New car created"}
```

### Make a reservation
```bash
curl --location --request POST 'localhost:8000/reservation/make_reservation' \
--header 'x-requested-with: XMLHttpRequest' \
--header 'Content-Type: application/json' \
--data-raw '{"timestamp_start": 1687530900,
"timestamp_end": 1687530999
}'
```
Response:
```
HTTP/1.1 200 OK
Content-Type: application/json
{
    "start": "2023-06-26T18:18:20",
    "end": "2023-06-26T18:26:40",
    "duration": 0.1388888888888889,
    "car_uid": "C51",
    "car_maker": "volvo",
    "car_model": "v60"
}
```

### See all reservations
```bash
curl --location --request GET 'localhost:8000/reservation/reservations'
```
Response:
```
HTTP/1.1 200 OK
Content-Type: application/json
[
    {
        "timestamp_start": 1687804050,
        "timestamp_end": 1687804150,
        "car_uid": "C51",
        "car_maker": "volvo",
        "car_model": "v60"
    },
    {
        "timestamp_start": 1687804050,
        "timestamp_end": 1687804150,
        "car_uid": "C5678",
        "car_maker": "BMW",
        "car_model": "118d"
    }
]
```