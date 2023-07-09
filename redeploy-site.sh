#!/bin/zsh

tmux kill-server
cd portfolio
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
tmux new -d -s prod 'cd ~/portfolio;source python3-virtualenv/bin/activate;flask run --host=0.0.0.0'

