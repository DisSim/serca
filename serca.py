import flask
import yaml
import pika

# read config
with open('serca.yml') as config:
    cnf = yaml.load(config)
    queue_cnf = cnf.get('queue', {})

# queue (rabitmq) connection
q_creds = pika.credentials.PlainCredentials(queue_cnf.get('username', 'guest'),
                                            queue_cnf.get('password', 'guest'))
q_params = pika.ConnectionParameters(queue_cnf.get('host', 'localhost'),
                                     queue_cnf.get('port', 5672),
                                     queue_cnf.get('path', '/'),
                                     q_creds)
# Helper functions
"""
Add to the queue.
the operation is the queue channel name
"""
def q_add(body, operation):
    with pika.BlockingConnection(q_params) as connection:
        channel = connection.channel()
        channel.queue_declare(queue=operation)
        channel.basic_publish(routing_key=operation, body=body)

"""
Task status from queue
"""
# TODO

"""
Get from queue iff key matches
"""
# TODO

# Routes

"""
Post a task
input: {'function': function, 'params': [...params]}
output: {'id': #, 'key': (alphanumeric key)}
"""
# TODO

"""
Get task status
input: id in url
output: {'started': epochtime, 'status': status}
"""
# TODO

"""
Post a task
input: id in url, key (from post step return) as authentication in header
output: {'datatype': datatype, 'output': (the output from the task)}
"""
# TODO
