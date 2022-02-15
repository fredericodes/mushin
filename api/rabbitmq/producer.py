import pika


def add_to_work_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
                                                                   credentials=pika.credentials.PlainCredentials(
                                                                       "mushin_user", "mushin_pass")))
    channel = connection.channel()
    channel.queue_declare(queue='encryption_uploads', durable=True)

    msg = message

    channel.basic_publish(
        exchange='',
        routing_key='encryption_uploads',
        body=msg,
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()
