from flask import Flask, request
from flask_pymongo import PyMongo
from flask_restful import Resource, Api
from flask_cors import CORS
import random 

app = Flask(__name__)
app.config["SECRET_KEY"] = "f9cfa0be9fc687395abc02588cba4ae3efb4c496"
# app.config["MONGO_URI"] = "mongodb+srv://danangwahyu:Semangat45@cluster0.u7vhogz.mongodb.net/?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb://danangwahyu:Semangat45@ac-d7hxbx4-shard-00-00.u7vhogz.mongodb.net:27017,ac-d7hxbx4-shard-00-01.u7vhogz.mongodb.net:27017,ac-d7hxbx4-shard-00-02.u7vhogz.mongodb.net:27017/?ssl=true&replicaSet=atlas-n0tl0g-shard-0&authSource=admin&retryWrites=true&w=majority"

# mongodb database
mongodb_client = PyMongo(app)
db = mongodb_client.db

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
