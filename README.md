# Angulask

A project to template flask web server to meet angularjs

## Getting started

```bash
# Clone
git clone https://github.com/pdonorio/angulask.git
# Run (in debug mode)
cd angulask/containers
docker-compose up flask
```

Then go visit http://localhost to access the web page

## Configuration and defaults

To use your personal directory of JSON files configuration
go edit PATH inside `config/__init__.py`, e.g.

```python
PATH = 'MYCONFIGURATION'
```

Config is located in `config/MYCONFIGURATION`.

Default account:

* Username: 'prototype'
* Password: 'test'