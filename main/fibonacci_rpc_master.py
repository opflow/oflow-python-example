#!/usr/bin/env python

import json
import time
import signal
import threading
import opflow
import sys

from misc import Misc

cmdargs = Misc.args_parser(sys.argv[1:], 'rpc_master')

master = opflow.RpcMaster(**{
	'uri': 'amqp://%s/' % cmdargs['uri'],
	'exchangeName': 'tdd-opflow-exchange',
	'routingKey': 'tdd-opflow-rpc',
	'responseName': 'tdd-opflow-feedback',
	'applicationId': 'FibonacciGenerator'
})

def signal_term_handler(signal, frame):
    print 'SIGTERM/SIGINT'
    master.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_term_handler)
signal.signal(signal.SIGTERM, signal_term_handler)

reqs = []
if cmdargs['number'] is None:
    for i in range(20, 40):
        print(" [-] Sent number: %r" % (i))
        req = master.request('fibonacci', json.dumps({ 'number': i }), {
            'timeout': 5
        })
        reqs.append(req)
else:
    print(" [-] Sent number: %r" % (cmdargs['number']))
    req = master.request('fibonacci', json.dumps({ 'number': cmdargs['number'] }), {
        'timeout': 5
    })
    reqs.append(req)

for req in reqs:
    while req.hasNext():
        print ' [-] message: %r' % req.next()

master.close()

print(' [*] Exit!')
