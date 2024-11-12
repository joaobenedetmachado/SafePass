from zxcvbn import zxcvbn
from translate import Translator

def verificarSenha(password):
    result = zxcvbn(password)
    if result['score'] == 0:
        msg = "Sua senha é muito fraca"
    elif result['score'] == 1:
        msg = "Sua senha é fraca"
    elif result['score'] == 2:
        msg = "Sua senha é média"
    elif result['score'] == 3:
        msg = "Sua senha é forte"
    elif result['score'] == 4:
        msg = "Sua senha é muito forte"

    feedback = result['feedback']
    if feedback['suggestions']:
        suggestions = "\n".join(feedback['suggestions'])
        translator = Translator(to_lang='pt-BR')
        output = translator.translate(suggestions)
        msg += f"\nSugestões: {output}\n"
    return msg