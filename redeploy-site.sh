#!/bin/bash

printf "Deploying...\n\n"
if
! cd portfolio
! git fetch && git reset origin/main --hard
! source python3-virtualenv/bin/activate
! pip install -r requirements.txt
! systemctl daemon-reload
! systemctl restart myportfolio
then
     printf "\n\nDeployment FAILED\n"
else
     printf "\n\nDeployment SUCCESS\n"
fi