import unicodedata

from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)

CORS(app, resources={r"/imprimir": {"origins": ["https://pontofacil-web.vercel.app", "http://localhost:5173"]}})

def send_command(printer, cmd: bytes):
    printer.write(cmd)
    printer.flush()
    time.sleep(0.1)

def remover_acentos(texto: str) -> str:
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

@app.route('/imprimir', methods=['POST'])
def imprimir():
    data = request.json
    print(f"Recebido: {data}")
    texto = data.get('texto', '')

    try:
        texto_normalizado = remover_acentos(texto)
        print(f"Texto normalizado: {texto_normalizado}")

        encoded_text = texto_normalizado.encode('latin1')
        print(f"Texto codificado: {encoded_text}")

        with open("/dev/usb/lp0", "wb") as printer:
            send_command(printer, encoded_text)
            send_command(printer, b"\n\n")
            send_command(printer, b"\x1D\x56\x00")

        return jsonify({"status": "sucesso", "mensagem": "Impressão realizada com sucesso!"}), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
