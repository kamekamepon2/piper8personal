#! /usr/bin/python3

import RPi.GPIO as GPIO
import time
import pika
import json
#RabbitMQIP='192.168.80.91'
RabbitMQIP='localhost'

Trigger = 16
Echo = 18

def postMessage(q_name,text='Hello World!'):
    pika_param = pika.ConnectionParameters(host=RabbitMQIP) 	#接続パラメータの指定,ポートはデフォルト 5672
    connection = pika.BlockingConnection(pika_param)		#接続
    channel = connection.channel()					#チャネルの作成
    channel.queue_declare(queue=q_name)				#Queueの作成
    channel.basic_publish(exchange='', routing_key=q_name, body=text)

def checkdist():
    GPIO.output(Trigger, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(Trigger, GPIO.LOW)
    while not GPIO.input(Echo):
        pass
    t1 = time.time()
    while GPIO.input(Echo):
        pass
    t2 = time.time()
    return (t2-t1)*340/2

GPIO.setmode(GPIO.BOARD)
GPIO.setup(Trigger,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(Echo,GPIO.IN)

try:
    while True:
        d = checkdist()
        df = "%0.2f" %d
        print ('Distance: %s m' %df)
        jsonData={"D_Value": df}
        #print(json.dumps(jsonData))
        #print(json.loads(json.dumps(jsonData)))
        postMessage("D_MONITOR",json.dumps(jsonData))
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
    print ('GPIO cleeanup and end!')
