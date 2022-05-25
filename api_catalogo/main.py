from app import app
from config import mysql
import pymysql
from flask import jsonify, request
from auth import auth_required


@app.route('/create', methods=['POST']) #rota para criar um novo produto
@auth_required
def create_produto():    
    try:
        _json = request.json
        _produto = _json['produto']
        _tamanho = _json['tamanho']
        _sabor = _json['sabor']
        _quantidade = _json['quantidade']        
        if _produto and _tamanho and _sabor and _quantidade and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO catalogo (produto, tamanho, sabor, quantidade) VALUES(%s, %s, %s, %s)"
            bindData = (_produto, _tamanho, _sabor, _quantidade)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Produto cadastrado com sucesso!')
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

@app.route('/produtos') #rota para listar os produtos cadastrados
@auth_required
def produtos_list():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM catalogo") #seleciona todos as informações da tabela
        catRow = cursor.fetchall()
        response = jsonify(catRow)
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({"Message": f"{e}"})
        return response
    finally:
        cursor.close() 
        conn.close()  

@app.route('/produtos/<int:id_produto>') #rota de busca de produto por id específico
@auth_required
def produto_detail(id_produto):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM catalogo WHERE id_produto =%s", id_produto)
        catRow = cursor.fetchall()
        response = jsonify(catRow)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/update', methods=['PUT']) #rota para atualizar um produto
@auth_required
def update_produto():
    try:
        _json = request.json  
        _id_produto = _json['id_produto'] 
        _produto = _json['produto']
        _tamanho = _json['tamanho']
        _sabor = _json['sabor']
        _quantidade = _json['quantidade']
        if _produto and _tamanho and _sabor and _quantidade and request.method == 'PUT':			
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE catalogo SET produto=%s, tamanho=%s, sabor=%s, quantidade=%s WHERE id_produto=%s"
            bindData = (_produto, _tamanho, _sabor, _quantidade, _id_produto)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Produto atualizado com sucesso!')
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

@app.route('/delete/<int:id_produto>', methods=['DELETE']) #rota para deletar um produto
@auth_required
def delete_produto(id_produto):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM catalogo WHERE id_produto =%s", (id_produto))
		conn.commit()
		response = jsonify('Produto deletado com sucesso!')
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
    app.run(port=5003, debug=True) #informa em que porta a api deve rodar