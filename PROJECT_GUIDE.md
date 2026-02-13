# Guia Completo do Projeto: API de Controle de Vacinação de Pets

Este guia explica detalhadamente a estrutura do projeto, o propósito de cada pasta e arquivo, como executar e configurar a aplicação, conectar ao banco de dados, o funcionamento dos inserts automáticos (seed data) e como a autenticação JWT (SimpleJWT) funciona.

## 1. Visão Geral do Projeto

Este é um projeto Django REST Framework para gerenciar o histórico de vacinação de pets em uma clínica veterinária. Inclui usuários (tutores), pets, vacinas e registros de vacinação, com autenticação JWT.

**Stack Tecnológica:**
- Python 3.11+
- Django 5.0.6
- Django REST Framework 3.15.1
- Autenticação: SimpleJWT
- Banco: SQLite (padrão) ou PostgreSQL (via Docker)
- Outros: django-environ, django-filter

## 2. Estrutura do Projeto

### Arquivos na Raiz

- **.gitignore**: Define arquivos/pastas ignorados pelo Git (ex.: .env, __pycache__, etc.).
- **docker-compose.yml**: Configuração para orquestrar containers Docker (serviços web e db).
- **Dockerfile**: Instruções para construir a imagem Docker da aplicação.
- **manage.py**: Script de gerenciamento do Django (migrações, servidor, comandos customizados).
- **README copy.md** e **README.md**: Documentação do projeto (instruções básicas).
- **requirements.txt**: Lista de dependências Python a serem instaladas via pip.
- **.env** e **.env.example**: Arquivos de variáveis de ambiente (não versionados no Git).

### Pastas Principais

