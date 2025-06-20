# Caching Proxy Server
> Minimalistic caching proxy server.

## Purpose
Speed-up ⏩: the process of requests by caching 🗄️ their results on a proxy server.

## Installation 
...

## Usage
### Kafka setup 🌊
This project uses Kafka on Docker as described [here](https://developer.confluent.io/confluent-tutorials/kafka-on-docker/).

First, install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and setup an account in [Docker Hub](https://hub.docker.com/explore). Other than that, we do not need to install anything else (like Zookeeper).
After that, use the `kafka/docker-compose.yml` to spin up the container. Edit the `.yml` file for your needs


#### Launching the container
>Make sure to start the Docker daemon beforehand.

First, spin up the Docker container for the Kafka service.
```
docker compose up -d broker
```

#### Viewing logs to verify that Kafka has started
```
docker logs broker # or howevert you named the service
```

#### Creating a new Kafka topic
Open a command terminal on the Kafka container:
```
docker exec -it -w /opt/kafka/bin broker sh
```

Then create a topic:
```
./kafka-topics.sh --create --topic log-topic --bootstrap-server broker:29092
```

Exit out of the command terminal using `exit`. 

---

### Start the server 🚀:
Start the caching proxy server by running a command like following:
```bash
caching-proxy --port <number> --origin <url>
```
- `--port` is the port on which the caching proxy server will run.
- `--origin` is the URL of the server to which the requests will be forwarded.
For example, if you run the following command:
```bash
caching-proxy --port 3000 --origin http://dummyjson.com
```
The caching proxy server will start on port 3000 and forward requests to http://dummyjson.com.

Taking the above example, if you make a request to http://localhost:3000/products, the caching proxy server will forward the request to http://dummyjson.com/products, return the response along with headers and cache the response. 
#### Response 📎:
In order to clarify from where the response is set, the response has a `X-Cache` header.
- If `X-Cache : HIT` - the response was found in the cache and sent form the proxy server.
- If `X-Cache: MISS` - the response was not found in the cache and fetched from the original server.



### Clear the cache :
```bash
caching-proxy --clear-cache
```


## Advanced - Metrics and Prometheus 
### Setting Up Prometheus with Docker 📊 
To monitor the proxy server metrics, you can run Prometheus in Docker and configure it to scrape metrics from your Python app using the `prometheus_client` library.
To not hardcode the values of the IP address, I designed a Bash script that would do take a `HOST_IP` env variable and place it into the `generated-prometheus.yml` file.

#### Step 1 - setup your host IP as an env variable
```.env
HOST_IP=192.168.x.x
```
This variable will be placed in the template file.
```
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'proxy'
    static_configs:
      - targets: ['${HOST_IP}:8000'] # use your port
```
#### Step 2 - run the script to place the IP address into Prometheus config dynamically
The script `start-prometheus.yml` loads the environment, substitutes the IP address into your config, and runs Docker Compose for the Prometheus service.
Make it executable:
```
chmod +x start-prometheus.sh
```
And run:
```
./start-prometheus.sh
```

#### Step 3 - run the Python script that creates a client for Prometheus
The client starts up on `localhost:8000`. You can edit this settings in the `caching-proxy-server/prometheus/metrics.py` file in the `PROMETHEUS_PORT` constant.
To start the client, execute this command in **the root of the project**
```bash
python3 -m caching_proxy_server.kafka.consumer
```
After running this script, you will see the logs of a Kafka consumer that are then passed to the Prometheus Database.


#### Verify Prometheus ✅ 
- Visit http://localhost:9090
- Go to Status > Targets — you should see your proxy server as a UP target.
- Use the Graph tab to query your custom metrics (e.g., proxy_requests_total, proxy_cache_hit_ratio).

#### Example PromQL Queries
Total requests:
```
sum(proxy_requests_total)
```
Cache hit ratio:
```
proxy_cache_hit_ratio
```
Request durations:
```
histogram_quantile(0.95, rate(proxy_request_duration_bucket[1m]))
```
