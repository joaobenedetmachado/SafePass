import random

caracteres = list('QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklçzxcvbnm@#%-*')

def GerarSenhas(number):
    senha = []
    for _ in range(number):
        letraEsc = caracteres[random.randint(0, len(caracteres) - 1)]
        senha.append(letraEsc)
    return ''.join(senha)

