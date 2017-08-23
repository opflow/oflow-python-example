#!/usr/bin/env python

import sys, getopt

class Misc(object):
    @classmethod
    def args_parser(cls, argv, cmd_name, has_number=True):
        result = { 'uri': 'localhost' }
        help_message = 'python %s -u <uri>' % cmd_name
        short_opts = 'hu:'
        long_opts = ["uri="]
        if has_number:
            result['number'] = None
            help_message += ' -n <number>'
            short_opts = 'hu:n:'
            long_opts = ["uri=","number="]
        try:
            opts, args = getopt.getopt(argv, short_opts, long_opts)
        except getopt.GetoptError:
            print help_message
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print help_message
                sys.exit(0)
            elif opt in ("-u", "--uri"):
                result['uri'] = arg
            elif has_number and opt in ("-n", "--number"):
                result['number'] = int(arg)
        return result
