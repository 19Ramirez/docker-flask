from flask import Flask
from datetime import datetime

app = Flask(__name__)

VERSION = "1.0.0"

@app.route("/")
def inicio():
    try:
        # Obtenemos únicamente la hora actual del sistema
        hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return f"""
        <h1>Aplicación Flask</h1>
        <h2>Versión {VERSION}</h2>
        <p>Despliegue exitoso en el servidor de Contabo de forma independiente.</p>
        <h3>Hora actual del servidor:</h3>
        <p style="font-size: 24px; font-weight: bold; color: #2c3e50;">{hora_actual}</p>
        """

    except Exception as e:
        return f"Ha ocurrido un error: {str(e)}"

if __name__ == "__main__":
    # Escuchando en todas las interfaces en el puerto 5000 para Traefik
    app.run(host="0.0.0.0", port=5000)