# MQTT2SQL 
# 使用python语言编写的接收MQTT消息并存入SQL数据库中
本项目完全使用python实现，可用于接收远程MQTT消息，按指定类型存入SQL数据库指定的表中。
## 运行前请确保安装并配置 ODBC 驱动程序
注意：在使用SQL server数据库时 'odbcinst.ini' 配置中的 'DSN Name'需要与'DRIVER=<DRIVER_Name>'一致
