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
- `red_isp_peru.csv`: archivo con los datos de la red (ciudad_origen, ciudad_destino, latencia, costo, ancho de banda).


## 🛠 Requisitos

- Python 3.8+
- `networkx`, `matplotlib`, `numpy`

