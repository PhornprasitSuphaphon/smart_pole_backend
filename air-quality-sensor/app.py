
import paho.mqtt.client as paho
from pyModbusTCP.client import ModbusClient
import time
import json
import random

broker="touch-iot.touch-ics.com"
port=1883

broker2="171.103.249.186"
port2=1883

client1= paho.Client("control1")
client1.connect(broker,port)  

client2= paho.Client("smartpole1")
client2.connect(broker2,port2)  

while 1 :
    try:
        client = ModbusClient(host="171.103.249.186", port=8006, unit_id=1, auto_open=True)
        regs_1 = client.read_holding_registers(0,15)
        data_json = {"topic":{
                        "name":"touch/smartpole/sensor",
                        "content": [{
                            "id" : "P001",
                            "temperature" : regs_1[1]/10,
                            "humidity" : regs_1[0]/10,
                            "pm10" : regs_1[10],
                            "pm25" : regs_1[11]
                            }]
                        }
                    }
        json_format = json.dumps(data_json)
        ret= client1.publish("touch/smartpole/sensor",json_format)

        client2.publish("touch/smartpole/sensor/temp",regs_1[1]/10)
        client2.publish("touch/smartpole/sensor/humi",regs_1[0]/10)
        client2.publish("touch/smartpole/sensor/pm10",regs_1[10])
        client2.publish("touch/smartpole/sensor/pm25",regs_1[11])
        print(json_format)
        time.sleep(2)
    except:
        print("not conect modbus")
    time.sleep(2)

# print(regs_1)
# regs_temp = random.randint(230, 250)
# regs_hu = random.randint(300, 306)
# regs_pm10 = random.randint(15, 18)
# regs_pm25 = random.randint(6, 11)
# print(type(regs_pm25))