from app import app
from config import mysql
import pymysql
from flask import jsonify, request
from auth import auth_required
import requests
import json


@app.route('/inventario', methods=['POST']) 
@auth_required
def create_inventario():    
    try:
        _json = request.json
        _id_iproduto = _json['id_iproduto']
        _id_cliente = _json['id_cliente']               
        if _id_iproduto and _id_cliente and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO inventario (id_iproduto, id_cliente) VALUES(%s, %s)"
            bindData = (_id_iproduto, _id_cliente)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Sucesso!')
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

@app.route('/inventario') 
@auth_required
def inventario_list():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM inventario") 
        invRow = cursor.fetchall()
        response = jsonify(invRow)
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({"Message": f"{e}"})
        return response
    finally:
        cursor.close() 
        conn.close()  

@app.route('/inventario/<int:id_cliente>') 
@auth_required
def inventario_detail(id_cliente):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM inventario WHERE id_cliente =%s", id_cliente)
        invRow = cursor.fetchall()
        response = jsonify(invRow)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/inventario', methods=['PUT']) 
@auth_required
def update_inventario():
    try:
        _json = request.json  
        _id_inventario = _json['id_inventario'] 
        _id_iproduto = _json['id_iproduto'] 
        _id_cliente = _json['id_cliente']         
        if _id_iproduto and _id_cliente and _id_inventario and request.method == 'PUT':			
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE inventario SET id_iproduto=%s, id_cliente=%s WHERE id_inventario=%s"
            bindData = (_id_iproduto, _id_cliente, _id_inventario)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Atualizado com sucesso!')
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

@app.route('/inventario/<int:id_inventario>', methods=['DELETE']) 
@auth_required
def delete_inventario(id_inventario):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM inventario WHERE id_inventario =%s", (id_inventario))
		conn.commit()
		response = jsonify('Deletado com sucesso!')
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/inventario/cadastro/<int:id_cliente>') 
@auth_required
def inventario_complete(id_cliente): 
    
    url = requests.get('http://127.0.0.1:5002/cadastro', auth=('username', '8080'))
    text = url.text
    data_cadastro = json.loads(text)        
    
    lista_cadastro = []     
    for cadastro in data_cadastro:
        if cadastro['id'] == id_cliente:
            lista_cadastro.append(cadastro)    

        url_e = requests.get('http://127.0.0.1:5001/endereco', auth=('username', '8080')) 
        text = url_e.text
        data_e = json.loads(text)        
        lista_endereco = []     
        for endereco in data_e:
            if endereco['id_cliente'] == id_cliente:
                lista_endereco.append(endereco)
    
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id_iproduto FROM inventario WHERE id_cliente=%s", id_cliente)        
    ids = cursor.fetchall()
    response = jsonify(lista_cadastro, lista_endereco)
    lista_id = []
    lista = []     
    for id in ids:
        id_iproduto = id['id_iproduto']
        lista_id.append(id_iproduto) 

        r = requests.get('http://127.0.0.1:5003/produtos/'+str(id_iproduto), auth=('username', '8080'))         
        produto_text = r.text
        data_p = json.loads(produto_text)
        lista.append(data_p)   
        
    try:
        response = {}
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM inventario WHERE id_cliente=%s", id_cliente)        
        invRow = cursor.fetchall()
        response['Inventário'] = invRow
        response['Cliente'] = lista_cadastro
        response['Endereços'] = lista_endereco 
        response['Produtos'] = lista    
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()   

@app.route('/inventario/produto/<int:id_cliente>') 
@auth_required
def inventario_produto(id_cliente): 
    
    url = requests.get('http://127.0.0.1:5002/cadastro', auth=('username', '8080'))
    text = url.text
    data_cadastro = json.loads(text)        
    
    lista_cadastro = []     
    for cadastro in data_cadastro:
        if cadastro['id'] == id_cliente:
            lista_cadastro.append(cadastro)         
    
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id_iproduto FROM inventario WHERE id_cliente=%s", id_cliente)        
    ids = cursor.fetchall()
    lista_id = []
    lista = []     
    for id in ids:
        id_iproduto = id['id_iproduto']
        lista_id.append(id_iproduto) 

        r = requests.get('http://127.0.0.1:5003/produtos/'+str(id_iproduto), auth=('username', '8080'))         
        produto_text = r.text
        data_p = json.loads(produto_text)
        lista.append(data_p)        
    try:
        response = {}
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM inventario WHERE id_cliente=%s", id_cliente)        
        invRow = cursor.fetchall()
        response['Inventário'] = invRow
        response['Cliente'] = lista_cadastro
        response['Produtos'] = lista    
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
    app.run(port=5004, debug=True, host='0.0.0.0') #informa em que porta a api deve rodar