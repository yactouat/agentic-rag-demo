#!/bin/bash

# Get the PID of the streamlit process
pid=$(ps aux | grep streamlit | awk '{print $2}')

# Check if the PID exists
if ps -p $pid > /dev/null
then
  echo "Streamlit process with PID $pid exists. Killing the process..."
  kill -9 $pid
  echo "Streamlit process killed successfully."
else
  echo "Streamlit process with PID $pid does not exist. Not doing anything..."
fi