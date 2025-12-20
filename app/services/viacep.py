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
        print(f"Requesting ViaCEP URL: {url}")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                headers = {"User-Agent": "Tech4Bike/1.0"}
                response = await client.get(url, headers=headers)
                print(f"ViaCEP Response Status: {response.status_code}")
                
                response.raise_for_status()
                data = response.json()

                if "erro" in data:
                    print(f"ViaCEP returned error: {data}")
                    return None

                return AddressResponse(**data)
        except Exception as e:
            print(f"Error requesting ViaCEP: {e}")
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

