import os
import cv2
from qrcode import make
from typing import List
from pyzbar import pyzbar
from datetime import datetime

from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.model_user import User
from controllers.depends import get_db
from schemas.schema_user import UserSchema

from celery_app import send_email
from celery.schedules import crontab


router = APIRouter()

@router.post("/schedule-message/")
async def schedule_message():#to: str, subject: str, body: str, scheduled_time: str
    
    to = ["lukasmulekezika2@gmail.com","monica.liborio1@gmail.com"]
    subject = "Lucas"
    body = "OI Lucas, ta bem?"
    scheduled_time = "2023-01-27 15:58:00"
    
    scheduled_time = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")
    countdown = (scheduled_time - datetime.now()).total_seconds()
    send_email.apply_async(args=[to, subject, body], countdown=countdown)
    return {"message": "Mensagem agendada com sucesso!"}


@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user_route(user: UserSchema, db: AsyncSession = Depends(get_db)):
    
    async with db as session:
        try:
            new_user:User = User(**user.dict())
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            
            if new_user:
                return new_user
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao cadastrar o usuário")
            
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Já tem um usuário cadastrado com o E-mail ou CPF/CNPJ')
        
@router.get("/qrcode/{user_id}")
async def generate_qrcode(user_id: str, db: AsyncSession = Depends(get_db)):
    user = next((user for user in db if user["code"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # gerar QRCode para o usuário
    # ...
    return {"msg": "QRCode gerado"}

@router.get("/scan")
async def scan_qr():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        decoded_objs = pyzbar.decode(frame)
        for obj in decoded_objs:
            user = next((user for user in User if user['code'] == obj.data.decode("utf-8")), None)
            if user:
                cap.release()
                cv2.destroyAllWindows()
                return {"user": user}
        cv2.imshow("Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    