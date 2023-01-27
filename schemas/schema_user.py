from pydantic import EmailStr
from pydantic import BaseModel
from pydantic import validator


class UserSchema(BaseModel):
    #code: UUID
    name: str
    email: EmailStr
    phone: str
    password: str
    cpf_cnpj: str
    
    @validator("name")
    def validate_name(cls, value):
        if not value:
            raise ValueError("Name is required.")
        if len(value.split()) < 2:
            raise ValueError("O nome do usuário deve conter o sobrenome tambem.")
        common_abbreviations = ["da", "dos", "de", "e", "a", "das"]
        for abbreviation in common_abbreviations:
            value = value.replace(f" {abbreviation} ", " ")
        return value
    
    @validator("phone")
    def phone_number_validator(cls, value):
        if not value.startswith("+"):
            raise ValueError("O número de telefone deve começar com um sinal de mais (+)")
        return value
    
    @validator("cpf_cnpj")
    def cpf_cnpj_validator(cls, value):
        if len(value) < 11 or len(value) > 14:
            raise ValueError("Deve ter 11 caracteres para CPF e 14 caracteres para CNPJ.")
        return value
    
    class Config:
        orm_mode = True