## API de Controle de Vacinação de Pets

### Visão Geral do Projeto

Este projeto é uma API REST para um sistema de clínica veterinária responsável por gerenciar o histórico de vacinação de pets.

Ela fornece endpoints para gerenciar tutores (usuários), pets, vacinas e registros de vacinação, garantindo acesso seguro por meio de autenticação JWT.

A API foi desenvolvida com **Django** e **Django REST Framework**, utilizando banco de dados relacional PostgreSQL.

---

### Stack Tecnológica

* **Linguagem**: Python 3.11+
* **Framework**: Django, Django REST Framework
* **Autenticação**: JWT (SimpleJWT)
* **Banco de Dados**: PostgreSQL
* **Outras Bibliotecas**: django-environ, django-filter
* **Containerização**: Docker, docker-compose

---

### Estrutura do Projeto

* `config/`: Configurações do projeto Django, URLs, WSGI/ASGI, handler customizado de exceções, comando de seed.
* `users/`: Modelo de usuário customizado e registro de tutores.
* `pets/`: Modelo de Pet e operações CRUD.
* `vaccines/`: Modelo de Vacina e operações CRUD.
* `vaccinations/`: Registros de vacinação, filtros e operações CRUD.
* `requirements.txt`: Dependências Python.
* `Dockerfile` e `docker-compose.yml`: Configuração de container e orquestração.
* `.env.example`: Exemplo de variáveis de ambiente.

---

## Instruções de Configuração (Sem Docker)

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd pet-vaccination
```

### 2. Criar e ativar um ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/macOS
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Criar o arquivo `.env`

Copie o `.env.example` para `.env` e ajuste os valores se necessário:

```bash
cp .env.example .env
```

### 5. Executar as migrações

```bash
python manage.py migrate
```

### 6. Popular dados iniciais (opcional, para desenvolvimento local)

```bash
python manage.py seed_data
```

### 7. Criar um superusuário (opcional, para acesso ao admin)

```bash
python manage.py createsuperuser
```

### 8. Iniciar o servidor de desenvolvimento

```bash
python manage.py runserver
```

A API estará disponível em:

```
http://127.0.0.1:8000/
```

---

## Instruções de Configuração (Com Docker)

### 1. Copiar `.env.example` para `.env` e configurar as variáveis do PostgreSQL, se desejar.

### 2. Construir e iniciar os serviços

```bash
docker-compose up --build
```

### 3. Aplicar migrações e popular dados (dentro do container `web`)

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py seed_data
```

A API estará disponível em:

```
http://127.0.0.1:8000/
```

---

## Guia de Autenticação

A autenticação é feita utilizando JWT (JSON Web Tokens) via SimpleJWT.

### 🔐 Registro

`POST /api/auth/register/`

**Body da requisição:**

* `full_name` (string, obrigatório)
* `email` (string, obrigatório, único)
* `phone_number` (string, opcional)
* `password` (string, obrigatório)
* `password_confirm` (string, obrigatório, deve ser igual ao `password`)

**Resposta:**

* Dados do usuário
* Tokens JWT (`access`, `refresh`)

---

### 🔑 Login

`POST /api/auth/login/`

**Body da requisição:**

* `username`: email utilizado no cadastro
* `password`

**Resposta:**

* Tokens `access` e `refresh`

---

### 🔄 Refresh Token

`POST /api/auth/refresh/`

**Body da requisição:**

* `refresh`: token de atualização

**Resposta:**

* Novo token `access`

---

Para todos os endpoints protegidos, inclua o header:

```http
Authorization: Bearer <access_token>
```

---

# Endpoints da API

Caminho base da API:

```
/api/
```

---

## Autenticação

* `POST /api/auth/register/` – Registrar novo usuário (tutor).
* `POST /api/auth/login/` – Obter tokens JWT.
* `POST /api/auth/refresh/` – Atualizar token de acesso.

---

## Usuários

* `GET /api/users/` – Listar usuários (apenas staff).
* `GET /api/users/{id}/` – Detalhar usuário.

  * Usuários comuns podem visualizar apenas seu próprio registro.
  * Usuários staff podem visualizar qualquer usuário.

---

## Pets

CRUD completo para pets. Usuários só podem acessar seus próprios pets.

* `GET /api/pets/` – Listar pets do usuário autenticado.
* `POST /api/pets/` – Criar pet (o owner é definido automaticamente).
* `GET /api/pets/{id}/` – Detalhar pet do usuário autenticado.
* `PUT /api/pets/{id}/` – Atualizar pet.
* `PATCH /api/pets/{id}/` – Atualização parcial.
* `DELETE /api/pets/{id}/` – Remover pet.

### Filtros e busca

Parâmetros de query:

* `species` – filtrar por espécie.
* `breed` – filtrar por raça.
* `?search=<termo>` – buscar por nome ou raça.

