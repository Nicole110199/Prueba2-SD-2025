
import json
import requests
from flask import Flask, request, jsonify
import os

# Cargar configuración de esclavos
with open("config/esclavos_config.json", "r", encoding="utf-8") as f:
    esclavos = json.load(f)

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor maestro en funcionamiento. Usa /query para consultas."

@app.route("/query", methods=["GET"])
def query():
    consulta_titulo = request.args.get("titulo", "")
    edad = request.args.get("edad", type=int)
    tipos = request.args.get("tipo_doc", "")

    resultados_totales = []

    if tipos:
        tipos_requeridos = [t.strip() for t in tipos.split("+") if t.strip()]
    else:
        tipos_requeridos = list(esclavos.keys())

    for tipo in tipos_requeridos:
        esclavo = esclavos.get(tipo)
        if esclavo:
            url = f"http://{esclavo['host']}:{esclavo['port']}/query"
            try:
                params = {"titulo": consulta_titulo}
                if edad is not None:
                    params["edad"] = edad
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    resultados = response.json()
                    for item in resultados:
                        doc = item["documento"]
                        doc["score"] = item["score"]
                        doc["coincidencias_titulo"] = item["coincidencias_titulo"]
                        doc["puntaje_categoria"] = item["puntaje_categoria"]
                        doc["tipo"] = tipo
                        resultados_totales.append(doc)
            except requests.exceptions.RequestException as e:
                print(f"Error consultando al esclavo {tipo}: {e}")

    # ORDENAR por score de mayor a menor
    resultados_totales.sort(key=lambda doc: doc["score"], reverse=True)

    return jsonify(resultados_totales)

if __name__ == "__main__":
    app.run(port=5000)
