#!/bin/bash

# find the PID of the processes having 'streamlit_app.py' in their name
# we use 'pgrep' with '-f' to match against the full process command line

pids=$(pgrep -f "streamlit_app.py")

# check if any PID was found
if [ ! -z "$pids" ]; then
    # loop through each PID and kill the process
    for pid in $pids; do
        kill $pid
        # check if kill command was successful
        if [ $? -eq 0 ]; then
            echo "Process with PID $pid has been stopped."
        else
            echo "Failed to stop process with PID $pid."
        fi
    done
else
    echo "No matching processes found."
fi