---

## Vacinas

CRUD completo para vacinas.

* `GET /api/vaccines/`
* `POST /api/vaccines/`
* `GET /api/vaccines/{id}/`
* `PUT /api/vaccines/{id}/`
* `PATCH /api/vaccines/{id}/`
* `DELETE /api/vaccines/{id}/`

### Filtros e ordenação

* `manufacturer` – filtrar por fabricante.
* Ordenação:

  * `?ordering=name`
  * `?ordering=-created_at`

---

## Vacinações

CRUD completo para registros de vacinação.
Usuários só podem acessar vacinações de pets que lhes pertencem.

* `GET /api/vaccinations/`
* `POST /api/vaccinations/`
* `GET /api/vaccinations/{id}/`
* `PUT /api/vaccinations/{id}/`
* `PATCH /api/vaccinations/{id}/`
* `DELETE /api/vaccinations/{id}/`

### Filtros

* `?pet=1` – filtrar por ID do pet.
* `?vaccine=2` – filtrar por ID da vacina.
* `?upcoming=true` – filtrar vacinações futuras onde `next_due_date` é maior ou igual à data atual.

---

# Decisões Técnicas

## Modelagem de Dados

### Usuário (Tutor)

* Extensão do `AbstractUser` do Django.
* Campos adicionais:

  * `full_name`
  * `phone_number`
  * `created_at` automático
* O email é único e também utilizado como username no login.

### Pet

* Relacionado ao `User` como `owner`.
* Campos principais:

  * `species`
  * `breed`
  * `birth_date`
  * `weight`

### Vacina

* Possui `periodicity_days` para permitir cálculo automático da próxima vacinação.

### Vacinação

* Relaciona `Pet` e `Vaccine`.
* Campos:

  * `application_date`
  * `next_due_date`
  * `notes`
  * `veterinarian_name`

---

## Estratégia de Autenticação

* JWT implementado com **SimpleJWT**.
* Endpoint de registro já retorna tokens.
* Todos os endpoints (exceto registro e tokens) exigem autenticação (`IsAuthenticated` global).

---

## Lógica de Permissões

### Usuários

* Permissão `IsSelfOrAdmin`:

  * Listagem restrita a staff.
  * Visualização permitida apenas para o próprio usuário ou staff.

### Pets

* Permissão `IsPetOwner`.
* Queryset filtrado por `owner=request.user`.

### Vacinações

* Permissão `IsVaccinationPetOwner`.
* Validação no serializer garante que só é possível criar vacinação para pets do usuário autenticado.

---

## Decisões Arquiteturais

### Separação em Apps

* `users`, `pets`, `vaccines`, `vaccinations`
* Facilita manutenção, escalabilidade e organização.

### ViewSets + Routers

* Uso de `ViewSet` do DRF com `DefaultRouter`.
* URLs RESTful padronizadas.

### Filtros e Paginação

* Paginação global configurada no DRF.
* Uso de `django-filter`.
* Filtros específicos implementados com `FilterSet`.

### Tratamento de Exceções

* Handler customizado:

  ```
  config.exceptions.custom_exception_handler
  ```
* Respostas padronizadas com status HTTP apropriado.

### Configuração por Ambiente

* Uso de `django-environ`.
* `.env.example` documenta variáveis necessárias.
* Suporte a PostgreSQL.

### Docker

* `Dockerfile` com imagem Python enxuta.
* `docker-compose.yml` com:

  * Serviço `web`
  * Serviço `db` (PostgreSQL)

---

# Seed de Dados

Existe um comando customizado `seed_data` para popular o banco com dados de exemplo:

* Usuários (tutores) com pets.
* Vacinas comuns.
* Registros de vacinação de exemplo.

### Uso:

```bash
python manage.py seed_data
```

Esse comando é idempotente para banco vazio e recomendado apenas para desenvolvimento e testes.


---

# Painel Administrativo - Django

O Django possui um painel administrativo pronto para gerenciar os dados da aplicação (usuários, pets, vacinas, vacinações etc.).

### 1. Criar um superusuário
Caso ainda não tenha criado um usuário administrador:

### Uso:

```bash
python manage.py createsuperuser
```

Preencha
* Email
* Senha

### 2. Iniciar o servidor

### Uso:

```bash
python manage.py runserver
```

Por padrão, o servidor ficará disponível em:

```bash
http://127.0.0.1:8000/
```

### 3. Acessar o painel administrativo

Abra o navegador e acesse:

### Uso:

```bash
http://127.0.0.1:8000/admin/
```

Faça login com as credenciais.

### 4. O que pode ser feito no Admin

No painel administrativo é possível:

* Gerenciar usuários (tutores)
* Cadastrar e editar pets
* Gerenciar vacinas
* Visualizar e alterar registros de vacinação
* Aplicar filtros e buscas nos registros
