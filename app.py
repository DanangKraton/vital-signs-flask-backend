from flask import Flask, render_template, request, session
from flask_socketio import SocketIO
from random import random, randint  
from datetime import datetime
from pymongo import MongoClient
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

db_ir.insert_one({'data': 0})
db_heat.insert_one({'data': 0})
db_heart.insert_one({'data': 0})
db_oksi.insert_one({'data': 0})
db_bp.insert_one({'data': 0})

tmzone = pytz.timezone('asia/jakarta')



async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*', async_mode=async_mode)
 

"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

"""
Generate random sequence of dummy sensor values and send it to our clients
"""
def background_thread(ev, last_data_id, db):
    while True:
        global last_bp_id 
        global last_heat_id 
        global last_heart_id 
        global last_oksi_id 
        global tmzone

        if last_data_id == None:
            last_data_id = db.find().sort('_id', -1).limit(3)[0]['_id']
        last_data = db.find({
            '_id':{
                '$gt': last_data_id
            }
        }).limit(1)
        try:
            last_data_id = last_data[0]['_id']
            time = last_data_id.generation_time.astimezone(tmzone)
            data = last_data[0]['data']
            socketio.emit(ev, {'value': data, "date": "{}:{}".format(str(time.hour), str(time.minute))})
        except:
            None
            # print('tidak ada')
        socketio.sleep(1)


# def background_thread(ev):
#     while True:
#         dummy_sensor_value = round(random() * 100, 3)
#         socketio.emit(ev, {'value': dummy_sensor_value, "date": get_current_datetime()})
#         socketio.sleep(1)

"""
Serve root index file
"""
# @app.route('/')
# def index():
#     return render_template('index.html', async_mode=socketio.async_mode)

"""
Decorator for connect
"""
@socketio.event
def save_data(message):
    global db_ir
    global db_heart
    global db_heat
    global db_oksi
    global db_bp

    data_heart = float(message['data_heart'])
    data_heat = float(message['data_heat'])
    data_oksi = float(message['data_oksi'])
    data_ir = float(message['data_ir'])
    data_bp = float(randint(50, 120))

    db_ir.insert_one({'data': data_ir})
    db_heat.insert_one({'data': data_heat})
    db_heart.insert_one({'data': data_heart})
    db_oksi.insert_one({'data': data_oksi})
    db_bp.insert_one({'data': data_bp})

    socketio.emit('tempel', {'data': 'data_heart: {}, data_heat: {}, data_oksi: {}'.format(data_heart, data_heat, data_oksi)})
    

@socketio.event()
def heart_rate():
    socketio.start_background_task(background_thread('resp_heart_rate', last_heart_id, db_heart))

@socketio.event
def bp():
    socketio.start_background_task(background_thread('resp_bp', last_bp_id, db_bp))

@socketio.event
def heat_body():
    socketio.start_background_task(background_thread('resp_heat_body', last_heat_id, db_heat))

@socketio.event
def oksi():
    socketio.start_background_task(background_thread('resp_oksi', last_oksi_id, db_oksi))

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)