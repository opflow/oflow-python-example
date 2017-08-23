#!/usr/bin/env python

import json
import opflow
import signal
import sys

from fibonacci import FibonacciGenerator
from misc import Misc

cmdargs = Misc.args_parser(argv=sys.argv[1:], cmd_name=sys.argv[0], has_number=False)

subscriber = opflow.PubsubHandler(**{
    'uri': 'amqp://%s/' % cmdargs['uri'],
    'exchangeName': 'tdd-opflow-publisher',
    'routingKey': 'tdd-opflow-pubsub-public',
    'subscriberName': 'tdd-opflow-subscriber',
    'recyclebinName': 'tdd-opflow-recyclebin',
    'applicationId': 'FibonacciGenerator'
})

def listener(body, headers):
    data = json.loads(body)

    if 'number' not in data:
        print('[+] invalid input data')
        raise opflow.OperationError('Invalid input data')

    print("[x] fibonacci(%s)" % (data['number']))
    
    if data['number'] < 0:
        print('[-] number should be positive')
        raise opflow.OperationError('The number should be positive')

    if data['number'] > 40:
        print('[-] number is greater than 40')
        raise opflow.OperationError('The number exceeding limit (40)')

    fg = FibonacciGenerator(data['number'])
    print("[-] result: %s" % json.dumps(fg.finish()))

subscriber.subscribe(listener)

print('[*] Waiting for message. To exit press CTRL+C')

def signal_term_handler(signal, frame):
    print 'SIGTERM/SIGINT'
    subscriber.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_term_handler)
signal.signal(signal.SIGTERM, signal_term_handler)

subscriber.retain()

print('[*] Exit!')
