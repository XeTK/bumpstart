
from time import sleep
from yaml import safe_load
from json import dumps as jsonfy

from requests import get, post

from flask import Flask
from flask_cors import CORS

with open('/home/xetk/bumpstart/settings.yaml', 'r') as file:
    config = safe_load(file)

if not config:
    print("No config specified")
    raise 

app = Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

def get_atx_status(url, basic_auth):
    response = get('https://%s/api/atx' % url, headers={'Authorization': 'Basic %s' % basic_auth}, verify=False)

    status_obj = response.json()

    if status_obj['ok'] == True:
        return status_obj['result']

    return None

def set_atx_status(url, status, basic_auth):
    response = post('https://%s/api/atx/power?action=%s' % (url, status), headers={'Authorization': 'Basic %s' % basic_auth}, verify=False)

    status_obj = response.json()

    return status_obj['ok'] 


@app.route("/api/servers")
def list_servers():
    return jsonfy(config['servers'])

@app.route("/api/server/<server_id>")
def get_server(server_id):
    server = config['servers'][server_id]
    
    if server:
        status = get_atx_status(server['ilo'], server['basic_auth'])

        return '{"status": %s}' % str(status['leds']['power']).lower()

    return '{"message": "server not found"}'

@app.route("/api/server/<server_id>/<status>", methods=['POST'])
def set_server(server_id, status):
    if status not in ['on', 'off']:
        return '{"message": "only on or off"}'

    server = config['servers'][server_id]
    
    if server:
        succeeded = set_atx_status(server['ilo'], status, server['basic_auth'])

        if succeeded:
            status = get_atx_status(server['ilo'], server['basic_auth'])

            return '{"status": %s}' % str(status['leds']['power']).lower()

    return '{"message": "server not found"}'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
