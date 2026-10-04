"""Locust 性能测试脚本。

模拟用户对平台的关键页面与接口进行并发访问，统计响应时间、吞吐量与错误率。

运行方式：
1. 启动服务：py -3.11 manage.py runserver 8080
2. 无界面压测（-u 用户数，-r 每秒孵化数，-t 持续时间）：
   py -3.11 -m locust -f locustfile.py --headless -u 100 -r 10 -t 1m --host http://127.0.0.1:8080
3. 或在浏览器打开 http://127.0.0.1:8089 使用 Locust Web 界面
"""
from locust import HttpUser, between, task


class MarketUser(HttpUser):
    """模拟平台用户，@task 权重越大访问越频繁。"""

    wait_time = between(1, 3)

    @task(5)
    def home_page(self):
        self.client.get('/')

    @task(3)
    def goods_list_page(self):
        self.client.get('/goods/')

    @task(2)
    def api_goods_list(self):
        self.client.get('/api/goods/')

    @task(1)
    def login_page(self):
        self.client.get('/user/login/')
