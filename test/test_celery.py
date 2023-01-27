import smtplib
import datetime
from typing import List

from celery import Celery
from celery import shared_task
from celery.schedules import crontab

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

REDIS_HOST = "redis://localhost:6379/0"

app = Celery('tasks', 
            backend=REDIS_HOST,
            broker=REDIS_HOST)

app.conf.timezone = 'UTC'
#app.autodiscover_tasks()

@app.task
def send_email(to: str, subject: str, message: str):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("tekertudo@gmail.com", "lbrkulimopjljajs")
        msg = f"Subject: {subject}\n\n{message}"
        server.sendmail("tekertudo@gmail.com", to, msg)
        server.quit()
        print('Email enviado com sucesso!')
    except Exception as e:
        print("O erro é =", e)



app.conf.beat_schedule = {
    'send_email': {
        'task': 'tasks.send_email',
        'schedule': crontab(minute='*/1'),  # Executar a cada 1 minuto
        'args': ("lukasmulekezika2@gmail.com", "Testando Celery", "Este foi apenas um email de teste do Celery"),
    },
}


if __name__ == '__main__':
    app.start()