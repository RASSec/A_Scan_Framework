# 个人安全漏洞管理平台

 Scan_Framework是一款开源的资产管理 、漏洞扫描、todolist的便捷系统，采用了celery+rabbitMQ异步处理队列，
 
 

![](https://i.imgur.com/wbflwiu.jpg)
![](https://i.imgur.com/HXtKczn.png)
![](https://i.imgur.com/sweC238.png)


### Installation

1. 安装django

    	$ sudo pip install django
    	
2. 安装最新版
 
    	$ sudo pip install --upgrade pip && setuptools
3. 其他需要的安全包

 		
 		
### 程序执行流程
	python manage.py celery worker -c 40
	flower --broker=amqp://guest:guest@localhost:5672//
	python manage.py makemigrations
	python manage.py migrate
	flower
	http://192.168.31.131:5555/dashboard
	rabbitmq 监控界面
	http://192.168.31.131:15672
	


__author__ : yds


