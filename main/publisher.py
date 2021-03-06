#!/usr/bin/env python

import json
import opflow
import sys

from misc import Misc

cmdargs = Misc.args_parser(sys.argv[1:], cmd_name=sys.argv[0])

publisher = opflow.PubsubHandler(**{
    'uri': 'amqp://%s/' % cmdargs['uri'],
    'exchangeName': 'tdd-opflow-publisher',
    'routingKey': 'tdd-opflow-pubsub-public',
    'applicationId': 'FibonacciGenerator'
})

if cmdargs['number'] is None:
    for i in range(20, 40):
        publisher.publish(json.dumps({ 'number': i }))
else:
    print '[+] number: %s' % cmdargs['number']
    publisher.publish(json.dumps({ 'number': cmdargs['number'] }))

print(' [*] Exit!')
