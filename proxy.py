#!/usr/bin/python3

'''
Proxy accepts datapoints using the KairosDB protocol, translating them to InfluxDB.
'''

import os
import yaml
from flask import Flask, request
from flask_restful import Api, Resource
from influxdb import InfluxDBClient

conf_path = os.path.dirname(os.path.abspath(__file__)) + r'/conf/proxy.yml'
config = yaml.load(open(conf_path, 'r'))

app = Flask(__name__)
api = Api(app)

client = InfluxDBClient(
    config['influxdb_host'],
    config['influxdb_port'],
    config['influxdb_user'],
    config['influxdb_pass'],
    config['influxdb_db'])
client.create_database(config['influxdb_db'])

class KairosRequest(Resource):
    def post(self):
        json_request = request.get_json(force=True)

        datapoints = []

        for k in json_request:
            datapoints.append(
                {
                    "measurement": k['name'],
                    "tags": k['tags'],
                    "time": int(k['timestamp']),
                    "fields": {
                        "value": k['value'],
                    }
                }
            )

        client.write_points(datapoints, time_precision='ms')

        return '', 200

api.add_resource(KairosRequest, '/api/v1/datapoints')

if __name__ == '__main__':
    if config['debug_mode'] is True:
        app.run(debug=True)
    else:
        app.run()
