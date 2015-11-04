# -*- coding: utf-8 -*-

""" Hello world for uwsgi """

from flask import Flask
from py2neo import Graph, Node
# from neomodel import db
from plumbum.cmd import ils

###########################
# GRAPH
###########################

# Parameters
# // TO FIX:
# Can i find this inside the environment?
protocol = 'http'
host = 'neo'
port = '7474'
user = 'neo4j'
pw = 'test'
# Connection http descriptor
GRAPHDB_LINK = \
    protocol + "://" + user + ":" + pw + "@" + host + ":" + port + "/db/data/"
# os.environ["NEO4J_REST_URL"] = GRAPHDB_LINK
# os.environ["NEO4J_URI"] = GRAPHDB_LINK

######################################
# Check if password change is needed?
# // TO FIX:
# curl -i -X POST http://neo4j:neo4j@neo:7474/user/neo4j/password
# -d 'password=test'
######################################

graph = Graph(GRAPHDB_LINK)
# Remove existing
graph.cypher.execute("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r")
# Test new node
alice = Node("Person", name='Alice')
graph.create(alice)

print("Graph is connected")

###########################
# IRODS
###########################

ils()
print("Irods is connected")

###########################
# FLASK
###########################
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello test World!"

###########################
# main
###########################

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
