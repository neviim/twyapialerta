# Caso não tenha instalado:

    # prepara o ambiente da aplicação
    $ sudo apt-get install virtualenvwrapper
    $ sudo apt-get install python-virtualenv

    $ cd v-0.3
    $ source tws_env/bin/activate

    # dependencias
    (tws_env)$ pip install flask-httpauth
    (tws_env)$ pip install configparser

    # configuraçoes
    (tws_env)$ sudo /var/log/webalerta
    (tws_env)$ sudo chown myUsuario:myUsuario /var/log/webalerta
    (tws_env)$ ln -s /var/log/webalerta log

    # executa a aplicação
    (tws_env)$ python app.py
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

    # para testar resposnata so server
    $ curl -u usuario:senha http://127.0.0.1:5000/ping

    # Para mensagem direct com uma só palavra de envio
    $ curl -u usuario:senha http://127.0.0.1:5000/mensagem/direct/@neviimdev/café
    $ curl -u usuario:senha http://127.0.0.1:5000/mensagem/direct/@neviimdev/fé

    # Envio de frases, usando "curl" segue a referencia abaixo, esta mensagem é enviada a um usuario especido de forma privada por direct.
    $ curl -u usuario:senha -i -H "Content-Type: application/json" -X POST -d '{"nome":"@neviimdev", "texto":"Bom dia"}'  http://127.0.0.1:5000/mensagem/

    # Envio de frases, usando "curl" segue a referencia abaixo, esta mensagem é enviada publica, a barra / no final é fundamental.
    $ curl -u usuario:senha -i -H "Content-Type: application/json" -X POST -d '{"texto":"Bom dia"}'  http://127.0.0.1:5000/mensagem/


    # usando pelo shell
    $ sendmensagem --nome @nomeTwitter --mensagem 'testo a ser enviado'


        # Para este programa passa dois parametros
            -n  ou --nome
            -m ou --mensagem

            $ python sendalerta.py -n @UserTwitter -m 'Mensagem a ser enviada.'


****************************************************************************************************
# V-0.4.0
    - Ciado um programa sendalerta.py que recebe 2 parametros nome e mensagem, uso no SHELL
    - Colocado uma varialvel para controle interno de versão em __init__.py
    - Documentação ajustada.

# V-0.3.7
    - Permitir passagem de parametro @nome e mensagem por linha de comando usando "CURL".
    - Otimisando a API para envio de mensagem public ou privat, usando uma unica chamada POST.
    - Colocando o ajuste do tamanho do arquivo de log e quantidade do log ajustado pelo arquivo config.ini
    - Atualização do arquivo README

# V-0.3.6
    - Menssagem de envinho do alerta com cabeçaçho resumido para (id:) e (msg:)
    - As mensaggens enviadas public e direct estara sendo enviada para o arquivo log.
    - Novas variaveis no arquivo config.ini, o arquivo sera substituido, tire backup da keys de acesso.
    - Criar um link de um diretorio de /var/log/webalerta para a pasta de nome log no diretorio local.
    - Especificado na tag #configuraçoes acima.
    - Instalar dependencia, configparser como especificado em #dependencias no texto acima.
    - Atualização do arquivo README

# V-0.3.5
    - Colocado o recursos para chamar as variaveis de altenticação key a partir do arquivo config.ini
    - O usuario e senha para altenticar a aplicação agora esta sendo lido do arquivo config.ini
    - Atualização do arquico README.

# V-0.3.4
    - Envia uma mensagem ping e espera um retorno Pong, teste se o serviço esta de pé.
    - Passagem de função para class.
    - Permite passagem de parametro com acentos.
    - Realizado algumas otimizações no codigo.




# referencia:
Para configurar o Browse (JSON-DataView)
https://github.com/warren-bank/moz-json-data-view
