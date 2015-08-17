# -*- coding: utf-8 -*-
#
# neviim v-0.3
#
# dependencias
#   $ pip install Flask
#
# referencia
#   https://github.com/mitsuhiko/flask/tree/master/examples/flaskr/
#
import glob
import logging
import logging.handlers
import ConfigParser
import tweepy
import socket
import fcntl
import struct
import sys
import re

from datetime import datetime, date, time


# ---
class TwAlerte(object):
        """doc para TwAlerte"""
        def __init__(self):
            super(TwAlerte, self).__init__()
            # --- abri arquivo de configuração
            self.config = ConfigParser.ConfigParser()
            self.config.read("config.ini")

            self.ipzerado = 0
            # --- socket
            self.hostname = socket.getfqdn()
            # --- key acesso ao twitter
            self.consumer_key = self.config.get("keyconfig", "consumer_key")
            self.consumer_secret = self.config.get("keyconfig", "consumer_secret")
            self.access_token          = self.config.get("keyconfig", "access_token")
            self.access_token_secret = self.config.get("keyconfig", "access_token_secret")

            self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            self.auth.set_access_token(self.access_token, self.access_token_secret)
            self.api = tweepy.API(self.auth)

            # log
            self.apilog = logging.getLogger('TwAlerte')
            self.apilog.setLevel(logging.DEBUG)
            logging.basicConfig(level=logging.WARNING)

            # handler
            self.handler = logging.handlers.RotatingFileHandler('./log/'+self.config.get("log", "logfilename"),
                                                                                     maxBytes=self.config.get("log", "maxBytes"),
                                                                                     backupCount=self.config.get("log", "numArquivos"))
            self.apilog.addHandler(self.handler)

        # --- pega o ip.
        def get_ip(self, ifname):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                return socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915, # SIOCGIFADDR
                    struct.pack('256s', ifname[:15])
                )[20:24])
            except IOError:
                return 0

        # ---  returna interface utilizada
        def get_interface(self):
            interfaces = ['eth0', 'eth1', 'wlan0']
            addresses = {}

            for interface in interfaces:
                interface_ip = self.get_ip(interface)
                if interface_ip != self.ipzerado:
                    addresses[interface] = interface_ip

            # --- formata o resultado para saida
            return "".join([', %s: %s' % (k, v) for k, v in addresses.iteritems()])

        # --- send mensagem publica
        def send_mensagem_public(self, menssagem):
            self.api.update_status(status=menssagem)

            # mensagem  enviada para o arquivo log.
            if self.config.getboolean ("log", "gravalog"):
                self.apilog.info(menssagem)

            return True

        # --- send mensagem direct
        def send_mensagem_direct(self, to_user, menssagem):
            keynow = datetime.now()
            interfaces_output = self.get_interface()
            keyid = "".join( re.findall(r'\d+', str(keynow)) )

            # mensagem  enviada para o arquivo log.
            if self.config.getboolean ("log", "gravalog"):
                texto_log = 'id: {0}, hostname: {1}{2}, menssagem: {3}'.format(keyid, self.hostname, interfaces_output, menssagem)
                self.apilog.info(texto_log)

            # menssagem enviada para o twitter
            tweet_text = 'id: {0}, msg: {1}'.format(keyid, menssagem)

            if len(tweet_text) > 500:
                print 'Mensagem não enviada, ela esta com %d caracter.' % len(tweet_text)
                return False
            else:
                self.api.send_direct_message(user = to_user, text = tweet_text)
                return True


# inicializa banco de dados
# https://docs.python.org/3/library/sqlite3.html
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('serveralerta.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


if __name__ == '__main__':
    #
    twa = TwAlerte()
    twa.send_mensagem_direct('@neviimdev',  'menssagem de webserveralerta.')
    #twa.send_mensagem_public('Mensagem publica e direct')
