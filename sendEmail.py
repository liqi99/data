import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
 
from readTxt import readTxt
from getTime import getToday,getNday
# 发件人信息
sender_email = "416934659@qq.com"
sender_password = "joedwwiemavtbidj"
 
# 收件人信息
recipient_email = "416934659@qq.com"
 
# 构造邮件对象
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = "{yesterday}想法".format(yesterday=getNday(0))
 
# 添加正文
body = readTxt('./{dir}/{aday}'.format(dir='./buysell',aday=getNday(0)))
msg.attach(MIMEText(body, 'plain'))
 
# 添加附件
#with open("example.pdf", "rb") as attachment:
#    part = MIMEApplication(attachment.read(), _subtype='pdf')
#    part.add_header('Content-Disposition', 'attachment', filename="example.pdf")
#    msg.attach(part)
 
# 发送邮件
with smtplib.SMTP_SSL('smtp.qq.com', 465) as smtp:
    smtp.login(sender_email, sender_password)
    smtp.sendmail(sender_email, recipient_email, msg.as_string())
