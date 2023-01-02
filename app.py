from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random, randint  
from datetime import datetime
from pymongo import MongoClient
from format_data import save_data, send_data
from pass_mongo import pass_mongo
import pytz


pass_mongo = pass_mongo()
CONNECTION_STRING = "mongodb://danangwahyu:{}@ac-d7hxbx4-shard-00-00.u7vhogz.mongodb.net:27017,ac-d7hxbx4-shard-00-01.u7vhogz.mongodb.net:27017,ac-d7hxbx4-shard-00-02.u7vhogz.mongodb.net:27017/?ssl=true&replicaSet=atlas-n0tl0g-shard-0&authSource=admin&retryWrites=true&w=majority".format(pass_mongo)

client = MongoClient(CONNECTION_STRING)
dbname = client["vital_signs"]
db_ir = dbname["raw_ir"]
db_bp = dbname["blood_pressure"]
db_heat = dbname["heat_body"]
db_heart = dbname["heart_rate"]
db_oksi = dbname["oksi"]

last_bp_id = None
last_heat_id = None
last_heart_id = None
last_oksi_id = None

tmzone = pytz.timezone('asia/jakarta')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')

"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

"""
Generate random sequence of dummy sensor values and send it to our clients
"""

def background_thread(ev):
    while True:
        dummy_sensor_value = round(random() * 100, 3)
        socketio.emit(ev, {'value': dummy_sensor_value, "date": get_current_datetime()})
        socketio.sleep(1)

"""
Serve root index file
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
Decorator for connect
"""
@socketio.on('save_data')
def save_data(message):
    data_heart = message['data_heart']
    data_heat = message['data_heat']
    data_oksi = message['data_oksi']
    data_ir = message['data_ir']
    data_bp = randint(50, 120)

    # print(type(data_ir))
    db_ir.insert_one(save_data(data_ir))
    db_heat.insert_one(save_data(data_heat))
    db_heart.insert_one(save_data(data_heart))
    db_oksi.insert_one(save_data(data_oksi))
    db_bp.insert_one(save_data(data_bp))

    socketio.emit('tempel', {'data': 'data_heart: {}, data_heat: {}, data_oksi: {}'.format(str(type(data_heart)), str(type(data_bp)), data_heat)})
    



@socketio.on('bp')
def connect():
    socketio.start_background_task(background_thread('resp_heart_rate'))

@socketio.on('heat_body')
def connect():
    socketio.start_background_task(background_thread('resp_bp'))

@socketio.on('heart_rate')
def connect():
    socketio.start_background_task(background_thread('resp_heat_body'))

@socketio.on('oksi')
def connect():
    socketio.start_background_task(background_thread('resp_oksi'))

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app)