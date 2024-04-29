import random
from flask import Flask, request, jsonify
from time import time

app = Flask(__name__)

sensors = {
    'sensor1': {
        'name': 'sensor1',
        'data': 40,
        'timestamp': int(time() * 1000)
    },
    'sensor2': {
        'name': 'sensor2',
        'data': 60,
        'timestamp': int(time() * 1000)
    },
    'sensor3': {
        'name': 'sensor3',
        'data': 30,
        'timestamp': int(time() * 1000)
    },

}

@app.route('/api/v1/sensors', methods=['GET'])
def get_sensor_data():
    global sensors

    name = request.args.get('name')
    r = random.randint(-2, 2)
    d = sensors[name]['data'] + r

    sensors[name]['data'] = d
    sensors[name]['timestamp'] = int(time() * 1000)

    return sensors[name]

@app.route('/api/v1/sensors/<sensor_name>/setpoint', methods=['POST'])
def set_sensor_setpoint(sensor_name):
    global sensors

    data = request.json
    setpoint = data.get('setpoint')
    sensors[sensor_name]['data'] = setpoint

    return jsonify(success=True)

@app.route('/api/v1/sensors/<sensor_name>', methods=['PUT'])
def update_sensor(sensor_name):
    global sensors

    data = request.json
    setpoint = data.get('setpoint')

    if sensor_name in sensors:
        sensors[sensor_name]['data'] = setpoint
    else:
        sensors[sensor_name] = {
            'name': sensor_name,
            'data': setpoint,
            'timestamp': int(time() * 1000)
        }

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
