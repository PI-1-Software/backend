#!/usr/bin/env python

import paho.mqtt.client as paho

def on_message(mosq, obj, msg):
    print(f"{msg.topic:<20} {msg.qos} {msg.payload}")
    
    # Enviar para frontend (websocket)
    
    
    # Enviar para o backend (API)
    
    
    mosq.publish('pong', 'ack', 0)

def on_publish(mosq, obj, mid):
    print("Chegou uma mensagem")
    pass

if __name__ == '__main__':
    client = paho.Client()
    client.on_message = on_message
    client.on_publish = on_publish

    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    client.connect("127.0.0.1", 1883) # host, port respectively

    client.subscribe("car_payload", 0)

    while client.loop() == 0:
        pass