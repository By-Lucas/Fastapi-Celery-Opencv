from celery import Celery

from fastapi import FastAPI

from api.v1.api import api_router

from controllers.configs import settings


app = FastAPI(title='TK Global Technology', description='Api para registro de pontos',version='0.1')
celery_app = Celery("my_app", broker="redis://localhost:6379/0")



app.include_router(api_router, prefix=settings.API_V1_STR)


# Rodar celery - celery -A celery_app beat  --loglevel=info
# Rodar celery terefas - celery -A celery_app  worker --loglevel=info

if __name__ == '__main__':
    import uvicorn
    import subprocess
    
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
    #subprocess.Popen(["celery", "-A", "main", "worker", "--loglevel=info"])
    
