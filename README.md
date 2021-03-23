# Http logs consumer

### Overview
The project is intended for consumption of streams of http logs. 
Server analyse the log to find exact hour in working days (Monday to Friday) where most of the users (unique count of IP addresses for that hour) has experienced a server error (status codes 5xx).
To implement the TCP server asyncio was used and to count unique records, a ready-made implementation of HyperLogLog in redis is used https://redislabs.com/redis-best-practices/counting/hyperloglog/


### Requirements
* python 3.8+
* redis
* poetry

### Installation
First of all you need a redis server, the easiest way to spin it up is docker:
```
docker run -d -p 6379:6379 redis
```

Then (inside `/src` directory):
```
poetry install
cp .env.example .env
```

### Usage
```
poetry shell
python launch_server.py
```
As an example of working with the server, you can run one of these bash scripts:
```
./tests/sh_scripts/script_no_1.sh | python stdin_proxy_client.py
./tests/sh_scripts/script_no_2.sh | python stdin_proxy_client.py
```
`stdin_proxy_client.py` internally simply proxies the stdin to the server

Once in a certain period of time (`REDIS_HOUR_STATS_INTERVAL` env variable in seconds) the server will display information about the current number of errors
```
2021-03-23 14:36:31.504 | INFO     | components.server_with_stats:log_stats:37 - Current hour with maximum number of errors 20
2021-03-23 14:36:31.504 | INFO     | components.server_with_stats:log_stats:39 - {
    "0": 9923,
    "1": 9939,
    "2": 9817,
    "3": 9776,
    "4": 9953,
    "5": 9854,
    "6": 9948,
    "7": 9892,
    "8": 9947,
    "9": 9925,
    "10": 9500,
    "11": 9064,
    "12": 9811,
    "13": 9811,
    "14": 9835,
    "15": 9754,
    "16": 9942,
    "17": 9932,
    "18": 9947,
    "19": 9881,
    "20": 9959,
    "21": 9929,
    "22": 9866,
    "23": 9860
}

```
### Configuration
You can config some settings of application via .env file:
```
SERVER_HOST=0.0.0.0
SERVER_PORT=2525
SERVER_TEST_PORT=2222
SERVER_BUFFER_LIMIT_SIZE=65536

REDIS_ADDRESS=redis://localhost/0
REDIS_HOUR_KEY_PREFIX=error_hour_
REDIS_HOUR_STATS_INTERVAL=60

LOG_LEVEL=INFO
LOG_FILENAME=logs/consumer_{time:YYYY-MM-DD}.log
```
For logging https://github.com/Delgan/loguru is used, so you can configure `LOG_FILENAME` with some predefined placeholders

### Tests
```
python -m pytest tests/
```

### Black
```
black .
```
