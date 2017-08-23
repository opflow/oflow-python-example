#!/usr/bin/env python

import json
import opflow
import signal
import sys

from fibonacci import FibonacciGenerator
from misc import Misc

cmdargs = Misc.args_parser(argv=sys.argv[1:], cmd_name=sys.argv[0], has_number=False)

worker = opflow.RpcWorker(**{
    'uri': 'amqp://%s/' % cmdargs['uri'],
    'exchangeName': 'tdd-opflow-exchange',
    'routingKey': 'tdd-opflow-rpc',
    'operatorName': 'tdd-opflow-queue',
    'responseName': 'tdd-opflow-feedback',
    'applicationId': 'FibonacciGenerator'
})

def callback(body, headers, response):
    try:
        # OPTIONAL
        response.emitStarted()
        print("[x] started")

        data = json.loads(body)
        print("[-] input data: %s" % (data))

        if data['number'] < 0:
            print('[-] number should be positive')
            raise opflow.OperationError('The number should be positive')

        if data['number'] > 40:
            print('[-] number is greater than 40')
            raise opflow.OperationError('The number exceeding limit (40)')

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

    except opflow.OperationError as error:
        # MANDATORY
        response.emitFailed(json.dumps({ 'msg': 'Internal exception' }))

    except Exception as error:
        # MANDATORY
        response.emitFailed(json.dumps({ 'msg': 'General exception' }))

info = worker.process(None, callback)

print(' [*] Waiting for message. To exit press CTRL+C')

def signal_term_handler(signal, frame):
    print 'SIGTERM/SIGINT'
    worker.close()

signal.signal(signal.SIGINT, signal_term_handler)
signal.signal(signal.SIGTERM, signal_term_handler)

worker.retain()

print(' [*] Exit!')
