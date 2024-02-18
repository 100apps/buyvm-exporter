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
vi /etc/systemd/system/uvicorn.service
```

```text
[Unit]
Description=uvicorn - python http server
After=network.target

[Service]
Type=simple
# 项目根目录
WorkingDirectory=/data/www/buyvm-exporter/
# uvicorn启动命令
ExecStart=/data/www/buyvm-exporter/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
ExecReload=/data/www/buyvm-exporter/.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000
ExecStop=killall uvicorn

[Install]
WantedBy=multi-user.target
```
重新加载：
```bash
systemctl daemon-reload
systemctl enbale uvicorn
service uvicorn start
# 查看服务状态
service uvicorn status

```

