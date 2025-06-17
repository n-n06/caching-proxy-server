from confluent_kafka import Consumer, KafkaError
import json

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
                log = json.loads(msg.value().decode("utf-8"))
                print(f"[{log['method']} {log['path']}] "
                      f"Status: {log['status_code']} | "
                      f"Cache: {log['cache_status']} | "
                      f"Time: {log['duration']}ms")
            except json.JSONDecodeError:
                print("Invalid JSON:", msg.value())
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        print("Consumer stopped.")

if __name__ == "__main__":
    main()
