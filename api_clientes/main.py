import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import request
from auth import auth_required

@app.route('/create', methods=['POST'])
@auth_required
def create_clientes():
    try:        
        _json = request.json             
        _nome = _json['nome']
        _email = _json['email']
        _cpf = _json['cpf']
        _telefone = _json['telefone']	
        _idade = _json['idade']        	
        if _nome and _email and _cpf and _telefone and _idade and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO cadastro(nome, email, cpf, telefone, idade) VALUES(%s, %s, %s, %s, %s)"
            bindData = (_nome, _email, _cpf, _telefone, _idade)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Cliente cadastrado com sucesso!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse
    finally:
        cursor.close() 
        conn.close()          
     
@app.route('/cadastro')
@auth_required
def cadastro():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM cadastro")
        cadRows = cursor.fetchall()
        response = jsonify(cadRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

@app.route('/cadastro/<int:id>')
@auth_required
def cadastro_detail(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, nome, email, cpf, telefone, idade FROM cadastro WHERE id =%s", id)
        cadRow = cursor.fetchone()
        response = jsonify(cadRow)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/update', methods=['PUT'])
@auth_required
def update_cadastro():
    try:
        _json = request.json  
        _id = _json['id']      
        _nome = _json['nome']
        _email = _json['email']
        _cpf = _json['cpf']
        _telefone = _json['telefone']	
        _idade = _json['idade']        
        if _nome and _email and _cpf and _telefone and _idade and id and request.method == 'PUT':			
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE cadastro SET nome=%s, email=%s, cpf=%s, telefone=%s, idade=%s WHERE id=%s"
            bindData = (_nome, _email, _cpf, _telefone, _idade, _id)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Cliente atualizado com sucesso!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})
        return reponse
    finally:
        cursor.close() 
        conn.close() 

@app.route('/delete/<int:id>', methods=['DELETE'])
@auth_required
def delete_cadastro(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM cadastro WHERE id =%s", (id,))
		conn.commit()
		response = jsonify('Cliente deletado com sucesso!')
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()        
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response
        
if (__name__ == "__main__"):
    app.run()