- **config/**: Configurações centrais do Django.
  - **__init__.py**: Torna a pasta um módulo Python.
  - **apps.py**: Configuração da app principal.
  - **asgi.py**: Configuração ASGI para servidores assíncronos.
  - **exceptions.py**: Handler customizado para exceções da API (respostas padronizadas).
  - **settings.py**: Configurações globais (banco, auth, REST Framework, etc.).
  - **urls.py**: URLs principais da aplicação.
  - **wsgi.py**: Configuração WSGI para servidores web.
  - **management/commands/seed_data.py**: Comando customizado para popular o banco com dados iniciais.

- **pets/**: App para gerenciar pets.
  - **models.py**: Modelo Pet (relacionado ao usuário como owner).
  - **views.py**: ViewSets para CRUD de pets.
  - **serializers.py**: Serializers para validação e representação de dados.
  - **permissions.py**: Permissões customizadas (ex.: IsPetOwner).
  - **admin.py**: Registro no admin do Django.
  - **apps.py**: Configuração da app.

- **users/**: App para usuários (tutores).
  - **models.py**: Modelo User customizado (extensão do AbstractUser).
  - **views.py**: ViewSets para usuários.
  - **serializers.py**: Serializers para registro/login.
  - **permissions.py**: Permissões (ex.: IsSelfOrAdmin).
  - **admin.py**: Registro no admin.
  - **apps.py**: Configuração da app.

- **vaccines/**: App para vacinas.
  - **models.py**: Modelo Vaccine (com periodicity_days).
  - **views.py**: ViewSets para CRUD.
  - **serializers.py**: Serializers.
  - **admin.py**: Registro no admin.
  - **apps.py**: Configuração.

- **vaccinations/**: App para registros de vacinação.
  - **models.py**: Modelo Vaccination (relaciona Pet e Vaccine).
  - **views.py**: ViewSets para CRUD.
  - **serializers.py**: Serializers.
  - **filters.py**: Filtros customizados (ex.: por pet, vaccine, upcoming).
  - **permissions.py**: Permissões (ex.: IsVaccinationPetOwner).
  - **admin.py**: Registro no admin.
  - **apps.py**: Configuração.

## 3. Como Executar e Configurar

### Pré-requisitos
- Python 3.11+ instalado.
- Git para clonar o repositório.
- (Opcional) Docker e docker-compose para execução containerizada.

### Opção 1: Sem Docker (Desenvolvimento Local)

1. **Clone o repositório**:
   ```
   git clone <url-do-repositorio>
   cd pet-vaccination
   ```

2. **Crie e ative um ambiente virtual**:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/macOS
   ```

3. **Instale as dependências**:
   ```
   pip install -r requirements.txt
   ```

4. **Configure o .env**:
   - Copie `.env.example` para `.env`:
     ```
     cp .env.example .env
     ```
   - Edite `.env` com valores como `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=True`, etc. (padrão usa SQLite).

5. **Execute migrações**:
   ```
   python manage.py migrate
   ```

6. **Popule dados iniciais (opcional)**:
   ```
   python manage.py seed_data
   ```

7. **Crie superusuário (opcional)**:
   ```
   python manage.py createsuperuser
   ```

8. **Inicie o servidor**:
   ```
   python manage.py runserver
   ```
   - API em: http://127.0.0.1:8000/

### Opção 2: Com Docker

1. **Configure .env** (copie de .env.example e ajuste para PostgreSQL se necessário).

2. **Construa e inicie**:
   ```
   docker-compose up --build
   ```

3. **Migrações e seed (dentro do container)**:
   ```
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py seed_data
   ```
   - API em: http://127.0.0.1:8000/

## 4. Conexão ao Banco de Dados

- **Configuração**: Definida em `config/settings.py` via `django-environ`.
- **Variáveis no .env**:
  - `DJANGO_DB_ENGINE`: django.db.backends.postgresql
  - `DJANGO_DB_NAME`: Nome do banco de dados.
  - `DJANGO_DB_USER`, `DJANGO_DB_PASSWORD`, `DJANGO_DB_HOST`, `DJANGO_DB_PORT`: Para PostgreSQL.
- **Padrão**: SQLite (arquivo local `db.sqlite3`).
- **Com Docker**: PostgreSQL via container `db`.
- Para conectar externamente: Use ferramentas como DBeaver ou pgAdmin (para PostgreSQL), ou abra o arquivo SQLite diretamente.

## 5. Inserts Automáticos (Seed Data)

- **Comando**: `python manage.py seed_data` (ou via Docker).
- **O que faz**: Popula o banco com dados de exemplo se estiver vazio (idempotente).
  - Cria 2 usuários (tutores) com pets.
  - Adiciona vacinas (ex.: Raiva, Distemper).
  - Registra vacinações de exemplo.
- **Arquivo**: `config/management/commands/seed_data.py`.
- **Uso**: Apenas para desenvolvimento/testes. Não execute em produção.

## 6. Autenticação com SimpleJWT

- **Biblioteca**: `djangorestframework-simplejwt`.
- **Como funciona**:
  - **Registro**: `POST /api/auth/register/` – Cria usuário e retorna tokens JWT (access e refresh).
  - **Login**: `POST /api/auth/login/` – Autentica e retorna tokens.
  - **Refresh**: `POST /api/auth/refresh/` – Renova access token com refresh.
  - **Uso**: Inclua `Authorization: Bearer <access_token>` nos headers de requests protegidos.
- **Configuração**: Em `settings.py` (SIMPLE_JWT), tokens duram 30 min (access) e 1 dia (refresh).
- **Permissões**: Endpoints exigem autenticação (exceto auth). Usuários acessam apenas seus dados.

## 7. Notas Adicionais

- **Endpoints**: Ver README.md para lista completa (/api/pets/, /api/vaccines/, etc.).
- **Filtros/Paginação**: Implementados globalmente (django-filter, paginação de 10 itens).
- **Tratamento de Erros**: Handler customizado em `config/exceptions.py`.
- **Admin**: Acesse /admin/ com superusuário.
- **Produção**: Configure DEBUG=False, use PostgreSQL, segredos fortes.

Se precisar de mais detalhes ou ajuda com algo específico, pergunte!
