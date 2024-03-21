import argparse
import subprocess
from subprocess import PIPE
import sys
import yaml 
import os
from datetime import datetime

def execute(cmd): 
    """
    Executes command using subprocess and consistently reports back to caller
    function output of said command /stack overflow
    """
    proc = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    for stdout_line in iter(proc.stdout.readline, ""): 
        yield stdout_line
    proc.stdout.close() 
    return_code = proc.wait() 
    if return_code: 
        raise subprocess.CalledProcessError(return_code, cmd) 

def main(config_file, recording_name, duration): 

    cmd_list = ['rosbag', 'record'] 

    # Then read the config file for topics
    if config_file is None: 
        cmd_list.append('-a') # Record from all topics 
    else: 
        with open(config_file, 'r') as file: 
            rosbag_config = yaml.safe_load(file) 
            topics = rosbag_config['topics'] 

            # Then add all topics to the cmd list 
            for topic in topics: 
                cmd_list.append(topic) 

    # Check to see we have a recordings directory
    recordings_directory = 'recordings' 
    if not os.path.exists(os.path.join(os.getcwd(), recordings_directory)): 
        os.mkdir(os.path.join(os.getcwd(), recordings_directory))

    recordings_directory = os.path.join(os.getcwd(), recordings_directory)

    # Then we append recording name 
    cmd_list.append('-O') 
    cmd_list.append(os.path.join(recordings_directory, recording_name))

    # Then we appedn the duration 
    cmd_list.append(f'--duration={duration}')

    # Then we attempt to execute the command
    for out in execute(cmd_list): 
        print(out, end="") 

    return 

if __name__ == "__main__": 

    # Create the parser to handle arguments 
    parser = argparse.ArgumentParser(description="start_recording is a helper"
    + " script that starts the recording of ROS bags subject to the configuration"
    + " parameters provided in the arugment list. Thse recordings are then saved"
    + " in the local `./recordings` directory") 


    parser.add_argument('--config_file', '-c', type=str, help='The path to the\
    (yaml) configuration file.')

    parser.add_argument('--recording_name', '-n', type=str, help='The name of\
    the recording.') 

    parser.add_argument('--duration', '-d', type=int, help='Duration of the\
            recording in seconds. (default 60s)')

    args = parser.parse_args() 


    # Check to see if all args are legitimate 
    if args.config_file is None: 
        config_file = None 
    else: 
        config_file = args.config_file

    if args.recording_name is None: 
        recording_name = 'recording' + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '.bag'
    else: 
        recording_name = args.recording_name

    if args.duration is None: 
        duration = 60 # Default 60 second duration 
    else: 
        duration = args.duration 

    # Then call main 
    main(config_file, recording_name, duration)

