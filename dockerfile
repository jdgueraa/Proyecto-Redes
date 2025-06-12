# Usa una imagen de Python liviana
FROM python:3.10-slim

# Crea una carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos de tu proyecto al contenedor
COPY . /app

# Instala las librerías que usa tu simulador
RUN pip install --no-cache-dir matplotlib networkx numpy

# Ejecuta el simulador cuando se inicie el contenedor
CMD ["python", "main.py"]
