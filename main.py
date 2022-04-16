
from time import sleep
from yaml import safe_load
from json import dumps as jsonfy

from flask import Flask
from flask_cors import CORS


from phue import Bridge, PhueRegistrationException

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


SLEEP_TIME = 30

with open('./settings.yaml', 'r') as file:
    config = safe_load(file)

if not config:
    print("No config specified")
    raise 

while True:
    try: 
        bridge = Bridge(config['bridge'])
        break
    except PhueRegistrationException as err:
        print("Failed to connect to bridge: %s" % err.message)
        sleep(SLEEP_TIME)


def get_servers():
    hue_objects = bridge.get_light_objects('name')

    servers = {}

    for server in config['servers']:
        name = server['name']
        if name in hue_objects:
            servers[server['id']] = hue_objects[name]
        else:
            print('No Hue object for: %s ' % name)

    return servers


@app.route("/api/servers")
def list_servers():
    return jsonfy(config['servers'])

@app.route("/api/server/<server>")
def get_server(server):
    servers = get_servers()
    if server in servers:
        return '{"status": %s}' % str(servers[server].on).lower()

    return '{"message": "server not found"}'

@app.route("/api/server/<server>/<status>", methods=['POST'])
def set_server(server, status):
    if status not in ['on', 'off']:
        return '{"message": "only on or off"}'

    servers = get_servers()
    if server in servers:
        servers[server].on = True if status == 'on' else False
        return '{"status": %s}' % str(servers[server].on).lower()

    return '{"message": "server not found"}'