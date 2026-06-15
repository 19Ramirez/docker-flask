from flask import Flask
import psycopg2
from datetime import datetime

app = Flask(__name__)

VERSION = "1.0.0"

@app.route("/")
def inicio():
    try:
        conexion = psycopg2.connect(
            host="db",
            database="empresa",
            user="admin",
            password="admin123"
        )

        cursor = conexion.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.close()
        conexion.close()

        return f"""
        <h1>Aplicación Flask</h1>
        <h2>Versión {VERSION}</h2>
        <p>Conexión exitosa a PostgreSQL</p>
        <p>{version}</p>
        <h3>Hora actual:</h3>
        <p style="font-size: 24px; font-weight: bold;">{hora_actual}</p>
        """

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)