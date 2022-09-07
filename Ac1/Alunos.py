import os
from flask import Flask, render_template, request
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# Configurações para o MySQL
# define o nome do user
app.config['MYSQL_DATABASE_USER'] = 'root'
# define a senha
app.config['MYSQL_DATABASE_PASSWORD'] = '12345'
# define o nome do DB
app.config['MYSQL_DATABASE_DB'] = 'DB_alunos'
# caso usando o docker, o ip precisar ser o da imagem do MySQL
# docker network inspect bridge
app.config['MYSQL_DATABASE_HOST'] = '172.17.0.2'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/gravarAluno', methods=['POST','GET'])
def gravarAluno():
  nome = request.form['nome']
  cpf = request.form['cpf']
  endereco = request.form['endereco']
  if nome and cpf and endereco:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('insert into dados_alunos (aluno, cpf, endereco) VALUES (%s, %s, %s)', (nome, cpf, endereco))
    conn.commit()
  return render_template('index.html')


@app.route('/listar', methods=['POST','GET'])
def listar():
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute('select nome, cpf, endereco from dados_alunos')
  data = cursor.fetchall()
  conn.commit()
  return render_template('lista.html', datas=data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5008))
    app.run(host='0.0.0.0', port=port)
