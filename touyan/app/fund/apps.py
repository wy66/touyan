from django.apps import AppConfig
from django.apps import AppConfig
from jqdatasdk import *

class FundConfig(AppConfig):
    name = 'app.fund'
    #设置启动一次的时候代码运行 同时要在 __init__中配置
    def ready(self):
        # startup code here
        auth('14613350695', '350695')

