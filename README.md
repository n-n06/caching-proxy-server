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

---
##### Launching the container**
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

---

### Clear the cache :
```bash
caching-proxy --clear-cache
```

## Advanced - Metrics and Prometheus 
