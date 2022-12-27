from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import random 

app = Flask(__name__)
api = Api(app)
CORS(app)

data_bp = random.randint(0, 9)
data_heat = random.randint(10, 19)
data_oksi = random.randint(20, 29)
data_heart = random.randint(30, 39)

class bp(Resource):
    def get(self):
        return {"blood_pressure": data_bp}

class heat(Resource):
    def get(self):
        return {"heat_body": data_heat}

class oksi(Resource):
    def get(self):
        return {"oksi": data_oksi}

class heart(Resource):
    def get(self):
        return {"heart_rate": data_heart}

api.add_resource(bp, "/bp", methods = ["GET"])
api.add_resource(heat, "/heat", methods = ["GET"])
api.add_resource(oksi, "/oksi", methods = ["GET"])
api.add_resource(heart, "/heart", methods = ["GET"])

if __name__ =="__main__":
    app.run(debug=True)
