import flask
# TODO pick a queue

# Helper functions
"""
Add to the queue
"""
# TODO

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
