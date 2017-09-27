# Introduction

This is a proxy to translate the KairosDB submission protocol to InfluxDB. The
proxy only supports KairosDB's JSON protocol. There is no support for translating
queries. Any queries must be rewritten to use the InfluxDB protocol, and query
language.

# Requirements

- Python 3
- Flask
- Flask-RESTful
- InfluxDB
- PyYAML

# Configuration

Edit conf/proxy.yml. Specify the hostname, port, login, and database used to
store the datapoints. Set debug_mode to True, to enable debugging in Flask.