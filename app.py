from flask import Flask, request
# from flask_pymongo import PyMongo
from flask_restful import Resource, Api
from flask_cors import CORS
import random 
from pymongo import MongoClient
from send_data import send_data

CONNECTION_STRING = "mongodb://danangwahyu:Semangat45@ac-d7hxbx4-shard-00-00.u7vhogz.mongodb.net:27017,ac-d7hxbx4-shard-00-01.u7vhogz.mongodb.net:27017,ac-d7hxbx4-shard-00-02.u7vhogz.mongodb.net:27017/?ssl=true&replicaSet=atlas-n0tl0g-shard-0&authSource=admin&retryWrites=true&w=majority"

client = MongoClient(CONNECTION_STRING)
dbname = client["vital_signs"]
db_ir = dbname["raw_ir"]
db_bp = dbname["blood_pressure"]
db_heat = dbname["heat_body"]
db_heart = dbname["heart_rate"]
db_oksi = dbname["oksi"]


app = Flask(__name__)

api = Api(app)
CORS(app)

data_vital_signs = {}

class add_data(Resource):
    def post(self):
        data_heart = float(request.form["data_heart"])
        data_heat = float(request.form["data_heat"])
        data_oksi = float(request.form["data_oksi"])
        data_IR = float(request.form["data_IR"])
        
        data_vital_signs["data_heart"] = data_heart
        data_vital_signs["data_heat"] = data_heat
        data_vital_signs["data_oksi"] = data_oksi
        data_vital_signs["data_IR"] = data_IR
        data_vital_signs["data_bp"] = data_IR**2

        db_ir.insert_one(send_data("raw_ir", data_IR))
        db_bp.insert_one(send_data("blood_pressure", data_IR**2))
        db_heat.insert_one(send_data("heat_body", data_heat))
        db_heart.insert_one(send_data("heart_rate", data_heart))
        db_oksi.insert_one(send_data("oksi", data_oksi))

        return {"msg": "Data tersimpan",
        "data": data_vital_signs}

class bp(Resource):
    def get(self):
        return {"blood_pressure": random.randint(0, 9)}

class heat(Resource):
    def get(self):
        return {"heat_body": random.randint(10, 19)}

class oksi(Resource):
    def get(self):
        return {"oksi": random.randint(20, 29)}

class heart(Resource):
    def get(self):
        return {"heart_rate": random.randint(30, 39)}

api.add_resource(add_data, "/", methods = ["POST"])
api.add_resource(bp, "/bp", methods = ["GET"])
api.add_resource(heat, "/heat", methods = ["GET"])
api.add_resource(oksi, "/oksi", methods = ["GET"])
api.add_resource(heart, "/heart", methods = ["GET"])




if __name__ =="__main__":
    app.run(debug=True)
