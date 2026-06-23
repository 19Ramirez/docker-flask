from flask import Flask, render_template_string, request
from datetime import datetime

app = Flask(__name__)

VERSION = "1.2.0"

# Diseño en HTML/CSS para una calculadora moderna y limpia
TEMPLATE_CALCULADORA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora DevOps</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f6f9;
            margin: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 350px;
        }
        h1 { color: #2c3e50; margin-bottom: 5px; font-size: 26px; }
        h2 { color: #7f8c8d; font-size: 14px; margin-top: 0; margin-bottom: 25px; }
        input[type="number"], select {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 16px;
        }
        button {
            width: 100%;
            background-color: #3498db;
            color: white;
            padding: 12px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.2s;
        }
        button:hover { background-color: #2980b9; }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #e8f4fd;
            border-radius: 6px;
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        }
        footer {
            margin-top: 20px;
            font-size: 11px;
            color: #bdc3c7;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>🧮 DevOps Calc</h1>
    <h2>Servidor Contabo | Versión {{ version }}</h2>
    
    <form method="POST">
        <input type="number" step="any" name="num1" placeholder="Primer número" value="{{ num1 }}" required>
        
        <select name="operacion">
            <option value="suma" {% if operacion == 'suma' %}selected{% endif %}>➕ Sumar</option>
            <option value="resta" {% if operacion == 'resta' %}selected{% endif %}>➖ Restar</option>
            <option value="multi" {% if operacion == 'multi' %}selected{% endif %}>✖️ Multiplicar</option>
            <option value="div" {% if operacion == 'div' %}selected{% endif %}>➗ Dividir</option>
        </select>
        
        <input type="number" step="any" name="num2" placeholder="Segundo número" value="{{ num2 }}" required>
        
        <button type="submit">Calcular</button>
    </form>

    {% if resultado is not none %}
    <div class="result">
        Resultado: {{ resultado }}
    </div>
    {% endif %}

    <footer>
        Hora del servidor: {{ hora }}<br>
        Desplegado de forma independiente mediante Docker Swarm
    </footer>
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def calculadora():
    resultado = None
    num1 = ""
    num2 = ""
    operacion = "suma"
    
    if request.method == "POST":
        try:
            num1 = float(request.form.get("num1"))
            num2 = float(request.form.get("num2"))
            operacion = request.form.get("operacion")
            
            if operacion == "suma":
                resultado = num1 + num2
            elif operacion == "resta":
                resultado = num1 - num2
            elif operacion == "multi":
                resultado = num1 * num2
            elif operacion == "div":
                resultado = num1 / num2 if num2 != 0 else "Error: División por cero"
                
            # Formatear el resultado si es entero
            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)
        except Exception as e:
            resultado = f"Error en los datos: {str(e)}"

    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return render_template_string(
        TEMPLATE_CALCULADORA,
        version=VERSION,
        hora=hora_actual,
        resultado=resultado,
        num1=num1,
        num2=num2,
        operacion=operacion
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)