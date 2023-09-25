import json
import logging

from enums import KafkaTopic
from handlers import user_registration_handler
from kafka import KafkaConsumer

from app.core.config import settings

bootstrap_servers = str(settings.KAFKA_URI)[8::]


def deserialize_message(message: bytes) -> dict:
    return json.loads(message.decode("utf-8"))


kafka_topic_handlers = {
    KafkaTopic.USER_REGISTRATION: user_registration_handler,
}
topics = [KafkaTopic.USER_REGISTRATION]  # Use topic that you need here
consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers, value_deserializer=deserialize_message)

logger = logging.getLogger(__name__)


def consume_messages(topics_list: list[KafkaTopic]):
    consumer.subscribe([topic.value for topic in topics_list])
    while True:
        try:
            for message in consumer:
                topic_name = KafkaTopic(message.topic)
                topic_handler = kafka_topic_handlers.get(topic_name)
                if topic_handler:
                    print(f"Received message for topic {topic_name}: {message.value}")
                    topic_handler.delay(message.value)
                    print("Hello, I'm listening topics from loans service")
        except Exception as e:
            logger.exception("An error occurred while consuming messages", exc_info=e)


print("I'M ALIVE")
if __name__ == "__main__":
    consume_messages(topics)
