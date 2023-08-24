#!/usr/bin/env python3

import sys
import subprocess
import json
import time
import threading
import termios

class tty_stopwatch:
    def __init__(self, start_time) -> None:
        self.running = True
        self.start_time = start_time
        
    def run(self):
        while self.running:
            elapsed_sec = int(time.time() - self.start_time)
            secs = elapsed_sec % 60
            mins = elapsed_sec // 60 % 60
            hours = elapsed_sec // 3600 % 3600

            print(f'{hours:02}:{mins:02}:{secs:02}', end='\r')
            time.sleep(min(0.1, 1 - (time.time() % 1)))
        print()
    
    def __enter__(self):
        self.old_attr = termios.tcgetattr(sys.stdin)
        new_attr = termios.tcgetattr(sys.stdin)
        new_attr[3] = new_attr[3] & ~termios.ECHO & ~termios.ECHONL & ~termios.ICANON
        termios.tcsetattr(sys.stdin, termios.TCSANOW, new_attr)
        
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
    
    def __exit__(self, *args):
        self.running = False
        termios.tcsetattr(sys.stdin, termios.TCSANOW, self.old_attr)
        self.thread.join()

def load_config():
    config_path = 'example_config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)
        
    return config

def activity_user_input(config):
    smenu_command = 'smenu'

    smenu_args = [
        smenu_command,
        '-m', 'Select activity:',
        '-r', #Enable Confirmation in seach mode.
        '-t', '1', #Set single collumn.
        '-W', '\n', #Split tokens by '\n' character.
        '-N', #Enumerate the entries.
        '-D', 'd:_', #Prefix output with its idx.
    ]

    tasks = [ t['name'] + 5*' ' + ','.join(t['tags']) for t in config['activities'] ]
    tasks = '\n'.join(tasks)

    selection = subprocess.check_output(smenu_args, input=tasks, text=True)
    sel_idx = int(selection.split('_')[0]) - 1 if selection else None
    
    return sel_idx, selection

def timer(config):
    start_time = time.time()

    with tty_stopwatch(start_time):
        while True:
            c = sys.stdin.read(1)
            if c == 'q':
                break

    return start_time, time.time() - start_time

def write_log(start_time,  duration):
    pass

def main(argv):
    
    config = load_config()

    sel_idx, selection = activity_user_input(config)

    print(f"Selection: '{selection}' idx: {sel_idx}")
    
    start_time, duration = timer(config)
    
    print(f"start time: {int(start_time)} duration: {int(duration)}")
    
    write_log(start_time, duration)


if __name__=='__main__':
    main(sys.argv)
