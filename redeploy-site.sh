#!/bin/bash

printf "Deploying...\n\n"
if
! cd portfolio
! git fetch && git reset origin/main --hard
! docker compose -f docker-compose.prod.yml down
! docker compose -f docker_compose.prod.yml up -d --build
then
     printf "\n\nDeployment FAILED\n"
else
     printf "\n\nDeployment SUCCESS\n"
fi
