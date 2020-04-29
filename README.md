#### Celery Worker使用说明


###### 运行环境

- Linux
- Python: 3.6.x
- Sqlite: SQLite 3.8.3 or later is required


###### 依次执行以下命令初始化环境

- git clone https://github.com/tinylambda/djangogo.git -b use-celery-demo
- cd djangogo
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt


###### 启动worker

- celery -A djangogo -P prefork -c 2


###### 在另一个命令行中启动Django Shell，调用异步任务

- python manage.py shell

