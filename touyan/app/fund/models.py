from django.db import models

# Create your models here.

#个人网格添加标的
class OuterFundWgConf(models.Model):
    code = models.CharField(max_length=30,null=False,primary_key=True)
    sdate = models.DateField(null=False)
    insert_dt = models.DateTimeField(auto_now_add = True)
    update_dt = models.DateTimeField(auto_now=True)

class jjCode(models.Model):
    jjcode = models.CharField(max_length=20,null=False,primary_key=True)
    fname = models.CharField(max_length=200, null=False)
    sname = models.CharField(max_length=100, null=False)
    stype = models.CharField(max_length=50, null=False)
    sday = models.DateField()
    gm = models.FloatField()
    insert_dt = models.DateTimeField(auto_now_add = True)
    update_dt = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'ttjjcode'
        unique_together = (("jjcode",),)

class jjNet(models.Model):
    datadate = models.DateField()
    jjcode = models.CharField(max_length=20,null=False,primary_key=True)
    net_value = models.FloatField()
    sum_value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ttjjnet'
        unique_together = (("datadate","jjcode"),)

class jjTop10Stock(models.Model):
    datadate = models.DateField()
    jjcode = models.CharField(max_length=20,null=False)
    scode = models.CharField(max_length=30,null=False)
    sname = models.CharField(max_length=100,null=False)
    pct = models.FloatField()
    num = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ttjjtop10stock'
        unique_together = (("datadate","jjcode",'scode'),)

