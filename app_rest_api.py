from flask import Flask, request
# from flask_pymongo import PyMongo
from flask_restful import Resource, Api
from flask_cors import CORS
import random 
from pymongo import MongoClient
from format_data import save_data, send_data
from pass_mongo import pass_mongo
from bson.json_util import dumps, loads
from datetime import datetime
import pytz
from bson import ObjectId
from flask_socketio import SocketIO, emit

 
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


app = Flask(__name__)

api = Api(app)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

tmzone = pytz.timezone('asia/jakarta')

class add_data(Resource):
    def post(self):
        data_heart = float(request.form["data_heart"])
        data_heat = float(request.form["data_heat"])
        data_oksi = float(request.form["data_oksi"])
        data_IR = float(request.form["data_IR"])

        db_ir.insert_one(save_data(data_IR))
        db_heat.insert_one(save_data(data_heat))
        db_heart.insert_one(save_data(data_heart))
        db_oksi.insert_one(save_data(data_oksi))

        # replace kapan kapan
        data_bp = float(random.randint(50, 120))
        db_bp.insert_one(save_data(data_bp))

        return {"msg": "Data tersimpan"}

class bp(Resource):
    def get(self):
        global last_bp_id
        global tmzone
        if last_bp_id == None:
            last_bp_id = db_bp.find().sort('_id', -1).limit(3)[0]['_id']
        last_data = db_bp.find({
            '_id':{
                '$gt': last_bp_id
            }
        }).limit(1)
        try:
            last_bp_id = last_data[0]['_id']
            time = last_bp_id.generation_time.astimezone(tmzone)
            data = last_data[0]['data']
            return send_data(time.hour, time.minute, data)
        except:
            return {'msg' : "noting"}

class heat(Resource):
    def get(self):
        global last_heat_id
        global tmzone
        if last_heat_id == None:
            last_heat_id = db_heat.find().sort('_id', -1).limit(3)[0]['_id']
        last_data = db_heat.find({
            '_id':{
                '$gt': last_heat_id
            }
        }).limit(1)
        try:
            last_heat_id = last_data[0]['_id']
            time = last_heat_id.generation_time.astimezone(tmzone)
            data = last_data[0]['data']
            return send_data(time.hour, time.minute, data)
        except:
            return {'msg' : "noting"}

class oksi(Resource):
    def get(self):
        global last_oksi_id
        global tmzone
        if last_oksi_id == None:
            last_oksi_id = db_oksi.find().sort('_id', -1).limit(3)[0]['_id']
        last_data = db_oksi.find({
            '_id':{
                '$gt': last_oksi_id
            }
        }).limit(1)
        try:
            last_oksi_id = last_data[0]['_id']
            time = last_oksi_id.generation_time.astimezone(tmzone)
            data = last_data[0]['data']
            return send_data(time.hour, time.minute, data)
        except:
            return {'msg' : "noting"}

class heart(Resource):
    def get(self):
        global last_heart_id
        global tmzone
        if last_heart_id == None:
            last_heart_id = db_heart.find().sort('_id', -1).limit(3)[0]['_id']
        last_data = db_heart.find({
            '_id':{
                '$gt': last_heart_id
            }
        }).limit(1)
        try:
            last_heart_id = last_data[0]['_id']
            time = last_heart_id.generation_time.astimezone(tmzone)
            data = last_data[0]['data']
            return send_data(time.hour, time.minute, data)
        except:
            return {'msg' : "noting"}

api.add_resource(add_data, "/send", methods = ["POST"])
api.add_resource(bp, "/bp", methods = ["GET"])
api.add_resource(heat, "/heat", methods = ["GET"])
api.add_resource(oksi, "/oksi", methods = ["GET"])
api.add_resource(heart, "/heart", methods = ["GET"])


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


if __name__ =="__main__":
    socketio.run(app, debug=True)
    # app.run(debug=True)
