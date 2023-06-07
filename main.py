from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY"

url_banco = "http://192.168.0.42:5000"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list')
def list():
    url = url_banco + '/seletor'
    response = requests.get(url)
    seletores = json.loads(response.text)
    return render_template('list.html', seletores=seletores)

@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    url = url_banco + '/seletor/' + str(id)
    response = requests.get(url)
    seletor = json.loads(response.text)
    return render_template('edit.html', seletor=seletor)

@app.route('/remove/<int:id>', methods=['GET'])
def remove(id):
    url = url_banco + '/seletor/' + str(id)
    response = requests.get(url)
    seletor = json.loads(response.text)
    return render_template('remove.html', seletor=seletor)

@app.route('/erro')
def erro():
    return render_template('erro.html')

@app.route('/submit', methods=['POST'])
def submit():
    nome = request.form['nome']
    ip = request.form['ip']

    url = url_banco + '/seletor/' + nome + '/' + ip
    data = {'nome': nome, 'ip': ip}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        flash("Cadastro efetuado com sucesso", "message")
        return redirect(url_for('list'))
    else:
        flash("Erro no cadastro", "error")
        return redirect(url_for('erro'))

@app.route('/update', methods=['POST'])
def update():
    nome = request.form['nome']
    ip = request.form['ip']
    id = request.form['id']

    url = url_banco + '/seletor/' + id + '/' + nome + '/' + ip
    data = {'id': id, 'nome': nome, 'ip': ip}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        flash("Cadastro alterado com sucesso", "message")
        return redirect(url_for('list'))
    else:
        flash("Erro na alteração", "error")
        return redirect(url_for('erro'))

@app.route('/delete', methods=['POST'])
def delete():
    id = request.form['id']

    url = url_banco + '/seletor/' + id
    data = {'id': id}
    response = requests.delete(url, json=data)

    if response.status_code == 200:
        flash("Cadastro excluído com sucesso", "message")
        return redirect(url_for('list'))
    else:
        flash("Erro na exclusão", "error")
        return redirect(url_for('erro'))

if __name__ == '__main__':
    app.run()
