#flaskblog
本blog系统基于flask框架+mysql数据库

所需环境
------------------------------------------------------
* python2.7
* mysql5.5+

安装
-----------------------------------------------------
* git clone https://github.com/SuZhiBai/flaskblog.git
* cd flaskblog
* pip install -r requirements/dev.txt
*
运行
---------------------------------------------------
* python manage.py db init
* python manage.py db migrate
* python manage.py db upgrade
* python manage.py runserver

