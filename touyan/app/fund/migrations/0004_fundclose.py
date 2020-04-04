# Generated by Django 3.0.4 on 2020-04-02 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0003_jqcodeinfo_jqcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundClose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30)),
                ('sdate', models.DateField()),
                ('net_value', models.FloatField()),
                ('sum_value', models.FloatField()),
            ],
            options={
                'unique_together': {('code', 'sdate')},
            },
        ),
    ]
