from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2"


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    datos = request.get_json()
    mensaje = datos.get("mensaje", "").strip()

    if not mensaje:
        return jsonify({"respuesta": "Escribe un mensaje."})

    try:
        respuesta = requests.post(
            OLLAMA_URL,
            json={
                "model": MODELO,
                "prompt": mensaje,
                "stream": False
            },
            timeout=120
        )

        resultado = respuesta.json()

        return jsonify({
            "respuesta": resultado.get(
                "response",
                "No recibí una respuesta."
            )
        })

    except Exception:
        return jsonify({
            "respuesta": "No pude conectarme con el servidor de IA."
        })


if __name__ == "__main__":
    app.run(debug=True)