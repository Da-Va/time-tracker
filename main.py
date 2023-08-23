#!/usr/bin/env python3

import sys
import subprocess

def main(argv):
    smenu_command = 'smenu'

    smenu_args = [
        smenu_command,
        '-r' #Enable Confirmation in seach mode
    ]

    tasks = "one two three four five"

    selection = subprocess.check_output(smenu_args, input=tasks.encode()) 
    selection = selection.decode()

    print("Selection: ", selection)


    
if __name__=='__main__':
    main(sys.argv)