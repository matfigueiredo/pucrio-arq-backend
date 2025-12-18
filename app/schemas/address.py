from pydantic import BaseModel
from typing import Optional


class AddressResponse(BaseModel):
    cep: str
    logradouro: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    localidade: Optional[str] = None
    uf: Optional[str] = None
    ibge: Optional[str] = None
    gia: Optional[str] = None
    ddd: Optional[str] = None
    siafi: Optional[str] = None
    erro: Optional[bool] = None

    class Config:
        from_attributes = True

