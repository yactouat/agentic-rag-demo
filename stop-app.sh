#!/bin/bash

# check if we have more at least two `python3 -m streamlit run streamlit_app.py` processes running
# shellcheck disable=SC2046
if [ $(ps aux | grep 'python3 -m streamlit run streamlit_app.py' | wc -l) -gt 1 ]; then
    # kill all `python3 -m streamlit run streamlit_app.py` processes
    pkill -f 'python3 -m streamlit run streamlit_app.py'
fi
