#!/bin/bash

. /opt/venv/bin/activate
sleep 30
curl -i -X POST \
    http://neo4j:neo4j@neo:7474/user/neo4j/password \
    -d 'password=test'

yes test | iinit

python /app/run.py
