# Gerenciador_Books

## Descrição

Esse projeto foi criado com o intuito de ajudar no gerenciamento de livros 
e suas respectivas leituras, de forma segura e confortável.
Nessa api o usuário/cliente terá que se cadastrar e fazer login. Dessa forma 
garantindo a segurança e privacidade de cada leitor.

## Status do projeto 

Atualmente (data que foi postado o readme), parei o desenvolvimento por está 
em uma versão estável.

## Estrutura do projeto 

# Estrutura do Projeto

```plaintext
├── Gerenciador_Books
|   ├── .venv
|   ├── booksGen
│   │   ├── booksgen
│   │   │   ├── __pycache__
│   │   │   ├── apps
│   │   │   │   ├── __pycache__
│   │   │   │   ├── Auth.py
│   │   │   │   ├── Books.py
│   │   │   │   └── users.py
│   │   │   ├── db
│   │   │   │   ├── __pycache__
│   │   │   │   ├── migrations
│   │   │   │   │   ├── __pycache__
│   │   │   │   │   ├── versions
│   │   │   │   │   ├── README
│   │   │   │   │   ├── env.py
│   │   │   │   │   └── script.py.mako
│   │   │   │   ├── conection_bd.py
│   │   │   │   └── connection_db_redis.py
│   │   │   ├── schemas
│   │   │   │   ├── __pycache__
│   │   │   │   ├── schema_auth.py
│   │   │   │   ├── schema_books.py
│   │   │   │   ├── schema_messages.py
│   │   │   │   └── schema_users.py
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   ├── security.py
│   │   │   └── settings.py
│   │   ├── tests
│   │   │   ├── __pycache__
│   │   │   ├── migrationsTests
│   │   │   │   ├── __pycache__
│   │   │   │   ├── versions
│   │   │   │   ├── README
│   │   │   │   ├── env.py
│   │   │   │   └── script.py.mako
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   ├── test_Auth.py
│   │   │   ├── test_Book.py
│   │   │   ├── test_Security.py
│   │   │   └── test_Users.py
│   │   ├── .env
│   │   ├── README.md
│   │   ├── alembic.ini
│   │   ├── poesia.lock
│   │   └── pyproject.toml
|   ├── imgs_readme
|   │   ├── start.png
|   │   ├── start_docs_1.png
|   │   ├── start_docs_2.png
|   │   ├── start_docs_3.png
|   │   └── tests_sucess.png
|   ├── .getattributes
|   ├── LICENSE
|   ├── README.md
|   └── alembic.ini
```

## Tecnologias usadas 

Usei o **poetry** pra gerenciar todas as bibiotecas e ferramentas usadas:

```.toml
[tool.poetry]
name = "booksgen"
version = "0.1.0"
description = ""
authors = ["Josué Luiz Barbosa e Silva <104951932+josuelb@users.noreply.github.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = {extras = ["standard"], version = "^0.112.2"}
sqlalchemy = "^2.0.32"
alembic = "^1.13.2"
pydantic-settings = "^2.5.2"
pyjwt = "^2.9.0"
pwdlib = {extras = ["argon2"], version = "^0.2.1"}
python-multipart = "^0.0.9"
tzdata = "^2024.1"
redis = "^5.1.1"


[tool.poetry.group.dev.dependencies]
ruff = "^0.6.3"
pytest = "^8.3.2"
pymysql = "^1.1.1"
sqlalchemy = {extras = ["asyncio"], version = "^2.0.36"}

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Passos pra startar a api

### Inicializar o redis e o banco de dados  

O banco de dados e o cache devem ser iniciados antes de tudo.

No windows usa-se o comando para iniciar o redis:

```powershell
redis-server
```

### Alterar o .env

No .env é quem guarda as configurações, como link de databases, portas, Algoritimos etc.

```.env
DATABASE_URI="mysql+pymysql://you-root:you-password@localhost:you-port/you-principal-db"
DATABASE_TESTS_URI="mysql+pymysql://you-root:you-password@localhost:you-port/you-test-db"
PORT_REDIS=6379
HOST_REDIS="localhost"

SECRET_KEY="your-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
ZONE_INFO_HOUR="UTC"
```

### Iniciar a VENV

A venv é quem esta com todas as bibliotecas salvas e é ela quem vai gerenciar a api.
Caso sua IDE nao inicie ela, digite no terminal:

```powershell
.venv/Scripts/activate
```

**Lembre-se: O terminal deve abrir a raiz do projeto**

### Subir as tabelas pro banco de dados

User o seguinte comando pra cirar as imigrações:

```powershell
alembic revision --autogenerate -m "create tables"
```

E para subi-las:

```powershell
alembic upgrade head
```

### Gere os testes

Para certifica-se que esta tudo bem gere os testes.

```powershell
pytest -vv
```

### Iniciar a api

```cmd
fastapi dev booksGen/bookgen/main.py
```
