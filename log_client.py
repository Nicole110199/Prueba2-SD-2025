import Pyro5.api
import sys
import time

def obtener_logs():
    try:
        # Configurar el tiempo de espera para Pyro
        Pyro5.config.COMMTIMEOUT = 5.0  # 5 segundos de timeout
        
        print("Conectando al servidor de logs...")
        logger = Pyro5.api.Proxy("PYRONAME:centralizado.logger")
        
        # Verificar la conexión
        try:
            print("Obteniendo logs del servidor...")
            logs = logger.lectura()
            
            if logs:
                print("\nLista de logs del servidor:")
                for i, log in enumerate(logs):
                    print(f"{i+1}: {log}")
                print(f"\nTotal de logs encontrados: {len(logs)}")
            else:
                print("No hay logs registrados en el servidor.")
                
        except Exception as e:
            print(f"Error al obtener logs: {e}")
            
    except Pyro5.errors.NamingError:
        print("No se encontró el servidor de logs centralizado.")
        print("Asegúrate de que el servidor de nombres de Pyro esté en ejecución.")
        
    except Pyro5.errors.CommunicationError as e:
        print(f"Error de comunicación con el servidor: {e}")
        print("Verifica que el servidor de logs esté en ejecución.")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        print(f"Tipo de error: {type(e)}")

if __name__ == "__main__":
    obtener_logs()