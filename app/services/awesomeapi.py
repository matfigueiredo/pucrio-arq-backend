from typing import Optional

import httpx
from app.schemas.address import AddressResponse


class AwesomeAPIService:
    BASE_URL = "https://cep.awesomeapi.com.br"

    @staticmethod
    async def get_address_by_cep(cep: str) -> Optional[AddressResponse]:
        cleaned_cep = cep.replace("-", "").replace(".", "").strip()
        
        if len(cleaned_cep) != 8 or not cleaned_cep.isdigit():
            return None

        url = f"{AwesomeAPIService.BASE_URL}/json/{cleaned_cep}"

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                if "status" in data and data["status"] in [400, 404]:
                    return None

                formatted_cep = f"{cleaned_cep[:5]}-{cleaned_cep[5:]}"
                
                return AddressResponse(
                    cep=formatted_cep,
                    logradouro=data.get("address"),
                    complemento=None,
                    bairro=data.get("district"),
                    localidade=data.get("city"),
                    uf=data.get("state"),
                    ibge=data.get("city_ibge"),
                    gia=None,
                    ddd=data.get("ddd"),
                    siafi=None
                )
        except (httpx.HTTPError, KeyError, ValueError):
            return None
