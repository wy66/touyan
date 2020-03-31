from django.db import models

# Create your models here.

#个人网格添加标的
class OuterFundWgConf(models.Model):
    code = models.CharField(max_length=30,null=False,primary_key=True)
    sdate = models.DateField(null=False)
    insert_dt = models.DateTimeField(auto_now_add = True)
    update_dt = models.DateTimeField(auto_now=True)

