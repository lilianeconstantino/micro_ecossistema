API feita como parte de um Microsserviço Empresarial

Para utilização:

Criar um abiente virtual:
python3 -m venv venv
Ativar ambiente virtual:
. venv/bin/activate
Instalar módulos Flask:
pip install Flask
pip install pymysql

Para rodar a aplicação:
export FLASK_ENV=development
export FLASK_APP=main
flask run 