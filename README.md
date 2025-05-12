# 📚 Biblioteca Digital Distribuida

Este proyecto implementa tres partes:

- ✅ **Parte 1:** Sistema distribuido con maestro y esclavos para búsqueda de documentos.
- ✅ **Parte 2:** Registro de logs centralizado usando RMI (Pyro5).
- ✅ **Parte 3:** Análisis visual de los logs centralizados mediante gráficos.

---

## 🧠 ¿Qué hace cada parte?

### Parte 1: Búsqueda distribuida
- El maestro recibe una consulta (`titulo`, `edad`).
- Contacta a todos los esclavos (libros, tesis, videos, papers).
- Junta sus respuestas, calcula el score y entrega resultados ordenados.

### Parte 2: Logging centralizado
- Cada nodo (esclavo y maestro) registra la búsqueda: hora, tipo, tiempo, score, grupo etario.
- Los registros se envían a un servidor de logs vía RMI (Pyro5) y se guardan en `logs.csv`.

### Parte 3: Análisis gráfico
- Permite visualizar la información registrada en los logs: distribución etaria, scores, tiempos, etc.

---

## 📦 Archivos de configuración esenciales (`/config`)

| Archivo | Contenido | Para qué sirve |
|--------|-----------|----------------|
| `esclavos_config.json` | Puertos y hosts de cada esclavo | Lo usa el maestro para enrutar consultas |
| `rango_etario.json` | Define rangos como joven, adulto, mayor | Clasifica usuarios según edad |
| `intereses_por_categoria.json` | Puntaje por categoría y edad | Se usa para calcular el `score` |

---

## ✅ PASO 0 – INSTALAR DEPENDENCIAS (una sola vez)

```powershell
pip install flask requests Pyro5 matplotlib pandas seaborn
```

---

## 🔌 PASO 1 – INICIAR SISTEMA DE LOGS (Parte 2)

### 1.1 Servidor de nombres Pyro5

```powershell
python -m Pyro5.nameserver
```

### 1.2 Servidor centralizado de logs

```powershell
python log_sv.py
```

Esto crea y escucha registros en `logs.csv`.

---

## ⚙️ PASO 2 – INICIAR LOS ESCLAVOS (Parte 1)

Abre **una terminal por cada esclavo** y ejecuta lo siguiente:

### Paso 2.1 – Esclavo de libros (puerto 5001)

```powershell
$env:ARCHIVO_DATOS = "esclavos\libros.json"
$env:PUERTO = 5001
python esclavo.py
```

### Paso 2.2 – Esclavo de tesis (puerto 5002)

```powershell
$env:ARCHIVO_DATOS = "esclavos\tesis.json"
$env:PUERTO = 5002
python esclavo.py
```

### Paso 2.3 – Esclavo de videos (puerto 5003)

```powershell
$env:ARCHIVO_DATOS = "esclavos\videos.json"
$env:PUERTO = 5003
python esclavo.py
```

### Paso 2.4 – Esclavo de papers (puerto 5004)

```powershell
$env:ARCHIVO_DATOS = "esclavos\papers.json"
$env:PUERTO = 5004
python esclavo.py
```

---

### 2.5 Iniciar el maestro

```powershell
python maestro.py
```

---

## 🌐 PASO 3 – REALIZAR CONSULTAS (Parte 1 + Parte 2)

Ejecuta consultas desde el navegador como:

```
http://localhost:5000/query?titulo=historia&edad=30
```

✅ Cada consulta será procesada por todos los esclavos y registrada como log en `logs.csv`.

---

## 🧪 PASO 4 – HACER VARIAS CONSULTAS PARA POBLAR LOS LOGS

Realiza al menos 5 consultas variadas como estas:

```
http://localhost:5000/query?titulo=historia&edad=30
http://localhost:5000/query?titulo=inteligencia&edad=65
http://localhost:5000/query?titulo=quimica&edad=20
http://localhost:5000/query?titulo=ficcion&edad=40
http://localhost:5000/query?titulo=programacion&edad=25
```

✅ Esto permitirá tener datos suficientes para los gráficos de la Parte 3.

---

## 📄 PASO 5 – VER LOS LOGS REGISTRADOS (Parte 2)

```powershell
python log_client.py
```

Esto imprimirá las líneas registradas en `logs.csv`.

---

## 📊 PASO 6 – ANALIZAR LOGS CON GRÁFICOS (Parte 3)

```powershell
python aggregate.py
```

Y selecciona una opción:

1. Torta por rango etario  
2. Score promedio en el tiempo  
3. Tiempos de respuesta por esclavo  
4. Latencia red  
5. Tamaño por hora

✅ Estos gráficos solo funcionarán bien si realizaste suficientes consultas antes.

---

## 📂 ESTRUCTURA DEL PROYECTO

```
biblioteca_distribuida/
├── esclavo.py
├── maestro.py
├── log_sv.py
├── log_client.py
├── aggregate.py
├── logs.csv
├── esclavos/
│   ├── libros.json
│   ├── tesis.json
│   ├── videos.json
│   └── papers.json
├── config/
│   ├── esclavos_config.json
│   ├── rango_etario.json
│   └── intereses_por_categoria.json
├── utils/
│   └── ranking.py
├── README.md
└── requirements.txt
```

---
