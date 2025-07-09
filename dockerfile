# Usa una imagen base liviana de Python 3.10
FROM python:3.10-slim

# Establece la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos del proyecto al contenedor
COPY . /app

# Copia el logo de la universidad
COPY static/logo_ulima.png /app/static/logo_ulima.png

# Crea la carpeta para imágenes generadas
RUN mkdir -p /app/salidas

# Instala las dependencias necesarias para tu simulador
RUN pip install --no-cache-dir matplotlib networkx numpy flask

# Copia el script de inicio y dale permisos de ejecución
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expone el puerto 80 para servir contenido web
EXPOSE 80

# Comando por defecto: ejecuta simulador y luego galería
CMD ["bash", "start.sh"]
