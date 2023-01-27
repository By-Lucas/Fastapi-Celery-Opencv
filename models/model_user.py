from uuid import uuid4

from sqlalchemy import Column, String, Integer

from controllers.configs import settings


class User(settings.DBBaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    code = Column(String, primary_key=True, default=str(uuid4()))
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    phone = Column(String, index=True)
    password = Column(String)
    cpf_cnpj = Column(String, index=True, unique=True)

    def __init__(self, name, email, phone, password, cpf_cnpj):
        self.code = str(uuid4())
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.cpf_cnpj = cpf_cnpj

