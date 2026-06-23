FROM python:3.12-slim

WORKDIR /app

# Copia primero los requerimientos para aprovechar la caché de Docker
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación (app.py)
COPY . .

# Expone el puerto interno que usa Flask
EXPOSE 5000

CMD ["python", "app.py"]