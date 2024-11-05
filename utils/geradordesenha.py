#Esta linha importa bibliotecas para o python
import numpy as np
import random

#Estas 3 linhas colocam os números, caracteres especiais e letras em váriaveis
ascii_letters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
digits = '1234567890'
punctuation = '_-.'

#Esta função pega os números/caracteres especiais/letras e randomifica de acordo com a quantidade desejada pelo cliente.
def GerarSenhas(numero):
  letras = list(ascii_letters)
  numeros = list(digits)
  especial = list(punctuation)
  tds_carac = letras+numeros+especial
  senha = np.random.choice(list(tds_carac),numero)
  print(''.join(senha))
  return ''.join(senha)

