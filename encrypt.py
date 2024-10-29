from cryptography.fernet import Fernet

#Define a chave para o processo de criptografia e descriptografia
key = b'pwuKAQce7PziqdPWViWSD1n5cXIIggwlh_SAm50955g='

#Objeto que fornece métodos para criptografar e descriptografar dados usando a chave especificada
f_obj = Fernet(key)

def criptografar(senha):
    #Transforma em bytes
    password_bytes = senha.encode() 
    #Criptografia
    encrypted_pass = f_obj.encrypt(password_bytes)
    return encrypted_pass


def descriptografar(senha):
    #Descriptografia, nesse caso, o parâmetro "senha" deve ser a senha já criptografada
    decrypted_pass = f_obj.decrypt(senha)
    return decrypted_pass
