#!/bin/bash

# ACTIVATE VIRTUAL ENV
echo "Enabling python environment"
. /opt/venv/bin/activate

if [ "$1" == "production" ];
then
    #### # NORMAL APP
    echo "Activate nginx"
    /etc/init.d/nginx start
    echo "Uwsgi app"
    uwsgi --ini /etc/uwsgi/vassals/uwsgi.ini
else
    ### # TEST irods and graphdb
    echo "Waiting for irods to be started"
    sleep 30
    curl -i -X POST \
        http://neo4j:neo4j@neo:7474/user/neo4j/password \
        -d 'password=test'
    yes test | iinit
    python /app/run.py
fi
