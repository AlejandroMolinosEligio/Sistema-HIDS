#!/bin/sh


python main.py
python TimerHIDS.py
open $(dirname $0)"/main.py"

echo "Hecho"
