##本程序适用于运行在远程服务器的MQTT客户端和MySQL
#带有JSON解析的版本
#以浮点型在表test1写入temperature, humidity两个数据
#以浮点型在表test写入co
import paho.mqtt.client as mqtt
import pymysql
import json

# MQTT回调函数，处理接收到的消息
def on_message(client, userdata, msg):
    # 在此处处理MQTT消息
    message = msg.payload.decode("utf-8")
    print(f"Received message: {message}")

    # 解析JSON字符串
    #{ "co": "11","tem": "32","hum":"76" }
    try:
        data = json.loads(message)
        co = float(data.get("co", 0))
        tem = float(data.get("tem", 0))
        hum = float(data.get("hum", 0))
        
        # 将消息中tem,hum的值存储到MySQL数据库表Data_A
        insert_data_to_mysql("Data_A", [("tem", tem), ("hum", hum)])
        # 将消息中co的值存储到MySQL数据库表Data_B
        insert_data_to_mysql("Data_B", [("co", co)])

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

# 通用的插入数据到MySQL表的函数
def insert_data_to_mysql(table_name, data):
    # 连接到MySQL数据库
    connection = pymysql.connect(
        host="localhost",  # MySQL服务器地址
        user="your_username",  # 你的MySQL用户名
        password="your_password",  # 你的MySQL密码
        database="your_database"  # 你要使用的数据库
    )

    # 创建游标对象
    cursor = connection.cursor()

    # 构建SQL语句
    columns = ', '.join([column for column, _ in data])
    placeholders = ', '.join(['%s' for _ in data])
    values = [value for _, value in data]

    # 插入数据到指定表中
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, values)
    connection.commit()

    # 关闭数据库连接
    cursor.close()
    connection.close()

# 设置MQTT客户端
client = mqtt.Client()
client.on_message = on_message

# 连接到MQTT代理
client.connect("mqtt_broker_address", 1883, 60)  # 替换为你的MQTT代理地址和端口号
client.subscribe("topic_name")  # 替换为你要订阅的MQTT主题

# 开始循环以接收消息
client.loop_forever()
