# Caching Proxy Server
> Minimalistic caching proxy server.

## Purpose
Speed-up ⏩: the process of requests by caching 🗄️ their results on a proxy server.

## Usage
### Kafka setup 🌊
This project uses Kafka on Docker as described [here](https://developer.confluent.io/confluent-tutorials/kafka-on-docker/).
#### TL;DR
First, install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and setup an account in [Docker Hub](https://hub.docker.com/explore). Other than that, we do not need to install anything else (like Zookeeper).
After that, use the `kafka/docker-compose.yml` to spin up the container. Edit the `.yml` file for your needs


##### Launching the container
Make sure to start the Docker daemon beforehand.

```
docker compose up -d
```

##### Viewing logs to verify that Kafka is working
```
docker logs broker # or howevert you named the service
```

##### Creating a new Kafka topic
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
To monitor the proxy server metrics, you can run Prometheus in Docker and configure it to scrape metrics from your Python app using the prometheus_client library.

#### Create Prometheus Config File 📁
Create a file named `prometheus.yml` in your project root with the following contents:

```yml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'caching-proxy-server'
    static_configs:
      - targets: ['host.docker.internal:8000']
```
host.docker.internal allows Prometheus running in a Docker container to access the host machine (your app must call start_http_server(8000) in code).

>If you're using Linux and host.docker.internal doesn't work, replace it with your actual local IP (e.g. 192.168.1.5:8000) or run everything inside the same Docker network.

#### Create Docker Compose Entry for Prometheus 🐳
Add this to your docker-compose.yml or create a new one:

```yaml
version: '3.7'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - 9090:9090
```
Then run:

```bash
docker-compose up -d prometheus
```
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
