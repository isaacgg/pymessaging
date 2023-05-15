from pika.connection import Connection

from event_sourcing.domain.event.message_consumer import MessageConsumer


class PikaConsumer(MessageConsumer):
    def __init__(self, connection: Connection):
        self.connection = connection

    def declare_queue(self, exchange, queue, binding_key):
        retry_queue = f"retry-{queue}"
        dead_letter_queue = f"dead_letter-{queue}"

        self.connection.channel().queue_declare(queue=queue)
        self.connection.channel().exchange_declare(retry_queue)
        self.connection.channel().exchange_declare(dead_letter_queue)

        self.connection.channel().queue_bind(queue=queue, exchange=exchange, routing_key=binding_key)
        # TODO: bind dead letter and retry

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    def consume(self, queue: str):
        self.connection.channel.basic_consume(queue=queue,
                                              auto_ack=False,
                                              on_message_callback=callback)
