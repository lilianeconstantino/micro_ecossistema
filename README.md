# Micro Ecossistema Empresarial

### O Micro Ecossistema é composto por 4 APIs e 4 Bancos de dados.

As REST APIs foram construídas utilizando a linguagem **Python**, com microframework **Flask**.
- Foram utilizadas durante o processo as bibliotecas nativas do Flask, a biblioteca requests (para as requisições), pymysql (para conexão do banco de dados) e o MySQL (para criação e manuseio o banco de dados).
- Cada API faz as operações de CRUD integrado com o MySQL.
- Para autenticação foi utilizado o HTTP basic autentication.

### Clientes
- Cria o cadastro de clientes
- Lista todos os clientes cadastrados
- Busca cliente por ID
- Busca cliente e seus endereços cadastrados por ID
- Atualiza cadastro
- Exclui cadastro
### Endereços
- Cria o endereços de clientes
- Lista todos os endereços cadastrados
- Busca endereço por id
- Atualiza endereço
- Exclui endereço
### Catalágo de Produtos
- Cria o produto
- Lista todos os produtos cadastrados
- Busca produto por id
- Atualiza produto
- Exclui produto
### Inventário
- Cria o inventário
- Lista todos os inventários cadastrados
- Lista inventário com informações de cliente e produtos
- Lista todas as informações do cliente por id (cadastro, endereço e produtos)
- Busca inventário por id
- Atualiza inventário
- Exclui inventário

### Passo a passo:

No diretório onde será criada cada API deve ser feito:

- Criar um abiente virtual:
```
python3 -m venv venv
```
- Ativar ambiente virtual:
```
. venv/bin/activate
```
- Instalar módulos Flask:
```
pip install Flask flask-mysql requests
pip install pymysql
```
- Para rodar a aplicação:
```
export FLASK_ENV=development
export FLASK_APP=main
flask run -p 5000 (cada API roda em um porta diferente)
```

**Os testes de requisições foram feitos no Postman**

**Fontes:**

- [Create RESTful API using Python & MySQL](https://webdamn.com/create-restful-api-using-python-mysql/) 
- [Flask](https://flask.palletsprojects.com/en/2.1.x/quickstart/)