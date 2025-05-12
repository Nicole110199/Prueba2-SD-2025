import Pyro5.api
import threading
import datetime
import copy
import csv
import os

@Pyro5.api.expose
class entradaLog:
    def __init__(self, timestamp_ini, timestamp_fin, maquina, tipo_maquina, query, tiempo_fin, score, rango_etario):
        self.timestamp_ini = timestamp_ini
        self.timestamp_fin = timestamp_fin
        self.maquina = maquina
        self.tipo_maquina = tipo_maquina
        self.query = query
        self.tiempo_fin = tiempo_fin
        self.score = score
        self.rango_etario = rango_etario

    def __str__(self):
        return f'{self.timestamp_ini}, {self.timestamp_fin}, {self.maquina}, {self.tipo_maquina}, {self.query}, {self.tiempo_fin}, {self.score}, {self.rango_etario}'
    
    def to_dict(self):
        """Convierte el objeto a un diccionario para facilitar la escritura en CSV"""
        return {
            'timestamp_ini': self.timestamp_ini,
            'timestamp_fin': self.timestamp_fin,
            'maquina': self.maquina,
            'tipo_maquina': self.tipo_maquina,
            'query': self.query,
            'tiempo_fin': self.tiempo_fin,
            'score': self.score,
            'rango_etario': self.rango_etario
        }

@Pyro5.api.expose
class logCentralizado:
    def __init__(self):
        self.logs = []
        self.lock = threading.Lock()
        self.log_file = "logs.csv"
        
        # Comprobar si el archivo existe, si no, crear con encabezados
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['timestamp_ini', 'timestamp_fin', 'maquina', 'tipo_maquina', 
                              'query', 'tiempo_fin', 'score', 'rango_etario']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
            print(f"Archivo de logs creado: {self.log_file}")
    
    def save_to_file(self, log_entry):
        """Guarda una entrada de log en el archivo CSV"""
        log_dict = log_entry.to_dict()
        with open(self.log_file, 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['timestamp_ini', 'timestamp_fin', 'maquina', 'tipo_maquina', 
                          'query', 'tiempo_fin', 'score', 'rango_etario']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(log_dict)
    
    def registro(self, entrada_log):
        # Hacer una copia profunda del diccionario de entrada
        log_copy = copy.deepcopy(entrada_log)
        
        # Crear una instancia separada de entradaLog para cada registro
        entrada = entradaLog(
            timestamp_ini=log_copy["timestamp_ini"],
            timestamp_fin=log_copy["timestamp_fin"],
            maquina=log_copy["maquina"],
            tipo_maquina=log_copy["tipo_maquina"],
            query=log_copy["query"],
            tiempo_fin=log_copy["tiempo_fin"],
            score=log_copy["score"],
            rango_etario=log_copy["rango_etario"]
        )
        
        with self.lock:
            # Agregar el nuevo log a la lista en memoria
            self.logs.append(entrada)
            
            # Guardar el log en el archivo
            try:
                self.save_to_file(entrada)
                print(f'Log registrado y guardado en archivo: {entrada.maquina} - {entrada.timestamp_ini}')
            except Exception as e:
                print(f'Error al guardar log en archivo: {e}')
    
    def lectura(self):
        with self.lock:
            # Convertir cada objeto entradaLog a string para la serialización
            return [str(log) for log in self.logs]
    
    def get_logs(self):
        # Redirigir a lectura() para mantener consistencia
        return self.lectura()
    
    def leer_archivo_logs(self):
        """Lee todos los logs del archivo CSV y los devuelve como una lista de diccionarios"""
        if not os.path.exists(self.log_file):
            return []
        
        logs = []
        with open(self.log_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                logs.append(row)
        return logs

def main():
    # Configurar Pyro para esperar a que terminen todas las solicitudes
    Pyro5.config.COMMTIMEOUT = 5.0
    Pyro5.config.SERVERTYPE = "thread"
    
    daemon = Pyro5.api.Daemon()
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(logCentralizado)
    ns.register('centralizado.logger', uri)
    print('Servidor de logs centralizados iniciado')
    print(f"URI: {uri}")
    print(f"Logs se guardarán en: {os.path.abspath('logs.csv')}")
    daemon.requestLoop()

if __name__ == "__main__":
    main()