from confluent_kafka import Consumer, KafkaError
from prometheus_client import start_http_server

import json

from ..kafka.schema import LogMessage
from ..prometheus.metrics_handlers import (
    inc_request,
    record_duration,
    record_request_size,
    record_response_size,
    update_cache_hit_ratio
)
from ..prometheus.metrics import PROMETHEUS_PORT

# Starting Prometheus server 
start_http_server(PROMETHEUS_PORT)

def main():
    config = {
        "bootstrap.servers" : "localhost:9092",
        "group.id" : "cps-consumers",
        "auto.offset.reset" : "earliest"
    }

    consumer : Consumer = Consumer(config)
    consumer.subscribe(["log-topic"])

    print("Listening for proxy logs... Press Ctrl+C to stop.\n")

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                     print("Consumer error: {}".format(msg.error()))
                continue

            try:               
                data : LogMessage = json.loads(msg.value().decode("utf-8"))

                method = data.get("method")
                path = data.get("path")
                cache = data.get("cache_status", "UNKNOWN")
                status_code = data.get("status_code", 0)
                duration = data.get("duration_ms", 0)
                request_size = data.get("request_size", 0)
                response_size = data.get("response_size", 0)

                # Update Prometheus metrics
                inc_request(method, cache, status_code)
                record_duration(cache, duration)
                record_request_size(request_size)
                record_response_size(response_size)

                if method == "GET":
                    update_cache_hit_ratio(cache == "HIT")

                print(f"[{method} {path}] "
                      f"Status: {status_code} | "
                      f"Cache: {cache} | "
                      f"Time: {duration}ms")

            except json.JSONDecodeError:
                print("Invalid JSON:", msg.value())
            
            except Exception as e:
                print("Unexpected error: ", e)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        print("Consumer stopped.")

if __name__ == "__main__":
    main()
