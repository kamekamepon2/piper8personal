import pika 
import pymsteams
import json
import sys

args = sys.argv


#RabbitMQIP='192.168.80.91'
#RabbitMQIP='localhost'
RabbitMQIP= args[1]
TEAMS_WEB_HOOK_URL = args[2]

def postMSTeams(body,title="default title"):
    myTeamsMessage = pymsteams.connectorcard(TEAMS_WEB_HOOK_URL)
    myTeamsMessage.text(body)
    myTeamsMessage.title(title)
    myTeamsMessage.send()


def callback(ch, method, properties, body):			#callback関数の作成
    D_Value=json.loads(body)
    print("Received:",D_Value)
    if float(D_Value["D_Value"]) < 1: 
        postMSTeams(body=D_Value["D_Value"])
        postMessage("B_COMMAND","trigger")
    ch.basic_ack(delivery_tag = method.delivery_tag)		#ackをする場合はコメントを外す。横から見るだけであればコメントアウトしたまま

def consumer(q_name):
    #pika_param = pika.ConnectionParameters(host=RabbitMQIP) 	#接続パラメータの指定,ポートはデフォルト 5672
    pika_param = pika.ConnectionParameters(host=RabbitMQIP,credentials=pika.PlainCredentials(RabbitMQUser, RabbitMQPassword))
    connection = pika.BlockingConnection(pika_param)		#接続
    channel = connection.channel()					#チャネルの作成
    channel.queue_declare(queue=q_name)				#Queueの作成
    channel.basic_consume(queue=q_name, on_message_callback=callback)	#Queueの受付設定
    #channel.basic_consume(callback,queue=q_name)				#Queueの受付設定.pika ver 0.11.2の場合
    channel.start_consuming()						#受付の開始

def postMessage(q_name,text='Hello World!'):
    #pika_param = pika.ConnectionParameters(host=RabbitMQIP) 	#接続パラメータの指定,ポートはデフォルト 5672
    pika_param = pika.ConnectionParameters(host=RabbitMQIP,credentials=pika.PlainCredentials(RabbitMQUser, RabbitMQPassword))
    connection = pika.BlockingConnection(pika_param)		#接続
    channel = connection.channel()					#チャネルの作成
    channel.queue_declare(queue=q_name)				#Queueの作成
    channel.basic_publish(exchange='', routing_key=q_name, body=text)


consumer("D_MONITOR")
