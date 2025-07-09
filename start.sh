#!/bin/bash

# Ejecutar el simulador con o sin CSV externo
if [ -n "$1" ]; then
  echo "📂 Usando archivo CSV personalizado: $1"
  python main.py "$1"
else
  echo "📂 Usando archivo por defecto: red_isp_peru.csv"
  python main.py
fi

# Luego inicia la galería
echo "🌐 Abriendo servidor de galería (Flask)"
python galeria.py
