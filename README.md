# Tech4Bike Backend API

Backend API desenvolvida com FastAPI para o sistema de gestão de manutenção de bicicletas Tech4Bike.

## Descrição do Projeto

API REST que fornece endpoints para gerenciamento de bicicletas e seus históricos de manutenção. O sistema permite cadastrar bicicletas, registrar serviços de manutenção realizados e buscar endereços de oficinas através da integração com a API ViaCEP.

## Tecnologias

- **Python 3.12**
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados relacional
- **Pydantic** - Validação de dados
- **httpx** - Cliente HTTP assíncrono para integração com ViaCEP
- **UV** - Gerenciador de pacotes Python

## Estrutura do Projeto

```
tech4bike-backend/
├── app/
│   ├── __init__.py
│   ├── database.py          # Configuração do banco de dados
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── bike.py
│   │   └── maintenance.py
│   ├── schemas/             # Schemas Pydantic
│   │   ├── bike.py
│   │   ├── maintenance.py
│   │   └── address.py
│   ├── routes/              # Rotas da API
│   │   ├── bikes.py
│   │   ├── maintenances.py
│   │   └── address.py
│   └── services/            # Serviços externos
│       └── viacep.py
├── main.py                  # Aplicação FastAPI
├── Dockerfile
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Instalação

### Pré-requisitos

- Python 3.12 ou superior
- UV (gerenciador de pacotes Python)
- Docker (opcional, para execução via container)

### Instalação Local

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd tech4bike-backend
```

2. Instale o UV (se ainda não tiver):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Crie e ative o ambiente virtual com UV:
```bash
uv venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

4. Instale as dependências:
```bash
uv pip install -r requirements.txt
```

## Execução

### Execução Local

1. Inicie o servidor:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Acesse a documentação interativa:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Execução com Docker

O projeto utiliza **Docker Compose** para facilitar a execução. O `docker-compose` utiliza o `Dockerfile` existente para construir a imagem com todas as definições necessárias (portas, volumes, variáveis de ambiente).

1. Inicie o servidor:
```bash
docker-compose up -d
```

2. Verifique os logs (opcional):
```bash
docker-compose logs -f
```

3. Para parar a execução:
```bash
docker-compose down
```

**Sobre o Dockerfile:**

O Dockerfile utiliza **multistage building** para otimizar o tamanho da imagem final:
- **Stage 1 (builder):** Instala UV e todas as dependências
- **Stage 2 (runtime):** Apenas copia as dependências Python instaladas, resultando em uma imagem mais leve

A imagem final usa `python:3.12-slim` (base leve) e não inclui o UV, apenas os pacotes Python necessários.

## Endpoints da API

### Bicicletas (`/api/v1/bikes`)

- `GET /api/v1/bikes` - Lista todas as bicicletas
- `GET /api/v1/bikes/{bike_id}` - Obtém uma bicicleta específica
- `POST /api/v1/bikes` - Cria uma nova bicicleta
- `PUT /api/v1/bikes/{bike_id}` - Atualiza uma bicicleta
- `DELETE /api/v1/bikes/{bike_id}` - Remove uma bicicleta

### Manutenções (`/api/v1/maintenances`)

- `GET /api/v1/maintenances` - Lista todas as manutenções
- `GET /api/v1/maintenances/{maintenance_id}` - Obtém uma manutenção específica
- `GET /api/v1/maintenances/bike/{bike_id}` - Lista manutenções de uma bicicleta
- `POST /api/v1/maintenances` - Cria um novo registro de manutenção
- `PUT /api/v1/maintenances/{maintenance_id}` - Atualiza uma manutenção
- `DELETE /api/v1/maintenances/{maintenance_id}` - Remove uma manutenção

### Endereços (`/api/v1/address`)

- `GET /api/v1/address/{cep}` - Busca endereço por CEP (integração ViaCEP)

## API Externa - ViaCEP

### Informações da API Externa

**ViaCEP** é uma API pública e gratuita para consulta de CEPs brasileiros.

- **URL Base:** https://viacep.com.br/ws/{cep}/json/
- **Licença:** Uso livre e gratuito
- **Cadastro:** Não é necessário cadastro
- **Documentação:** https://viacep.com.br/

### Rotas Utilizadas

- `GET /ws/{cep}/json/` - Consulta endereço completo a partir do CEP

### Exemplo de Uso

```bash
curl http://localhost:8000/api/v1/address/01310100
```

**Resposta:**
```json
{
  "cep": "01310-100",
  "logradouro": "Avenida Paulista",
  "complemento": "",
  "bairro": "Bela Vista",
  "localidade": "São Paulo",
  "uf": "SP",
  "ibge": "3550308",
  "gia": "1004",
  "ddd": "11",
  "siafi": "7107"
}
```

## Diagrama de Arquitetura

```
┌─────────────┐
│   Frontend  │
│ (Next.js)   │
└──────┬──────┘
       │ HTTP REST
       │
┌──────▼──────────────────┐
│   Backend API (FastAPI) │
│                         │
│  ┌──────────────────┐   │
│  │  Routes          │   │
│  │  - Bikes         │   │
│  │  - Maintenances  │   │
│  │  - Address       │   │
│  └────────┬─────────┘   │
│           │              │
│  ┌────────▼─────────┐   │
│  │  Services        │   │
│  │  - ViaCEP        │   │
│  └────────┬─────────┘   │
│           │              │
│  ┌────────▼─────────┐   │
│  │  Models          │   │
│  │  - Bike          │   │
│  │  - Maintenance   │   │
│  └────────┬─────────┘   │
│           │              │
│  ┌────────▼─────────┐   │
│  │  SQLite Database │   │
│  └──────────────────┘   │
└─────────────────────────┘
       │
       │ HTTP
       │
┌──────▼──────┐
│   ViaCEP    │
│   (Externa) │
└─────────────┘
```

## Modelos de Dados

### Bike
- `id` (Integer, PK)
- `brand` (String) - Marca da bicicleta
- `model` (String) - Modelo da bicicleta
- `year` (Integer, opcional) - Ano de fabricação
- `color` (String, opcional) - Cor
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Maintenance
- `id` (Integer, PK)
- `bike_id` (Integer, FK) - Referência à bicicleta
- `service_type` (String) - Tipo de serviço
- `description` (String, opcional) - Descrição do serviço
- `cost` (Float, opcional) - Custo do serviço
- `workshop_name` (String, opcional) - Nome da oficina
- `workshop_cep` (String, opcional) - CEP da oficina
- `workshop_address` (String, opcional) - Endereço completo da oficina
- `service_date` (DateTime) - Data do serviço
- `created_at` (DateTime)
- `updated_at` (DateTime)

## Desenvolvimento

### Estrutura de Pastas

- `app/models/` - Modelos do banco de dados (SQLAlchemy)
- `app/schemas/` - Schemas de validação (Pydantic)
- `app/routes/` - Endpoints da API
- `app/services/` - Lógica de negócio e integrações externas
- `app/database.py` - Configuração e sessão do banco de dados

### Convenções

- Nomes de arquivos e variáveis: `snake_case`
- Classes: `PascalCase`
- Type hints obrigatórios
- Docstrings apenas quando necessário

## Licença

Este projeto é parte de um MVP acadêmico.

