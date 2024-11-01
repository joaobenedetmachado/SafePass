import requests

def pegarIPCidade():
  res = requests.get("http://ip-api.com/json/")
  if res.status_code == 200:
    dados = res.json()
    return dados["city"]
  else:
    return "Não possivel obter GeoLocalização."
