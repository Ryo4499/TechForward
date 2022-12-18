#!/bin/sh
pip list -o | awk '{print $1}' | xargs pip install -U
