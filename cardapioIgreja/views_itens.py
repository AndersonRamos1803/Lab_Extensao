from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from cardapio import app, db
from models import Itens
from helpers import recupera_imagem, deleta_arquivo, FormularioItem
import time


@app.route('/')
def index():
    lista = Itens.query.order_by(Itens.id)
    return render_template('lista.html', titulo='itens', itens=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioItem()
    return render_template('novo.html', titulo='Novo Item', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioItem(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    descricao = form.descricao.data
    preco = form.preco.data

    item = Itens.query.filter_by(nome=nome).first()

    if item:
        flash('Item já existente!')
        return redirect(url_for('index'))

    novo_item = Itens(nome=nome, descricao=descricao, preco=preco)
    db.session.add(novo_item)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_item.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    item = Itens.query.filter_by(id=id).first()
    form = FormularioItem()
    form.nome.data = item.nome
    form.descricao.data = item.descricao
    form.preco.data = item.preco
    capa_item = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Item', id=id, capa_item=capa_item, form=form)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioItem(request.form)

    if form.validate_on_submit():
        item = Itens.query.filter_by(id=request.form['id']).first()
        item.nome = form.nome.data
        item.descricao = form.descricao.data
        item.preco = form.preco.data

        db.session.add(item)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(id)
        arquivo.save(f'{upload_path}/capa{item.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Itens.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Item deletado com sucesso!')

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)