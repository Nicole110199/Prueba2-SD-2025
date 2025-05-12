
# 📚 Biblioteca Digital Distribuida – Prueba 2 Sistemas Distribuidos 2025-01

Este repositorio contiene el desarrollo completo de la **Prueba 2** de Sistemas Distribuidos.  
Está dividido en tres partes funcionales:

- ✅ **Parte 1:** Sistema distribuido de búsqueda (maestro + esclavos).
- ✅ **Parte 2:** Registro de logs centralizado usando Pyro5 (estilo RMI).
- ✅ **Parte 3:** Visualización de estadísticas desde los logs mediante gráficos.

---

## 🧾 ¿Qué contiene este repositorio?

Estructura después de descomprimir:

```
Prueba2-SD-2025-main/
├── esclavo.py                 
├── maestro.py                
├── log_sv.py                
├── aggregate.py              
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

## 📥 PASO 0 – DESCARGAR Y DESCOMPRIMIR

1. Descarga el repositorio como ZIP desde GitHub o tu plataforma:
   - Archivo: `Prueba2-SD-2025-main.zip`

2. Extrae el contenido. Al hacerlo obtendrás la carpeta:
   - `Prueba2-SD-2025-main/`

3. Abre PowerShell en esa carpeta:
   - Puedes hacer clic derecho en la carpeta extraída y elegir “Abrir en Terminal”.

---

## ✅ PASO 1 – INSTALAR DEPENDENCIAS (una sola vez)

Abre **una nueva terminal** y ejecuta lo siguiente:

```powershell
pip install flask requests Pyro5 matplotlib pandas seaborn
```

---

## 🔌 PASO 2 – INICIAR SISTEMA DE LOGS (Parte 2)

### 2.1 Servidor de nombres Pyro5

```powershell
python -m Pyro5.nameserver
```

### 2.2 Servidor de logs

Abre **una nueva terminal** y ejecuta lo siguiente:

```powershell
python log_sv.py
```

---

## ⚙️ PASO 3 – INICIAR LOS ESCLAVOS (Parte 1)

Abre **una terminal por cada esclavo** y ejecuta lo siguiente:

### Paso 3.1 – Esclavo de libros (puerto 5001)

```powershell
$env:ARCHIVO_DATOS = "esclavos\libros.json"
$env:PUERTO = 5001
python esclavo.py
```

### Paso 3.2 – Esclavo de tesis (puerto 5002)

```powershell
$env:ARCHIVO_DATOS = "esclavos\tesis.json"
$env:PUERTO = 5002
python esclavo.py
```

### Paso 3.3 – Esclavo de videos (puerto 5003)

```powershell
$env:ARCHIVO_DATOS = "esclavos\videos.json"
$env:PUERTO = 5003
python esclavo.py
```

### Paso 3.4 – Esclavo de papers (puerto 5004)

```powershell
$env:ARCHIVO_DATOS = "esclavos\papers.json"
$env:PUERTO = 5004
python esclavo.py
```

---

## 🚦 PASO 4 – INICIAR EL MAESTRO
Abre **una nueva terminal para el maestro** y ejecuta lo siguiente:
```powershell
python maestro.py
```

---

## 🌐 PASO 5 – REALIZAR CONSULTAS

Abre tu navegador:

```
http://localhost:5000/query?titulo=historia+codigo&edad=30
```

✅ El maestro envía la consulta a todos los esclavos, calcula el score y registra el log.

---

## 🧪 PASO 6 – HACER VARIAS CONSULTAS PARA QUE LOS GRÁFICOS FUNCIONEN

Ejecuta al menos 5 consultas diferentes como:

```
http://localhost:5000/query?titulo=historia+codigo&edad=30
http://localhost:5000/query?titulo=tecnologia+programacion&edad=25
http://localhost:5000/query?titulo=origen&edad=25
http://localhost:5000/query?titulo=descubrimiento+del+futuro&edad=20
http://localhost:5000/query?titulo=ficcion+leyenda&edad=35
http://localhost:5000/query?titulo=origen&edad=60
http://localhost:5000/query?titulo=descubrimiento+del+futuro&edad=45

```

---

## 📊 PASO 7 – VER GRÁFICOS ESTADÍSTICOS (Parte 3)

Abre **una nueva terminal** y ejecuta lo siguiente:

```powershell
python aggregate.py
```

Selecciona una opción del menú:

1. Torta por rango etario  
2. Score promedio en el tiempo  
3. Tiempos por esclavo  
4. Latencia red  
5. Tamaño por hora

---

## 🗂️ ARCHIVOS DE CONFIGURACIÓN (carpeta `config/`)

- `esclavos_config.json`: define puertos y hosts de los esclavos.
- `rango_etario.json`: traduce edad a grupo etario.
- `intereses_por_categoria.json`: peso por grupo etario y categoría (usado en el score).

---

## 📁 Nota Final

Los logs de las consultas se almacenan automáticamente en `logs.csv`.

---
