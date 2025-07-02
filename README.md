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

- `main.py`: código principal del simulador.
- `red_isp_peru.csv`: archivo CSV de ejemplo con la red base.
- El simulador también acepta archivos `.csv` personalizados.

## 🛠 Requisitos (si ejecutas sin Docker)

- Python 3.8+
- Librerías: `networkx`, `matplotlib`, `numpy`

```bash
pip install networkx matplotlib numpy
```

## 🚢 Ejecutar el simulador con Docker

### Requisitos:
- Docker instalado (https://www.docker.com/products/docker-desktop)

### 🔁 Opción 1: Usar el archivo CSV por defecto (`red_isp_peru.csv`)

```bash
docker pull jdguerraa/simulador-isp:latest
docker run -it jdguerraa/simulador-isp
```

### 🧩 Opción 2: Usar tu propio archivo CSV personalizado
- Crea tu propia carpeta:
  ```
   mkdir ~/salidas
   ```

1. Asegúrate de que tu archivo `.csv` tenga el siguiente formato:
   ```
   ciudad_origen,ciudad_destino,latencia_ms,costo_soles,ancho_banda_mbps
   ```

2. Ejecuta el contenedor montando tu archivo:

```bash
docker run -it \
  -v "/ruta/completa/a/tu_archivo.csv":/app/mi_red.csv \
  jdguerraa/simulador-isp /app/mi_red.csv

```

## 📷 Ver las imágenes generadas por el simulador

Para que las imágenes del grafo generadas por el simulador se guarden fuera del contenedor:

1. Crea una carpeta local `salidas/`:

```bash
mkdir salidas
```

2. Ejecuta Docker montando esta carpeta:

```bash
docker run -it -v "$(pwd)/salidas":/app/salidas jdguerraa/simulador-isp
```

> También puedes combinar ambas opciones:
```bash
docker run -it \
  -v "/ruta/completa/a/tu_archivo.csv":/app/mi_red.csv \
  -v "/ruta/completa/a/tu_carpeta_salidas":/app/salidas \
  jdguerraa/simulador-isp /app/mi_red.csv

```

---

¡Este simulador es ideal para explorar conceptos de enrutamiento, topología de red y optimización de tráfico de forma práctica y visual! 🚀
