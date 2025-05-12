
# 📚 Biblioteca Digital Distribuida – Manual Completo (Windows PowerShell)

Este proyecto implementa tres partes:

- ✅ **Parte 1:** Sistema distribuido con maestro y esclavos para búsqueda de documentos.
- ✅ **Parte 2:** Registro de logs centralizado usando RMI (Pyro5).
- ✅ **Parte 3:** Análisis visual de los logs centralizados.

---

## ✅ ¿Qué hace cada parte?

### Parte 1: Búsqueda distribuida
- El maestro recibe una consulta (`titulo`, `edad`).
- Consulta a cada esclavo (libros, tesis, videos, papers).
- Junta resultados, calcula el score y ordena.
- Devuelve los documentos más relevantes.

### Parte 2: Logging distribuido
- Cada esclavo y el maestro registran sus operaciones (inicio, fin, tipo, score).
- Envían los registros vía RMI (Pyro5) a un servidor central.
- Los logs se guardan en `logs.csv`.

### Parte 3: Análisis visual
- Se grafican los logs registrados: por grupo etario, tiempos, latencia, tamaño de respuestas, etc.

---

## 📦 Archivos de configuración importantes (carpeta `/config`)

| Archivo | Contenido | Función |
|--------|-----------|---------|
| `esclavos_config.json` | Dirección y puerto de cada esclavo | El maestro usa esto para reenviar consultas |
| `rango_etario.json` | Define rangos de edad (joven, adulto, mayor) | Se usa para clasificar al usuario |
| `intereses_por_categoria.json` | Puntajes por categoría y grupo etario | Se usa para calcular el score |

---

## ⚙️ PASO 0 – INSTALAR DEPENDENCIAS (una sola vez)

En PowerShell dentro de la carpeta del proyecto:

```powershell
pip install flask requests Pyro5 matplotlib pandas seaborn
```

---

## 🔌 PASO 1 – INICIAR EL SISTEMA DE LOGS (Parte 2)

### Paso 1.1 – Iniciar el servidor de nombres Pyro5

```powershell
python -m Pyro5.nameserver
```

Mantén esta terminal abierta.

---

### Paso 1.2 – Iniciar el servidor de logs

En otra terminal:

```powershell
python log_sv.py
```

Esto empezará a recibir y guardar los logs en `logs.csv`.

---

## 🧠 PASO 2 – INICIAR LOS ESCLAVOS (Parte 1)

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

## 🔁 PASO 3 – INICIAR EL MAESTRO

En otra terminal PowerShell:

```powershell
python maestro.py
```

✅ El maestro recibirá las consultas, contactará a los esclavos y devolverá los resultados ordenados.

---

## 🌐 PASO 4 – REALIZAR CONSULTAS DESDE EL NAVEGADOR

Abre tu navegador web y prueba:

```url
http://localhost:5000/query?titulo=historia+futuro&edad=30
```

Puedes cambiar `titulo` y `edad` libremente.

---

## 🧾 PASO 5 – VER LOS LOGS CENTRALIZADOS (Parte 2)

En una nueva terminal PowerShell:

```powershell
python log_client.py
```

Esto te mostrará las entradas en `logs.csv` generadas por esclavos y maestro.

---

## 📊 PASO 6 – VER GRÁFICOS ESTADÍSTICOS (Parte 3)

En otra terminal:

```powershell
python aggregate.py
```

Luego selecciona una opción del menú:

1. Torta por rango etario  
2. Score promedio en el tiempo  
3. Tiempos de respuesta por esclavo  
4. Latencia de red  
5. Tamaño por hora

---

## 🧪 PASO 7 – CONSULTAS DE PRUEBA RECOMENDADAS

Realiza estas consultas desde el navegador para poblar los logs con datos variados:

```
http://localhost:5000/query?titulo=historia&edad=30
http://localhost:5000/query?titulo=inteligencia&edad=65
http://localhost:5000/query?titulo=quimica&edad=20
http://localhost:5000/query?titulo=ficcion&edad=40
http://localhost:5000/query?titulo=programacion&edad=25
```

---

## 📂 ESTRUCTURA ESPERADA DEL PROYECTO

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
