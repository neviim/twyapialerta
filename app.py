#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser

from flask import Flask, jsonify
from flask import render_template
from flask import make_response
from flask import url_for
from flask import request
from flask import abort

from webserveralerta import TwAlerte
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app   = Flask(__name__)
twad = TwAlerte()

# log
config = ConfigParser.ConfigParser()
config.read("config.ini")

# Login
@auth.get_password
def get_password(username):
    if username == config.get("acesso", "user"):
        return config.get("acesso", "password")
    return None


@app.route("/")
@auth.login_required
def index():
    dado =  {  'by': 'Neviim Jads.',
                        'aplicacao': 'API',
                        'versao': 'V-0.3.7',
                        'titulo': 'Web server de Alerta por twitter.',
                        'home': 'http://127.0.0.1:5000',
                        'ping': 'http://127.0.0.1:5000/ping',
                        'public': 'http://127.0.0.1:5000/mensagem/public/ola Jads, mensagem publica.',
                        'direct': 'http://127.0.0.1:5000/mensagem/direct/@neviimdev/direct para Jads.' }

    return jsonify({'ficha': dado}), 201

# ping - pong
@app.route('/ping')
@auth.login_required
def ping():
  return 'pong'

# curl -u usuario:senha http://127.0.0.1:5000/mensagem/direct/@neviimdev/ola Jads
@app.route('/mensagem/direct/<nome>/<texto>', methods=['GET'])
@auth.login_required
def direct(nome, texto):
    twad.send_mensagem_direct( nome,  texto.encode('utf-8') )
    return "Aterta direct enviado! "+texto, 200

# curl -u usuario:senha http://127.0.0.1:5000/mensagem/publica/café%20com%20fé
@app.route('/mensagem/publica/<texto>', methods=['GET'])
@auth.login_required
def public(texto):
    twad.send_mensagem_public( texto.encode('utf-8') )
    return "Aterta publico enviado! "+texto, 200

# curl -u usuario:senha -i -H "Content-Type: application/json" -X POST -d '{"nome":"@neviimdev", "texto":"Bom dia"}'  http://127.0.0.1:5000/mensagem/
@app.route('/mensagem/', methods=['POST'])
@auth.login_required
def mensagem():
    if not request.json or not 'texto' in request.json:
        abort(400)
    if not 'nome' in request.json:
        twad.send_mensagem_public( request.json['texto'].encode('utf-8') )
    else:
        twad.send_mensagem_direct( request.json['nome'], request.json['texto'].encode('utf-8') )
    #
    return "Aterta enviado modo: POST! "+request.json['texto'].encode('utf-8'), 200


# --- Inicio
if __name__ == '__main__':
    app.run(  debug=True,
                    host="0.0.0.0",
                    port=int("5000")
    )