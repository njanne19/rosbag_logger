# ROS Bag Recorder
This is a simple ROS bag recorder, designed to be added to projects that wish
to regularly capture data on just a few of the many topics that are currently
being published to. 

For usage, please see the help message: 
```
python start_recording.py -h 
```
```
usage: start_recording.py [-h] [--config_file CONFIG_FILE]
                          [--recording_name RECORDING_NAME]
                          [--duration DURATION]

start_recording is a helper script that starts the recording of ROS bags
subject to the configuration parameters provided in the arugment list. Thse
recordings are then saved in the local `./recordings` directory

optional arguments:
  -h, --help            show this help message and exit
  --config_file CONFIG_FILE, -c CONFIG_FILE
                        The path to the (yaml) configuration file.
  --recording_name RECORDING_NAME, -n RECORDING_NAME
                        The name of the recording.
  --duration DURATION, -d DURATION
                        Duration of the recording in seconds. (default 60s)
```
