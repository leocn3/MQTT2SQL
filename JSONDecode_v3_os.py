#0.本程序适用于运行在远程服务器的MQTT客户端和SQL server
#1.带有JSON解析的版本
#2.请确保已安装并配置 ODBC 驱动程序
#3.可以使用msodbcsql或者 FreeTDS 作为 ODBC 驱动程序
#4.以浮点型在表test1写入temperature, humidity两个数据
#5.以浮点型在表test写入co

import paho.mqtt.client as mqtt
import pyodbc
import json

def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe('testtopic/#')#订阅主题testtopic/#

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))  # 打印接收到的消息内容

    try:
        # 解析 JSON 字符串
        #{ "co": "11","tem": "32","hum":"76" }
        data = json.loads(msg.payload.decode('utf-8'))

        # 提取所需字段并转换为浮点数
        temperature = float(data.get('tem', 0.0))
        humidity = float(data.get('hum', 0.0))

        # 提取 CO 字段并转换为浮点数
        co = float(data.get('co', 0.0))

        # 插入'temperature', 'humidity'数据到数据库'MQTT' 表'Data_A'
        query_tem_hum = "INSERT INTO MQTT.dbo.Data_A (temperature, humidity) VALUES (?, ?)"
        cursor.execute(query_tem_hum, (temperature, humidity))
        conn.commit()

        # 插入 CO 数据到 'Data_B' 表
        query_co = "INSERT INTO MQTT.dbo.Data_B (co) VALUES (?)"
        cursor.execute(query_co, (co,))
        conn.commit()

    except json.JSONDecodeError as e:
        print(f"JSON解析错误：{e}")

client = mqtt.Client()

# 指定回调函数
client.on_connect = on_connect
client.on_message = on_message

# 建立MQTT连接
client.connect('<Your_database_address>', 1883, 60)

# 建立与数据库的连接
#"DRIVER={ms-sql};SERVER=127.0.0.1;PORT=1433;DATABASE=Data;UID=sa;PWD=public;"
#DRIVER={ms-sql}这里要和odbcinst.ini 配置中的 DSN Name一致
conn = pyodbc.connect(
    "DRIVER=<DRIVER_Name>;SERVER=<Your_database_address>;PORT=1433;DATABASE=<Database_Name>;UID=<Account_Name>;PWD=<Password>;"
)
cursor = conn.cursor()

client.loop_forever()
