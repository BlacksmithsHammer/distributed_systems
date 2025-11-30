import pika
import json
import time
import random
import os

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'admin123')

OPERATIONS = ['add', 'subtract', 'multiply', 'divide', 'power', 'invalid']

def connect_rabbitmq():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        credentials=credentials,
        heartbeat=600
    )
    
    for attempt in range(30):
        try:
            connection = pika.BlockingConnection(parameters)
            print(f"Connected to RabbitMQ")
            return connection
        except Exception as e:
            print(f"Attempt {attempt + 1}/30: Waiting for RabbitMQ... {e}")
            time.sleep(2)
    
    raise Exception("Could not connect to RabbitMQ")

def setup_exchanges_and_queues(channel):
    # Main exchange
    channel.exchange_declare(
        exchange='calc_exchange',
        exchange_type='direct',
        durable=True
    )
    
    # DLX exchange
    channel.exchange_declare(
        exchange='dlx_exchange',
        exchange_type='direct',
        durable=True
    )
    
    # DLQ queue
    channel.queue_declare(
        queue='dlq_queue',
        durable=True
    )
    channel.queue_bind(
        queue='dlq_queue',
        exchange='dlx_exchange',
        routing_key='dlq'
    )
    
    # Main queue with DLX
    channel.queue_declare(
        queue='calc_queue',
        durable=True,
        arguments={
            'x-dead-letter-exchange': 'dlx_exchange',
            'x-dead-letter-routing-key': 'dlq'
        }
    )
    channel.queue_bind(
        queue='calc_queue',
        exchange='calc_exchange',
        routing_key='calculate'
    )
    
    print("Exchanges and queues configured")

def generate_task():
    operation = random.choice(OPERATIONS)
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    
    if operation == 'divide' and random.random() < 0.3:
        b = 0
    
    task = {
        'id': random.randint(1000, 9999),
        'operation': operation,
        'a': a,
        'b': b,
        'timestamp': time.time()
    }
    return task

def main():
    print("Producer starting...")
    
    connection = connect_rabbitmq()
    channel = connection.channel()
    
    setup_exchanges_and_queues(channel)
    
    message_count = 0
    
    try:
        while True:
            task = generate_task()
            message_count += 1
            
            channel.basic_publish(
                exchange='calc_exchange',
                routing_key='calculate',
                body=json.dumps(task),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type='application/json'
                )
            )
            
            print(f"[{message_count}] Sent: {task['operation']}({task['a']}, {task['b']}) id={task['id']}")
            
            time.sleep(random.uniform(1, 3))
            
    except KeyboardInterrupt:
        print("Producer stopped")
    finally:
        connection.close()

if __name__ == '__main__':
    main()
