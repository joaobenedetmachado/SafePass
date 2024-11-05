import numpy as np
import random


ascii_letters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
digits = '1234567890'
punctuation = '_-.'

pergunta = int(input("Digite quantos caracteres você quer que a sua senha tenha:"))

if pergunta >=7 and pergunta <= 13:
    letras = list(ascii_letters)
    numeros = list(digits)
    especial = list(punctuation)
    tds_carac = letras+numeros+especial
    senha = np.random.choice(list(tds_carac),pergunta)
    print(''.join(senha))

elif pergunta <7:
    print("Senha inválida, poucos caractéres na senha")

elif pergunta >13:
    print("Senha inválida, quantidade desenecessária de caractéres.")


# def GerarSenhas(number):

#     return senha


# GerarSenha(10)

