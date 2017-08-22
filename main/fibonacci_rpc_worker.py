#!/usr/bin/env python

import json
import signal
import opflow

from fibonacci_generator import FibonacciGenerator

worker = opflow.RpcWorker(**{
    'uri': 'amqp://master:zaq123edcx@192.168.56.56/',
    'exchangeName': 'tdd-opflow-exchange',
    'routingKey': 'tdd-opflow-rpc',
    'operatorName': 'tdd-opflow-queue',
    'responseName': 'tdd-opflow-feedback',
    'applicationId': 'FibonacciGenerator'
})

def callback(body, headers, response):
    data = json.loads(body)
    print("[x] input: %s" % (data))

    # OPTIONAL
    response.emitStarted()
    print("[-] started")

    fg = FibonacciGenerator(data['number'])

    # OPTIONAL
    while(fg.next()):
        state = fg.result()
        response.emitProgress(state['step'], state['number'])
        print("[-] step: %s / %s" % (state['step'], state['number']))

    # MANDATORY
    state = json.dumps(fg.result())
    response.emitCompleted(state)
    print("[-] result: %s" % state)

info = worker.process(None, callback)

print(' [*] Waiting for message. To exit press CTRL+C')

def signal_term_handler(signal, frame):
    print 'SIGTERM/SIGINT'
    worker.close()

signal.signal(signal.SIGINT, signal_term_handler)
signal.signal(signal.SIGTERM, signal_term_handler)

worker.retain()

print(' [*] Exit!')