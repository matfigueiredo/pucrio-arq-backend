import httpx
from typing import Optional
from app.schemas.address import AddressResponse


class ViaCEPService:
    BASE_URL = "https://viacep.com.br/ws"

    @staticmethod
    async def get_address_by_cep(cep: str) -> Optional[AddressResponse]:
        cleaned_cep = cep.replace("-", "").replace(".", "").strip()
        
        if len(cleaned_cep) != 8 or not cleaned_cep.isdigit():
            return None

        url = f"{ViaCEPService.BASE_URL}/{cleaned_cep}/json/"

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                if "erro" in data:
                    return None

                return AddressResponse(**data)
        except (httpx.HTTPError, KeyError, ValueError):
            return None

    @staticmethod
    def format_address(address: AddressResponse) -> str:
        parts = []
        if address.logradouro:
            parts.append(address.logradouro)
        if address.bairro:
            parts.append(address.bairro)
        if address.localidade:
            parts.append(address.localidade)
        if address.uf:
            parts.append(address.uf)
        
        return ", ".join(parts) if parts else ""

