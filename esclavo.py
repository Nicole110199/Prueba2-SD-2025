import json
from flask import Flask, request, jsonify
import os
from utils import ranking
import datetime
import time
import socket
import Pyro5.api
import threading

# Cargar configuración del esclavo desde variables de entorno
ARCHIVO_DATOS = os.environ.get("ARCHIVO_DATOS", "esclavos/libros.json")
PUERTO = int(os.environ.get("PUERTO", 5001))
RANGO_ETARIO_PATH = os.environ.get("RANGO_ETARIO", "config/rango_etario.json")
INTERESES_PATH = os.environ.get("INTERESES", "config/intereses_por_categoria.json")

# Cargar datos
try:
    with open(ARCHIVO_DATOS, 'r', encoding='utf-8') as f:
        documentos = json.load(f)
    print(f"Datos cargados correctamente desde {ARCHIVO_DATOS}")
except Exception as e:
    print(f"Error al cargar datos: {e}")
    documentos = []  # Usar una lista vacía como fallback

try:
    rangos, intereses = ranking.cargar_configuracion(RANGO_ETARIO_PATH, INTERESES_PATH)
    print("Configuración cargada correctamente")
except Exception as e:
    print(f"Error al cargar configuración: {e}")
    rangos, intereses = {}, {}  # Valores por defecto

# Configurar timeout para Pyro
Pyro5.config.COMMTIMEOUT = 5.0

# Thread-local storage para mantener un proxy por hilo
thread_local = threading.local()

def get_logger_proxy():
    """
    Obtiene un proxy para el logger, creando uno nuevo si no existe
    para el hilo actual.
    """
    if not hasattr(thread_local, 'logger_proxy'):
        thread_local.logger_proxy = Pyro5.api.Proxy("PYRONAME:centralizado.logger")
    return thread_local.logger_proxy

# Servidor Flask
app = Flask(__name__)

@app.route("/query", methods=["GET"])
def query():
    consulta_titulo = request.args.get("titulo", "")
    edad = request.args.get("edad", type=int)
    if edad is None:
        edad = 30  # Valor por defecto
    
    timestamp_ini = datetime.datetime.now().isoformat()
    inicio = time.time()

    try:
        resultados = ranking.aplicar_ranking(documentos, consulta_titulo, edad, rangos, intereses)
    except Exception as e:
        print(f"Error al aplicar ranking: {e}")
        resultados = []

    fin = time.time()
    timestamp_fin = datetime.datetime.now().isoformat()
    tiempo_total = fin - inicio
    score = resultados[0]["score"] if resultados else 0
    rango_etario = f"{edad}"

    # Log al Servidor
    log = {
        "timestamp_ini": timestamp_ini,
        "timestamp_fin": timestamp_fin,
        "maquina": socket.gethostname(),
        "tipo_maquina": "esclavo",
        "query": consulta_titulo,
        "tiempo_fin": round(tiempo_total, 4),
        "score": score,
        "rango_etario": rango_etario
    }
    
    try:
        # Obtener el proxy específico para este hilo
        log_servidor = get_logger_proxy()
        log_servidor.registro(log)  # Llama al método registro con el diccionario log
        print(f"Log enviado al servidor: {log}")
    except Exception as e:
        # Si hay un error con el proxy, limpiarlo para forzar recreación
        if hasattr(thread_local, 'logger_proxy'):
            delattr(thread_local, 'logger_proxy')
        print(f"Error al registrar el log: {e}")
        print(f"Detalles del error: {type(e)}")

    return jsonify(resultados)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Esclavo funcionando correctamente"})

if __name__ == "__main__":
    print(f"Iniciando servidor en puerto {PUERTO}...")
    # Ejecutar sin modo debug
    app.run(host="0.0.0.0", port=PUERTO, debug=False, threaded=True)