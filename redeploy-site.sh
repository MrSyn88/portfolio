#!/bin/bash

echo "Deploying..."
if 
! cd portfolio || exit
! git fetch && git reset origin/main --hard
! source python3-virtualenv/bin/activate
! pip install -r requirements.txt
! systemctl daemon-reload
! systemctl restart myportfolio
then
     echo "Deployment FAILED"
else
     echo "Deployment Success"
fi