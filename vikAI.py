
import tkinter as tk
from tkinter import scrolledtext
import json
import urllib.request
import urllib.error
import threading

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2"


def preguntar_ollama(mensaje):
    datos = {
        "model": MODELO,
        "prompt": mensaje,
        "stream": False
    }

    datos_json = json.dumps(datos).encode("utf-8")

    solicitud = urllib.request.Request(
        OLLAMA_URL,
        data=datos_json,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(solicitud, timeout=120) as respuesta:
            resultado = json.loads(
                respuesta.read().decode("utf-8")
            )
            return resultado.get(
                "response",
                "No recibí una respuesta."
            )

    except urllib.error.URLError:
        return "No pude conectarme con Ollama. Asegúrate de que esté abierto."

    except Exception as e:
        return f"Ocurrió un error: {e}"


def mostrar_respuesta(respuesta):
    chat.config(state="normal")
    chat.insert(tk.END, "VikAI: " + respuesta + "\n\n")
    chat.config(state="disabled")
    chat.see(tk.END)

    boton.config(state="normal")
    entrada.config(state="normal")
    entrada.focus()


def procesar_mensaje(mensaje):
    respuesta = preguntar_ollama(mensaje)
    ventana.after(0, mostrar_respuesta, respuesta)


def enviar_mensaje():
    mensaje = entrada.get().strip()

    if not mensaje:
        return

    chat.config(state="normal")
    chat.insert(tk.END, "Tú: " + mensaje + "\n\n")
    chat.config(state="disabled")
    chat.see(tk.END)

    entrada.delete(0, tk.END)

    boton.config(state="disabled")
    entrada.config(state="disabled")

    hilo = threading.Thread(
        target=procesar_mensaje,
        args=(mensaje,),
        daemon=True
    )
    hilo.start()


ventana = tk.Tk()
ventana.title("VikAI")
ventana.geometry("700x750")
ventana.minsize(500, 600)

encabezado = tk.Frame(ventana)
encabezado.pack(fill="x")

titulo = tk.Label(
    encabezado,
    text="VikAI",
    font=("Arial", 24, "bold")
)
titulo.pack(pady=(15, 0))

subtitulo = tk.Label(
    encabezado,
    text="Tu asistente virtual",
    font=("Arial", 10)
)
subtitulo.pack()

chat = scrolledtext.ScrolledText(
    ventana,
    font=("Arial", 12),
    wrap=tk.WORD,
    state="disabled"
)
chat.pack(
    padx=15,
    pady=15,
    fill="both",
    expand=True
)

zona_entrada = tk.Frame(ventana)
zona_entrada.pack(
    fill="x",
    padx=15,
    pady=(0, 15)
)

entrada = tk.Entry(
    zona_entrada,
    font=("Arial", 12)
)
entrada.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=8
)

boton = tk.Button(
    zona_entrada,
    text="Enviar",
    font=("Arial", 11, "bold"),
    command=enviar_mensaje
)
boton.pack(
    side="right",
    padx=(10, 0),
    ipadx=15,
    ipady=5
)

entrada.bind(
    "<Return>",
    lambda evento: enviar_mensaje()
)

chat.config(state="normal")
chat.insert(
    tk.END,
    "VikAI: ¡Hola! Soy VikAI. ¿En qué puedo ayudarte?\n\n"
)
chat.config(state="disabled")

entrada.focus()

ventana.mainloop()