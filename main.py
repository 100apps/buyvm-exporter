from fastapi import FastAPI
import spider
import time
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.get("/metrics", response_class=PlainTextResponse)
def read_root():
    line = """
# HELP buy_vm_stock 监控 buyvm 虚拟机或者磁盘的库存，方便购买。
# TYPE buy_vm_stock gauge
"""
    data = spider.get_results()
    for row in data:
        line += "buy_vm_stock{{zone=\"{}\",package_name=\"{}\",price={}}} {} {}\n".format(row["zone"],
                                                                                              row["package_name"],
                                                                                              row["price"],
                                                                                              row["stock"],
                                                                                              int(round(
                                                                                                  time.time() * 1000)))
    return line
