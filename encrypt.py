from cryptography.fernet import Fernet

# Define a chave para o processo de criptografia e descriptografia
key = b'pwuKAQce7PziqdPWViWSD1n5cXIIggwlh_SAm50955g='

# Objeto que fornece métodos para criptografar e descriptografar dados
f_obj = Fernet(key)

def criptografar(senha):
    try:
        # Garante que a senha está em bytes
        if isinstance(senha, str):
            password_bytes = senha.encode('utf-8')
        else:
            password_bytes = senha
            
        # Criptografia
        encrypted_pass = f_obj.encrypt(password_bytes)
        # Converte para string para armazenamento
        return encrypted_pass.decode('utf-8')
    except Exception as e:
        print(f"Erro na criptografia: {e}")
        return None

def descriptografar(senha_criptografada):
    try:
        if isinstance(senha_criptografada, str):
            senha_bytes = senha_criptografada.encode('utf-8')
        else:
            senha_bytes = senha_criptografada
            
        # Descriptografia
        decrypted_pass = f_obj.decrypt(senha_bytes)
        # Converte de volta para string
        return decrypted_pass.decode('utf-8')
    except Exception as e:
        print(f"Erro na descriptografia: {e}")
        return None
