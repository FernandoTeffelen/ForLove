from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def carregar_respostas():
    if os.path.exists('respostas.json'):
        with open('respostas.json', 'r') as f:
            return json.load(f)
    return []

def salvar_respostas(respostas):
    with open('respostas.json', 'w') as f:
        json.dump(respostas, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nome = request.form['nome']
        mensagem = request.form['mensagem']
        data = request.form['data']
        hora = request.form['hora']

        imagens = request.files.getlist('imagens')
        nomes_imagens = []

        for imagem in imagens:
            if imagem and allowed_file(imagem.filename):
                filename = secure_filename(imagem.filename)
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagem.save(caminho)
                nomes_imagens.append(filename)

        resposta = {
            'nome': nome,
            'mensagem': mensagem,
            'data': data,
            'hora': hora,
            'imagem': nomes_imagens
        }

        respostas = carregar_respostas()
        respostas.append(resposta)
        salvar_respostas(respostas)

        return redirect(url_for('respostas_por_nome', nome_slug="-".join(nome.split())))

    return render_template('form.html')

@app.route('/<nome_slug>', methods=['GET'])
def respostas_por_nome(nome_slug):
    respostas = carregar_respostas()

    respostas_filtradas = [r for r in respostas if "-".join(r['nome'].split()) == nome_slug]

    if not respostas_filtradas:
        return render_template('respostas.html', titulo="Respostas", respostas=[])

    return render_template('respostas.html', titulo="Respostas", respostas=respostas_filtradas)

if __name__ == '__main__':
    app.run(debug=True)
