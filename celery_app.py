import os
import smtplib
from typing import List
from datetime import datetime
from celery import Celery
from celery.schedules import crontab

celery_app = Celery("celery_app", broker="redis://127.0.0.1:6379/0")

celery_app.config_from_object("celery_app")
celery_app.autodiscover_tasks(['celery_app'])

# Configuração do Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True
    )


@celery_app.task
def send_email(to: List[str], subject: str, message: str):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("tekertudo@gmail.com", "lbrkulimopjljajs")
    messages = f"Subject: {subject}\n\n{message}"
    server.sendmail("tekertudo@gmail.com", to, messages)
    server.quit()


# Agendar a tarefa para ser executada a cada minuto
celery_app.conf.beat_schedule = {
    'send_email': {
        'task': 'celery_app.send_email',
        'schedule': crontab(minute='*/1'),
        'args': ("destinatario@email.com", "Assunto do email", "Conteudo do email"),
    },
}

# Rodar tarefas em aberto: celery -A celery_app beat --loglevel=info
# Rodar o celery: celery -A celery_app worker --loglevel=info

