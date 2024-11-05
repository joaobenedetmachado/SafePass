import requests

def pegarIPCidade(): 
  res = requests.get("http://ip-api.com/json/") # manda um GET pra essa api que pega o teu ip e infos dele
  if res.status_code == 200: # se der certo ele retornara o [city]
    dados = res.json()
    return dados["city"]
  else: # se nao, da erro
    return "Não possivel obter GeoLocalização."
