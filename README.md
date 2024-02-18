# buyvm-exporter
buyvm prometheus exporter

## 初始化 Python 环境
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install uvicorn beautifulsoup4 fastapi requests
```

## 配置开机启动
```bash
vi /etc/systemd/system/gunicorn.service
```

```text
[Unit]
Description=gunicorn - python http server
After=network.target

[Service]
Type=forking
PIDFile=/var/run/gunicorn.pid
# 项目根目录
WorkingDirectory=/data/www/buyvm-exporter/
# gunicorn启动命令
ExecStart=/data/www/buyvm-exporter/.venv/python /data/www/buyvm-exporter/.venv/bin/gunicorn main:app -D --pid /var/run/gunicorn.pid --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8080
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID

[Install]
WantedBy=multi-user.target
```
重新加载：
```bash
systemctl daemon-reload
systemctl enbale gunicorn
service gunicorn start
# 查看服务状态
service gunicorn status

```

