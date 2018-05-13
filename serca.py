import flask
import yaml
import kafka # https://github.com/dpkp/kafka-python
import secrets

# read config
with open('serca.yml') as config:
    cnf = yaml.load(config)
    queue_cnf = cnf.get('queue', {})
"""
Add to the queue.
the operation is the queue channel name
"""
def q_add(body, operation):
    secret = secrets.token_hex(queue_cnf.get('secret_len', 32))
    body['_secret'] = secret
    with kafka.KafkaProducer(
        bootstrap_servers=queue_cnf.get("host", "localhost"),
        value_serializer=lambda v: json.dumps(v).encode(queue_cnf.get("encoding",'utf-8'))) as queue:
    future = queue.send(operation, key, body)
    res = future.get(timeout=queue_cnf['timeout', 10])
    return {'topic': res.topic, 'partition': res.partition, 'offset': res.offset, '_secret'}

"""
Get from queue iff key matches
"""
# TODO
def q_get(operation, offset, secret):
    with kafka.KafkaConsumer(operation,
                         bootstrap_servers=queue_cnf.get("host", "localhost")) as queue:
        res = [message in queue where message.topic.decode(
            queue_cnf.get("encoding",'utf-8'))==operation
               and message.offet.decode(queue_cnf.get("encoding",'utf-8'))==offset]
        if len(res) == 0:
            return {}
        else:
            res.update({n: res[n].decode(queue_cnf.get("encoding",'utf-8')) for n in res.keys()})
            res_secret = res.pop('_secret', None)
            if res_secret == secret:
                return res[0]
            else:
                return {}

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
