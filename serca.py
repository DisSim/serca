import flask
import yaml
import kafka # https://github.com/dpkp/kafka-python
import secrets
import json

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
    body['_status'] = new
    with kafka.KafkaProducer(
        bootstrap_servers=queue_cnf.get("host", "localhost"),
        value_serializer=lambda v: json.dumps(v).encode(queue_cnf.get("encoding",'utf-8'))) as queue:
    future = queue.send(operation, body)
    res = future.get(timeout=queue_cnf['timeout', 10])
    return {'topic': res.topic, 'partition': res.partition, 'offset': res.offset, '_secret': secret}

"""
Get status from queue
"""
# TODO
def q_status(operation, offset, secret):
    with kafka.KafkaConsumer(operation,
                         bootstrap_servers=queue_cnf.get("host", "localhost")) as queue:
        result = [message in queue if message.topic.decode(
            queue_cnf.get("encoding",'utf-8'))==operation
               and message.offet.decode(queue_cnf.get("encoding",'utf-8'))==offset]
        if len(result) == 0:
            return {}
        else:
            res = result[0]
            if res_secret == secret:
                return res['_status'].decode(queue_cnf.get("encoding",'utf-8'))
            else:
                return {}

"""
Get from queue iff key matches
"""
# TODO
def q_get(operation, offset, secret):
    with kafka.KafkaConsumer(operation,
                         bootstrap_servers=queue_cnf.get("host", "localhost")) as queue:
        result = [message in queue if message.topic.decode(
            queue_cnf.get("encoding",'utf-8'))==operation
               and message.offet.decode(queue_cnf.get("encoding",'utf-8'))==offset]
        if len(result) == 0:
            return {}
        else:
            res = result[0]
            res.update({n: res[n].decode(queue_cnf.get("encoding",'utf-8')) for n in res.keys()})
            res_secret = res.pop('_secret', None)
            if res_secret == secret:
                return res
            else:
                return {}

# Routes
routes = Flask(__name__)
"""
POST a task
input: {'function': function, 'params': [...params]}
output: {'id': #, 'key': (alphanumeric key)}
"""
@routes.route("/new/task/<operation>", methods=['POST'])
def newtask(operation):
    return json.dumps(q_add(operation, request.data))

"""
Get task status
input: id in url
output: {'status': status}
"""
@routes.route("/status/task/<operation>/<offset>")
def newtask(operation, offset):
    return q_status(operation, offset)

"""
Get task result
input: id in url, key (from post step return) as authentication in header
output: {'datatype': datatype, 'output': (the output from the task)}
"""
@routes.route("/get/task/<operation>/<offset>")
def newtask(operation, offset):
    secret = request.headers.get('authorization')
    return q_get(operation, offset, secret)

"""
CORS
"""
@routes.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response


if __name__ == '__main__':
    app.run()
