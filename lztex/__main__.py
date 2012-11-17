#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lztex
import argparse

def get_shell_args():
    '''Get command line arguments for initialize program'''
    # TODO write a user-friendly description

    parser = argparse.ArgumentParser(description="(a desc to this prog)")
    parser.add_argument('files', metavar='FILE', nargs='*',
                        type=argparse.FileType('r'),
                        help='(input file help desc)')
    args = parser.parse_args()

    return args

def py2_handler():
    # FIXME simple input handler for python2
    # TODO remove this
    try:
        global input
        input = raw_input
    except:
        pass

# FIXME quick hack for build-in help.
def LzTeX():
    '''some help?
    
    No <=, use =< instead (Haskell style).'''

def run():
    py2_handler()
    args = get_shell_args()

    if not args.files:
        welcome_message = '''
        LzTeX beta preview (nightly build: Thu, 19 Jul 2012 03:12:35 +0700)
          Quick Docs: Type a document in LzTeX format when prompt.
          On empty line hit ^D to see result, and hit ^D again to quit.
        '''.strip().replace('    ', '')
        print(welcome_message)
        while True:
            try:
                s = input('>>> ')

                # FIXME quick hack for invoke intepreter help command.
                if s == r'\h':
                    pass
                    #help(LzTeX)
                elif s == r'\q':
                    raise EOFError
                else:
                    while True:
                        try:
                            s += '\n'
                            s += input('... ')
                        except (EOFError, KeyboardInterrupt):
                            print('')
                            output = lztex.parse(s)
                            print(output)
                            break
            except (EOFError, KeyboardInterrupt):
                print('')
                exit('bye ^^)/')
    else:
        import os
        for in_file in args.files:
            output = lztex.parse(in_file.read())

            file_name, file_ext = os.path.splitext(in_file.name)

            # TODO check if .tex file already exists before overwrite it!
            out_file = open(file_name + '.tex', 'w')
            out_file.write(output)

            in_file.close()
            out_file.close()

if __name__ == '__main__':
    run()

