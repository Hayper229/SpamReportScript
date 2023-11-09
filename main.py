#!/bin/python3
import os
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import datetime


def send_email(sender_email, sender_password, recipient_email, subject, message_text):
    try:
        # print("connect...")
        server = smtplib.SMTP_SSL('smtp.rambler.ru', 465)
        # print("start TLS")
        # server.starttls()
        # print("login...")
        server.login(sender_email, sender_password)
        # print("login success")
        # Создайте объект письма
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        body = message_text
        message.attach(MIMEText(body, 'plain'))

        server.send_message(message)
        now = datetime.datetime.now()
        print(now.strftime("%H:%M:%S"), end=' ')
        print(f"Письмо от {sender_email} успешно отправлено на {recipient_email}.")

        server.quit()
    except Exception as e:
        print(f"Ошибка при отправке письма: {str(e)}")

mes_text = ''
mes_subject = ''
senders = []
recipients = []
with open('emails.txt', 'r') as f:
    for line in f:
        try:
            senders.append((line.strip().split(';')[0], line.strip().split(';')[1]))
        except:
            pass

with open('recipients.txt', 'r') as f:
    for i in f:
        if '@' in i and '.' in i:
            recipients.append(i.strip())

with open('text.txt', 'r') as f:
    mes_text = f.read()
with open('sublect.txt', 'r') as f:
    mes_subject = f.read()
print(f'Загруженно {len(senders)} почт\n')
print(f'Загруженно {len(recipients)} получателей')

print(f'Заголовок:\n{mes_subject}\n\nТекст:\n{mes_text}')


if len(senders) > 0:
    if mes_text and mes_subject:
        for sender_email, sender_password in senders:
            for recipient_email in recipients:
                subject = mes_subject
                message_text = mes_text

                send_email(sender_email, sender_password, recipient_email, subject, message_text)

    else:
        print('Не задан текст и/или заголовок письма!\nОткройте файлы text.txt и subject.txt и заполните их')
