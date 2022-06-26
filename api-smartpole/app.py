from flask import Flask, render_template, Response, request, redirect, url_for, session, flash, jsonify ,make_response
from flask_socketio import SocketIO,emit
import cv2
import os
import json
import queue
import threading
import imutils
from config import *
import pymysql
from flask_cors import CORS
from RtspCapture import RtspCapture
import time
from flask_mqtt import Mqtt
# import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'smartpole_phuket_1'
app.config['JSON_AS_ASCII'] = False
CORS(app)

topic = 'touch/smartpole/intercom'
app.config['MQTT_BROKER_URL'] = 'touch-iot.touch-ics.com'
app.config['MQTT_BROKER_PORT'] = 1883
mqtt = Mqtt(app)

def connect_db():
    return pymysql.connect(host=DBHOST, user=DBUSER, port=DBPORT, password=DBPASS, db=DBNAME)
			
def readData():
    conn = connect_db()
    datecurentFix = []
    rows=[]
    count=0
    with conn:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("select * from  pole")
        rows = cur.fetchall()
        cur.close()
        if rows:
            for data in rows:
                data_json = {
                    "id" : data['id'],
                    "status" : data['status'],
                    "position" : {"latitude":data['latitude'],"longitude":data['longitude'],"location":data['location']},
                    "Streaming" : {"cctv1":data['cctv1'],"cctv2":data['cctv2'],"intercom":data['intercom']}
                }
                datecurentFix.append(data_json)
        return datecurentFix

@app.route('/api/smartpole')
def showData():
    return jsonify(readData()),200


@app.route('/restart')
def restartapi():
    os.system("systemctl restart restart_api.service")
    return "ok",200
    
@app.route('/webhook', methods = ['GET'])
def webhook():
    if request.method == "GET":
        
        id = request.args.get('id')
        status = request.args.get('status') 
        # if status == "MakeCall" :
        #     os.system("docker restart streaming-intercom")
        #     time.sleep(0.6)
        data_json = {"topic":{
                        "name":"touch/smartpole/intercom",
                        "content": [{
                            "id" : id,
                            "status":status
                        }]
                        }
                    }
        print(data_json)  
        json_format = json.dumps(data_json)
        mqtt.publish(topic,json_format)
        return jsonify(data_json),200
    else :
        data_json = {"status":"error"}
        return jsonify(data_json),400

@app.route('/streaming', methods = ['GET'])
def streaming():
    state =""
    if request.method == "GET":
        status = request.args.get('service') 
        if status == "stop":
            state="stop"
            os.system("docker stop streaming-cctv ")
            os.system("docker stop streaming-cctv2")
        if status == "start":
            state="start"
            os.system("docker start streaming-cctv")
            os.system("docker start streaming-cctv2")
        if status == "restart":
            state="restart"
            os.system("docker restart streaming-cctv")
            os.system("docker restart streaming-cctv2")
            os.system("docker restart streaming-intercom")

        data_json = {"service":state,"code":"200"}
        print(data_json)  
        return jsonify(data_json),200
    else :
        data_json = {"status":"error"}
        return jsonify(data_json),400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4500,debug=True)
    # app.run(host="0.0.0.0")








