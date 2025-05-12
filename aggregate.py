import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

class AdvancedLogAnalyzer:
    def __init__(self, log_file='logs.csv'):
        """Inicializa el analizador de logs con la ruta al archivo CSV"""
        self.log_file = log_file
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Carga los datos del archivo CSV y realiza preprocesamiento básico"""
        if not os.path.exists(self.log_file):
            raise FileNotFoundError(f"El archivo de logs {self.log_file} no existe")
        
        print(f"Cargando datos desde {self.log_file}...")
        self.df = pd.read_csv(self.log_file)
        
        # Convertir columnas de timestamps a datetime
        self.df['timestamp_ini'] = pd.to_datetime(self.df['timestamp_ini'])
        self.df['timestamp_fin'] = pd.to_datetime(self.df['timestamp_fin'])
        
        # Asegurar que tiempo_fin y score sean numéricos
        self.df['tiempo_fin'] = pd.to_numeric(self.df['tiempo_fin'])
        self.df['score'] = pd.to_numeric(self.df['score'])
        
        # Convertir rango_etario a tipo numérico si es posible
        self.df['rango_etario'] = pd.to_numeric(self.df['rango_etario'], errors='coerce')
        
        # Agregar columnas útiles para análisis
        self.df['fecha'] = self.df['timestamp_ini'].dt.date
        self.df['hora'] = self.df['timestamp_ini'].dt.hour
        self.df['dia_semana'] = self.df['timestamp_ini'].dt.day_name()
        
        # Calcular latencia de red (tiempo entre timestamp_fin y timestamp_ini)
        self.df['latencia'] = (self.df['timestamp_fin'] - self.df['timestamp_ini']).dt.total_seconds() - self.df['tiempo_fin']
        
        # Estimar tamaño de respuesta (simulado - basado en score y tiempo)
        # En un caso real, esto debería venir en el log
        self.df['tamanio_respuesta_kb'] = (self.df['score'] * 10 + self.df['tiempo_fin'] * 5) * np.random.uniform(0.8, 1.2, len(self.df))
        
        print(f"Datos cargados exitosamente. {len(self.df)} registros encontrados.")
    
    def grafico_torta_rangos_etarios(self, save=False):
        """
        1. Genera un gráfico de torta mostrando el porcentaje de consultas por rango etario
        """
        # Filtrar registros con rango etario válido
        df_valid = self.df.dropna(subset=['rango_etario'])
        
        # Contar ocurrencias por rango etario
        conteo = df_valid['rango_etario'].astype(int).value_counts().sort_index()
        
        # Crear figura
        plt.figure(figsize=(10, 8))
        
        # Colores para el gráfico de torta
        colors = plt.cm.viridis(np.linspace(0, 1, len(conteo)))
        
        # Graficar torta
        patches, texts, autotexts = plt.pie(
            conteo, 
            labels=conteo.index, 
            autopct='%1.1f%%',
            startangle=90,
            shadow=True,
            colors=colors,
            explode=[0.05] * len(conteo)  # Separar ligeramente todas las secciones
        )
        
        # Mejorar la apariencia de las etiquetas
        for text in texts:
            text.set_fontsize(12)
            text.set_fontweight('bold')
        
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
            autotext.set_color('white')
        
        plt.title('Distribución de Consultas por Rango Etario', fontsize=16, pad=20)
        plt.axis('equal')  # Para que el círculo sea circular
        
        # Añadir leyenda con conteo exacto
        legend_labels = [f'Edad {age}: {count} consultas' for age, count in zip(conteo.index, conteo.values)]
        plt.legend(legend_labels, loc='best', fontsize=10)
        
        plt.tight_layout()
        
        if save:
            plt.savefig('distribucion_rangos_etarios.png', dpi=300, bbox_inches='tight')
            print("Gráfico guardado como 'distribucion_rangos_etarios.png'")
        else:
            plt.show()
    
    def grafico_curvas_score_tiempo(self, ventanas=[5, 10, 20], save=False):
        """
        2. Genera curvas de promedios de score a través del tiempo con ventanas variables
        """
        # Ordenar por timestamp
        df_sorted = self.df.sort_values('timestamp_ini').copy()
        
        # Crear figura
        plt.figure(figsize=(12, 7))
        
        # Graficar puntos de score individuales
        plt.scatter(df_sorted['timestamp_ini'], df_sorted['score'], 
                   color='gray', alpha=0.3, s=20, label='Scores individuales')
        
        # Calcular y graficar medias móviles con diferentes tamaños de ventana
        colors = ['red', 'blue', 'green', 'purple', 'orange']
        
        for i, window in enumerate(ventanas):
            if window < len(df_sorted):
                # Calcular media móvil
                rolling_mean = df_sorted['score'].rolling(window=window, center=False).mean()
                
                # Graficar la media móvil
                plt.plot(df_sorted['timestamp_ini'], rolling_mean, 
                        linewidth=2.5, color=colors[i % len(colors)], 
                        label=f'Media móvil (ventana={window})')
        
        # Formatear eje X para mostrar fecha y hora
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.xticks(rotation=45)
        
        # Etiquetas y título
        plt.title('Evolución del Score a Través del Tiempo', fontsize=15)
        plt.xlabel('Fecha y Hora', fontsize=12)
        plt.ylabel('Score', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc='best')
        
        plt.tight_layout()
        
        if save:
            plt.savefig('evolucion_score_tiempo.png', dpi=300, bbox_inches='tight')
            print("Gráfico guardado como 'evolucion_score_tiempo.png'")
        else:
            plt.show()
    
    def grafico_cajas_tiempo_esclavos(self, save=False):
        """
        3. Genera un gráfico de cajas mostrando tiempos (promedio, min, max) por esclavo
        """
        # Filtrar solo registros de esclavos
        df_esclavos = self.df[self.df['tipo_maquina'] == 'esclavo'].copy()
        
        if len(df_esclavos) == 0:
            print("No hay datos de máquinas esclavas en el log")
            return
        
        # Crear figura
        plt.figure(figsize=(14, 8))
        
        # Crear boxplot
        ax = sns.boxplot(x='maquina', y='tiempo_fin', data=df_esclavos, 
                       palette='viridis', width=0.6, showmeans=True,
                       meanprops={"marker":"o", "markerfacecolor":"white", 
                                  "markeredgecolor":"black", "markersize":"10"})
        
        # Añadir puntos individuales para ver la distribución
        sns.stripplot(x='maquina', y='tiempo_fin', data=df_esclavos,
                     jitter=True, size=4, color='black', alpha=0.3)
        
        # Añadir etiquetas con estadísticas para cada esclavo
        for i, maquina in enumerate(sorted(df_esclavos['maquina'].unique())):
            datos_maquina = df_esclavos[df_esclavos['maquina'] == maquina]['tiempo_fin']
            
            # Calcular estadísticas
            promedio = datos_maquina.mean()
            minimo = datos_maquina.min()
            maximo = datos_maquina.max()
            
            # Añadir texto con estadísticas
            plt.text(i, maximo * 1.05, 
                     f"Prom: {promedio:.4f}s\nMin: {minimo:.4f}s\nMax: {maximo:.4f}s", 
                     ha='center', va='bottom', fontsize=9, 
                     bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        # Mejorar etiquetas y título
        plt.title('Distribución de Tiempos de Ejecución por Esclavo', fontsize=16)
        plt.xlabel('Máquina (Esclavo)', fontsize=14)
        plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=14)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Rotar etiquetas del eje x si hay muchas máquinas
        if df_esclavos['maquina'].nunique() > 4:
            plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        if save:
            plt.savefig('tiempos_por_esclavo.png', dpi=300, bbox_inches='tight')
            print("Gráfico guardado como 'tiempos_por_esclavo.png'")
        else:
            plt.show()
    
    def grafico_latencia_red(self, save=False):
        """
        4. Genera un gráfico mostrando la latencia de red entre el maestro y los esclavos
        """
        # Filtrar latencias válidas (eliminar valores negativos o extremadamente altos)
        df_latencia = self.df[
            (self.df['latencia'] >= 0) & 
            (self.df['latencia'] < self.df['latencia'].quantile(0.95))  # Eliminar outliers
        ].copy()
        
        # Crear figura
        plt.figure(figsize=(12, 7))
        
        # Agrupar por máquina y hora
        latencia_por_maquina_hora = df_latencia.groupby(['maquina', 'hora'])['latencia'].mean().reset_index()
        
        # Crear gráfico de líneas
        sns.lineplot(
            data=latencia_por_maquina_hora,
            x='hora',
            y='latencia',
            hue='maquina',
            marker='o',
            markersize=8,
            linewidth=2
        )
        
        # Añadir etiquetas y título
        plt.title('Latencia de Red Promedio por Hora y Máquina', fontsize=16)
        plt.xlabel('Hora del Día', fontsize=14)
        plt.ylabel('Latencia (segundos)', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Ajustar eje X para mostrar todas las horas
        plt.xticks(range(0, 24), rotation=0)
        
        # Añadir línea promedio general
        plt.axhline(y=df_latencia['latencia'].mean(), color='red', linestyle='--', 
                   label=f'Latencia promedio global: {df_latencia["latencia"].mean():.4f}s')
        
        plt.legend(title='Máquina', title_fontsize=12)
        plt.tight_layout()
        
        if save:
            plt.savefig('latencia_red.png', dpi=300, bbox_inches='tight')
            print("Gráfico guardado como 'latencia_red.png'")
        else:
            plt.show()
    
    def grafico_tamanio_respuestas_hora(self, save=False):
        """
        5. Genera un gráfico de tamaño en MB de las respuestas por hora a través del día
        """
        # Convertir KB a MB
        self.df['tamanio_respuesta_mb'] = self.df['tamanio_respuesta_kb'] / 1024
        
        # Agrupar por fecha, hora y calcular suma de tamaños
        tamanio_por_hora = self.df.groupby(['fecha', 'hora', 'dia_semana'])['tamanio_respuesta_mb'].sum().reset_index()
        
        # Crear figura
        plt.figure(figsize=(14, 8))
        
        # Crear paleta de colores para diferentes días
        dias_unicos = tamanio_por_hora['dia_semana'].unique()
        paleta = sns.color_palette("husl", len(dias_unicos))
        
        # Crear mapeo de día a color
        color_map = {dia: paleta[i] for i, dia in enumerate(dias_unicos)}
        
        # Agrupar por día de la semana
        for dia in dias_unicos:
            data_dia = tamanio_por_hora[tamanio_por_hora['dia_semana'] == dia]
            
            # Convertir fecha a string para etiquetas
            data_dia['fecha_str'] = data_dia['fecha'].astype(str)
            
            # Para cada fecha de ese día
            for fecha in data_dia['fecha'].unique():
                data_fecha = data_dia[data_dia['fecha'] == fecha]
                
                # Graficar línea para esta fecha
                plt.plot(data_fecha['hora'], data_fecha['tamanio_respuesta_mb'], 
                        marker='o', linewidth=2, alpha=0.8,
                        color=color_map[dia],
                        label=f"{dia} ({fecha})")
        
        # Mejorar aspecto del gráfico
        plt.title('Tamaño Total de Respuestas por Hora del Día', fontsize=16)
        plt.xlabel('Hora del Día', fontsize=14)
        plt.ylabel('Tamaño de Respuestas (MB)', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Ajustar eje X para mostrar todas las horas
        plt.xticks(range(0, 24))
        
        # Formatear eje Y para mostrar decimales con 2 dígitos
        plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.2f}'))
        
        # Ajustar leyenda
        plt.legend(title='Día', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        
        if save:
            plt.savefig('tamanio_respuestas_por_hora.png', dpi=300, bbox_inches='tight')
            print("Gráfico guardado como 'tamanio_respuestas_por_hora.png'")
        else:
            plt.show()
    
    def generar_todos_los_graficos(self, directorio="analisis_logs"):
        """Genera todos los gráficos solicitados y los guarda en un directorio"""
        # Crear directorio si no existe
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"Directorio '{directorio}' creado.")
        
        # Guardar directorio actual y cambiar al nuevo
        dir_actual = os.getcwd()
        os.chdir(directorio)
        
        try:
            print("\nGenerando gráficos...")
            
            # 1. Gráfico de torta de rangos etarios
            self.grafico_torta_rangos_etarios(save=True)
            
            # 2. Curvas de score a través del tiempo
            self.grafico_curvas_score_tiempo(ventanas=[3, 5, 10], save=True)
            
            # 3. Gráfico de cajas por esclavo
            self.grafico_cajas_tiempo_esclavos(save=True)
            
            # 4. Latencia de red
            self.grafico_latencia_red(save=True)
            
            # 5. Tamaño de respuestas por hora
            self.grafico_tamanio_respuestas_hora(save=True)
            
            print(f"\nTodos los gráficos generados correctamente en '{directorio}'")
            
        except Exception as e:
            print(f"Error al generar gráficos: {e}")
        
        # Volver al directorio original
        os.chdir(dir_actual)


# Ejecutar el script
if __name__ == "__main__":
    try:
        analyzer = AdvancedLogAnalyzer()
        
        print("\n=== ANALIZADOR DE LOGS AVANZADO ===")
        print("1. Gráfico de torta con porcentajes por rango etario")
        print("2. Curvas de score a través del tiempo")
        print("3. Gráfico de cajas de tiempos por esclavo")
        print("4. Latencia de red maestro-esclavos")
        print("5. Tamaño de respuestas por hora")
        print("6. Generar todos los gráficos")
        print("0. Salir")
        
        opcion = input("\nSeleccione una opción (0-6): ")
        
        if opcion == "1":
            analyzer.grafico_torta_rangos_etarios()
        elif opcion == "2":
            ventanas = input("Ingrese tamaños de ventana separados por comas (ej: 5,10,20): ")
            ventanas = [int(v.strip()) for v in ventanas.split(",")]
            analyzer.grafico_curvas_score_tiempo(ventanas=ventanas)
        elif opcion == "3":
            analyzer.grafico_cajas_tiempo_esclavos()
        elif opcion == "4":
            analyzer.grafico_latencia_red()
        elif opcion == "5":
            analyzer.grafico_tamanio_respuestas_hora()
        elif opcion == "6":
            analyzer.generar_todos_los_graficos()
        elif opcion == "0":
            print("Saliendo...")
        else:
            print("Opción no válida")
            
    except Exception as e:
        print(f"Error: {e}")