#!/bin/sh
pip-review --auto
pip freeze > ./requirements.txt
