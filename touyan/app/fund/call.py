# @Time    : 2020/4/15 11:13
# @Author  : wangyang
# @File    : call.py
# @Software: PyCharm

# @Time    : 2020/4/14 9:50
# @Author  : wangyang
# @File    : email.py
# @Software: 发送邮件

import datetime
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(title,info):
    from_addr = 'bi_system@kffund.cn'
    password = 'bi1234'
    to_addr = ['2465876959@qq.com']
    to_addr_str = ";".join(to_addr)

    smtp_server = 'smtp.exmail.qq.com'

    curdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 邮件对象:
    msg = MIMEText(info, 'plain', 'utf-8')
    msg['From'] = 'bi_system@kffund.cn'
    msg['To'] = to_addr_str
    msg['Subject'] = Header(title, 'utf-8')


    # 发送邮件
    server = smtplib.SMTP(smtp_server, 25, timeout=30)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

if __name__ == '__main__':
    send_email('adfasfsa')
