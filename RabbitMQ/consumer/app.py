import pika
import json
import time
import os
import traceback

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'admin123')

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

def calculate(operation, a, b):
    if operation == 'add':
        return a + b
    elif operation == 'subtract':
        return a - b
    elif operation == 'multiply':
        return a * b
    elif operation == 'divide':
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    elif operation == 'power':
        return a ** b
    else:
        raise ValueError(f"Unknown operation: {operation}")

def process_message(ch, method, properties, body):
    task = json.loads(body)
    task_id = task.get('id', 'unknown')
    operation = task.get('operation', 'unknown')
    a = task.get('a', 0)
    b = task.get('b', 0)
    
    print(f"[RECEIVED] Task {task_id}: {operation}({a}, {b})")
    
    try:
        result = calculate(operation, a, b)
        print(f"[SUCCESS] Task {task_id}: {operation}({a}, {b}) = {result}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        error_msg = str(e)
        print(f"[FAILED] Task {task_id}: {operation}({a}, {b}) - Error: {error_msg}")
        print(f"[DLQ] Rejecting task {task_id} to Dead Letter Queue")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    print("Consumer starting...")
    
    connection = connect_rabbitmq()
    channel = connection.channel()
    
    channel.basic_qos(prefetch_count=1)
    
    channel.basic_consume(
        queue='calc_queue',
        on_message_callback=process_message,
        auto_ack=False
    )
    
    print("Waiting for messages...")
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Consumer stopped")
    finally:
        connection.close()

if __name__ == '__main__':
    main()
