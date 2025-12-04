import requests
base_url = "https://cl.dolarapi.com"
respuesta = requests.get(url=f"{base_url}/v1/cotizaciones/usd")
codigo_respuesta = respuesta.status_code
try:
        data = respuesta.json
        print(data)
except:
        print(respuesta)