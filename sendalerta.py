#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 'Neviim Jads'
#
import sys
import getopt
import ConfigParser

from webserveralerta import TwAlerte


# funcao main
def main(argv):
    nome = ''
    mensagem = ''
    # Validando parametros
    try:
      opts, args = getopt.getopt(argv,"hn:m:",["nome=","mensagem="])
    except getopt.GetoptError:
      print 'sendalerta.py -n <nome> -m <mensagem>'
      sys.exit(2)

    for opt, arg in opts:
      # -h <ajuda>
      if opt == '-h':
         print 'sendalerta.py -n <nome> -o <mensagem>'
         sys.exit()
      # -n <nome>
      elif opt in ("-n", "--nome"):
         nome = arg
      # -m <mensagem>
      elif opt in ("-m", "--mensagem"):
         mensagem = arg

    # se mensagem for nula, returna com status de False.
    if mensagem == '':
        return False
    else:
        # se nome for nulo retorna com status de False.
        if nome == '':
            return False
        else:
            # tendo uma mensagem ela sera encaminhada.
            twa = TwAlerte()
            twa.send_mensagem_direct( nome, mensagem )
        return True


# iniciando
if __name__ == "__main__":
    if main(sys.argv[1:]):
        print "Alerta enviado!"
    else:
        print "Alerta não enviado!"
