# Simulador de Red ISP - Perú 🇵🇪

Este proyecto es un simulador educativo desarrollado en Python que modela una red de un proveedor de servicios de Internet (ISP). Utiliza el algoritmo de Dijkstra para encontrar rutas óptimas entre ciudades considerando distintos criterios:

- ⏱️ Latencia (ms)
- 💰 Costo (S/ por MB)
- 📶 Ancho de banda (Mbps)
- ⚖️ Criterio compuesto (balanceado)

## 🎯 Funcionalidades

- Cálculo de la mejor ruta entre dos ciudades.
- Comparación de rutas con distintos criterios.
- Visualización gráfica del grafo de red, con rutas destacadas.
- Análisis estadístico de conectividad por ciudad.
- Interfaz de línea de comandos fácil de usar.

## 📂 Archivos clave

- main.py: código principal del simulador de tráfico en redes ISP.
- red_isp_peru.csv: archivo CSV de ejemplo con la red base del Perú.
- galeria.py: servidor Flask que muestra una galería con las imágenes generadas.
- start.sh: script de arranque que ejecuta automáticamente el simulador con el archivo CSV (personalizado o por defecto) y luego lanza la galería.
- dockerfile: configuración para crear la imagen Docker del simulador.

## 🛠 Requisitos (si ejecutas sin Docker)

- Python 3.8+
- Librerías: `networkx`, `matplotlib`, `numpy`, `flask`

```bash
pip install networkx matplotlib numpy flask
```

## 🚢 Ejecutar el simulador con Docker

### Requisitos:
- Docker instalado (https://www.docker.com/products/docker-desktop)

### 🔁 Opción 1: Usar el archivo CSV por defecto (`red_isp_peru.csv`) | 

a. Comando para windows

```bash
docker pull jdguerraa/simulador-isp:latest
docker run -it -p 80:80 -v %cd%/salidas:/app/salidas jdguerraa/simulador-isp:latest
```
b. Comando para MacOs

```bash
docker pull jdguerraa/simulador-isp:latest
docker run -it -p 80:80 -v "$(pwd)/salidas":/app/salidas jdguerraa/simulador-isp:latest
```

### 🧩 Opción 2: Usar tu propio archivo CSV personalizado y guardar las imagenes en una carpeta "salidas" | (comando para windows)
1. Asegúrate de que tu archivo `.csv` tenga el siguiente formato:
   ```
   ciudad_origen,ciudad_destino,latencia_ms,costo_soles,ancho_banda_mbps
   ```

2. Ejecuta el contenedor montando tu archivo:

```bash
docker run -it -p 80:80 ^
-v %cd%/salidas:/app/salidas ^
-v "RUTA\A\TU\CARPETA:/archivos" ^
simulador-isp:latest bash start.sh /archivos/NOMBRE_DEL_ARCHIVO.csv
```
- Por ejemplo:
  ```bash
   docker run -it -p 80:80 ^
  -v %cd%/salidas:/app/salidas ^
  -v C:\Users\guerr\Downloads:/archivos ^
  jdguerraa/simulador-isp:latest bash start.sh /archivos/ejemplo.csv
```

¡Este simulador es ideal para explorar conceptos de enrutamiento, topología de red y optimización de tráfico de forma práctica y visual! 🚀
