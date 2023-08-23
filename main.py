#!/usr/bin/env python3

import sys
import subprocess
import json

def main(argv):
    config_file = 'example_config.json'
    with open(config_file, 'r') as config_f:
        config = json.load(config_f)

    smenu_command = 'smenu'

    smenu_args = [
        smenu_command,
        '-m', 'Select activity:',
        '-r', #Enable Confirmation in seach mode.
        '-t', '1', #Set single collumn.
        '-W', '\n',
        '-N',
        '-D', 'd:_',
    ]

    tasks = [ t['name'] + 5*' ' + ','.join(t['tags']) for t in config['activities'] ]
    tasks = '\n'.join(tasks)

    selection = subprocess.check_output(smenu_args, input=tasks, text=True)

    print(f"Selection: '{selection}'")



if __name__=='__main__':
    main(sys.argv)
