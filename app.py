import pika 
import pymsteams
import json

TEAMS_WEB_HOOK_URL = "https://dell.webhook.office.com/webhookb2/e0a540f3-e6bb-4273-83f9-e82877290ce8@945c199a-83a2-4e80-9f8c-5a91be5752dd/IncomingWebhook/8ab059ee2edd43a49cf1a684e145e888/767f097b-3df4-4cce-8ff8-b94533a5e92b"
#RabbitMQIP='192.168.80.91'
RabbitMQIP='localhost'

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


consumer("D_MONITOR")
