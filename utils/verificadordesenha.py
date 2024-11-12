from zxcvbn import zxcvbn

password = input("Enter your password: ")

def verificarSenha(password):
    result = zxcvbn(password)
    if result['score'] == 0:
        msg = "Password is very weak"
    elif result['score'] == 1:
        msg = "Password is weak"
    elif result['score'] == 2:
        msg = "Password is medium"
    elif result['score'] == 3:
        msg = "Password is strong"
    elif result['score'] == 4:
        msg = "Password is very strong"
    return msg
