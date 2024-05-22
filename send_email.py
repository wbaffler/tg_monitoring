import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class SendEmail(object):
    
    
    def __init__(self, smtp_server, smtp_username, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.port = 465
    
    
    def send(self, sender, receiver, filename):
        # Создание сообщения
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver 
        msg['Subject'] = 'Отчет по мониторингу Telegram-канала'

        # Текст письма
        body = 'Ознакомтесь с новым отчетом во вложении.'
        msg.attach(MIMEText(body, 'plain'))

        attachment = open(filename, 'rb')

        # Создание объекта MIMEBase
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # Прикрепляем файл к сообщению
        msg.attach(part)

        # Установка соединения с SMTP сервером
        server = smtplib.SMTP_SSL(self.smtp_server, self.port)
        server.login(self.smtp_username, self.smtp_password)
        # Отправка письма
        text = msg.as_string()
        server.sendmail(self.smtp_username, 'agiev29@gmail.com', text)

        # Закрытие соединения
        server.quit()