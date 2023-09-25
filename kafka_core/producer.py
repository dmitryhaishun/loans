import json
from typing import Any

from kafka import KafkaProducer

from app.core.config import settings

bootstrap_servers = str(settings.KAFKA_URI)[8::]


def serialize_message(value: Any) -> bytes:
    return json.dumps(value).encode("utf-8")


def send_to_kafka(topic: str, message: Any) -> None:
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=serialize_message)
    producer.send(topic, message)
    producer.flush()
    producer.close()
