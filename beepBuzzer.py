import pika 
import json
import RPi.GPIO as GPIO
import time
import sys

args = sys.argv

#RabbitMQIP='192.168.80.91'
RabbitMQIP=args[1]

def beepBuzzer():
    BZRPin = 11
    GPIO.setmode(GPIO.BOARD) # Numbers pins by physical location
    GPIO.setup(BZRPin, GPIO.OUT) # Set pin mode as output
    GPIO.output(BZRPin, GPIO.LOW)
    p = GPIO.PWM(BZRPin, 50) # init frequency: 50HZ
    p.start(50) # Duty cycle: 50%
    counter=0
    try:
        while counter<1:
            for f in range(220, 880, 10):
                p.ChangeFrequency(f)
                time.sleep(0.01)
            for f in range(0, 4):
                p.ChangeFrequency(923.32)
                time.sleep(0.2)
                p.ChangeFrequency(880)
                time.sleep(0.2)
            counter+=1
    except:
        p.stop()
        GPIO.cleanup()
        print('-- cleanup GPIO/PWM! --')


def callback(ch, method, properties, body):			#callback関数の作成
    beepBuzzer()
    ch.basic_ack(delivery_tag = method.delivery_tag)		#ackをする場合はコメントを外す。横から見るだけであればコメントアウトしたまま

def consumer(q_name):
    pika_param = pika.ConnectionParameters(host=RabbitMQIP) 	#接続パラメータの指定,ポートはデフォルト 5672
    connection = pika.BlockingConnection(pika_param)		#接続
    channel = connection.channel()					#チャネルの作成
    channel.queue_declare(queue=q_name)				#Queueの作成
    channel.basic_consume(queue=q_name, on_message_callback=callback)	#Queueの受付設定
    #channel.basic_consume(callback,queue=q_name)				#Queueの受付設定.pika ver 0.11.2の場合
    channel.start_consuming()						#受付の開始

def postMessage(q_name,text='Hello World!'):
    pika_param = pika.ConnectionParameters(host=RabbitMQIP) 	#接続パラメータの指定,ポートはデフォルト 5672
    connection = pika.BlockingConnection(pika_param)		#接続
    channel = connection.channel()					#チャネルの作成
    channel.queue_declare(queue=q_name)				#Queueの作成
    channel.basic_publish(exchange='', routing_key=q_name, body=text)


consumer("B_COMMAND")
