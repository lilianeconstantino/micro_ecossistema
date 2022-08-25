from app import app
from config import mysql
import pymysql
from flask import jsonify, request
from auth import auth_required

@app.route("/health")
def health():
    return

@app.route('/endereco', methods=['POST']) #rota para criar um novo endereço
@auth_required
def create_endereco():    
    try:
        _json = request.json
        _rua = _json['rua']
        _numero = _json['numero']
        _bairro = _json['bairro']
        _cidade = _json['cidade']
        _estado = _json['estado']
        _cep = _json['cep']
        _id_cliente = _json['id_cliente']
        if _rua and _numero and _bairro and _cidade and _estado and _cep and _id_cliente and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO endereco (rua, numero, bairro, cidade, estado, cep, id_cliente) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            bindData = (_rua, _numero, _bairro, _cidade, _estado, _cep, _id_cliente)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Endereço cadastrado com sucesso!')
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

@app.route('/endereco') #rota para listar os endereços cadastrados
@auth_required
def endereco_list():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM endereco") #seleciona todos as informações da tabela
        endRow = cursor.fetchall()
        response = jsonify(endRow)
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({"Message": f"{e}"})
        return response
    finally:
        cursor.close() 
        conn.close()  

@app.route('/endereco/<int:id_cliente>') #rota de busca de endereço por id específico
@auth_required
def endereco_detail(id_cliente):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id_cliente, rua, numero, bairro, cidade, estado, cep, id_end FROM endereco WHERE id_cliente =%s", id_cliente)
        endRow = cursor.fetchall()
        response = jsonify(endRow)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/endereco', methods=['PUT']) #rota para atualizar um endereço
@auth_required
def update_endereco():
    try:
        _json = request.json  
        _id_end = _json['id_end']      
        _rua = _json['rua']
        _numero = _json['numero']        
        _bairro = _json['bairro']
        _cidade = _json['cidade']	
        _estado = _json['estado']
        _cep = _json['cep']
        _id_cliente = _json['id_cliente']
        if _rua and _numero and _bairro and _cidade and _estado and _cep and _id_cliente and _id_end and request.method == 'PUT':			
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE endereco SET rua=%s, numero=%s, bairro=%s, cidade=%s, estado=%s, cep=%s, id_cliente=%s WHERE id_end=%s"
            bindData = (_rua, _numero, _bairro, _cidade, _estado, _cep, _id_cliente, _id_end)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Endereço atualizado com sucesso!')
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

@app.route('/endereco/cliente/<int:id_cliente>', methods=['DELETE']) #rota para deletar todos os endereços do cliente
@auth_required
def delete_endereco(id_cliente):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM endereco WHERE id_cliente =%s", (id_cliente))
		conn.commit()
		response = jsonify('Endereço deletado com sucesso!')
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/endereco/<int:id_end>', methods=['DELETE']) #rota para deletar um endereço
@auth_required
def endereco_apagar(id_end):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM endereco WHERE id_end =%s", (id_end))
		conn.commit()
		response = jsonify('Endereço deletado com sucesso!')
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.errorhandler(404)
def showMessage(error=None): #função que define mensagens de código de erro
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if (__name__ == "__main__"):
    app.run(port=5001, debug=True, host='0.0.0.0') #informa em que porta a api deve rodar