from app import app
from flaskext.mysql import MySQL

mysql = MySQL(app) 
app.config['MYSQL_DATABASE_USER'] = 'admin' 
app.config['MYSQL_DATABASE_PASSWORD'] = 'senhafortedb' 
app.config['MYSQL_DATABASE_DB'] = 'clientes' 
app.config['MYSQL_DATABASE_HOST'] = 'database-cali.ckatnedhbqjh.us-east-2.rds.amazonaws.com' 

mysql.init_app(app)

# mysql = MySQL(app) #conexão com o banco de dados 
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'Senha-forte-para-dados1'
# app.config['MYSQL_DATABASE_DB'] = 'clientes'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'