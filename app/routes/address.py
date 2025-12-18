from fastapi import APIRouter, HTTPException
from app.schemas.address import AddressResponse
from app.services.viacep import ViaCEPService

router = APIRouter()


@router.get("/{cep}", response_model=AddressResponse)
async def get_address_by_cep(cep: str):
    address = await ViaCEPService.get_address_by_cep(cep)
    
    if not address:
        raise HTTPException(
            status_code=404, 
            detail="CEP not found or invalid. Please provide a valid 8-digit CEP."
        )
    
    return address

