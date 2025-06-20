from confluent_kafka import Producer
import json
import time

from .schema import LogMessage
from ..config import logger as global_logger

config = {
    "bootstrap.servers" : "localhost:9092",
    "client.id" : "log-topic"
}

producer : Producer = Producer(config)

def delivery_callback(err, msg):
    if err:
        global_logger.error('Message failed delivery: {}'.format(err))
    else:
        global_logger.info(
            'Message delivered to {} [{}]'.format(
                msg.topic(), 
                msg.partition()
            )
        )


def log_req_kafka(data: LogMessage):
    try:
        message = json.dumps(data)
        producer.produce(
            'log-topic',
            message.encode("utf-8"),
            callback=delivery_callback
        )
        producer.poll(0)
    except Exception as e:
        global_logger.error("Kafka logging error: %s", e)

