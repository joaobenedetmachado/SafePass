import numpy as np
import random

ascii_letters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
digits = '1234567890'
punctuation = '_-.'

def GerarSenhas(numero):
  letras = list(ascii_letters)
  numeros = list(digits)
  especial = list(punctuation)
  tds_carac = letras+numeros+especial
  senha = np.random.choice(list(tds_carac),numero)
  print(''.join(senha))
  return ''.join(senha)