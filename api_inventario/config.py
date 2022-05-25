from app import app
from flaskext.mysql import MySQL

mysql = MySQL(app) #configuração para conexão com o banco de dados
app.config['MYSQL_DATABASE_USER'] = 'root' #usuário padrão local
app.config['MYSQL_DATABASE_PASSWORD'] = 'Senha-forte-para-dados1' #senha do mysql
app.config['MYSQL_DATABASE_DB'] = 'inventario_produtos' #nome do banco de dados
app.config['MYSQL_DATABASE_HOST'] = 'localhost' #endereço padrão local

mysql.init_app(app)