from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
@app.route('/')
def home():
    return 'Hello, World!'
    
@app.route('/verificar_swift', methods=['POST'])
def verificar_swift():
    try:
        # Obtener el código SWIFT desde el formulario
        code = request.form.get('code', '')

        # URL de la página que verificará el código SWIFT
        url = f'https://wise.com/es/swift-codes/bic-swift-code-checker?code={code}'

        # Realizar la petición HTTP
        response = requests.post(url)
        response.raise_for_status()

        # Parsear el HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Inicializar la estructura de la respuesta
        response_json = {
            "swiftCode": {
                "address": "",
                "bank": "",
                "country": "",
                "countrycode": "",
                "error": "",
                "message": "",
                "swift": code,
                "valid": False
            }
        }

        # Extraer los elementos de información (por ejemplo, address, bank, country)
        data_items = soup.find_all('dl', class_='_detailsList_5tbr3_1')
        if data_items:
            bank_info = {}  # Diccionario para almacenar la información

            for dl in data_items:
                terms = dl.find_all('dt')
                definitions = dl.find_all('dd')
                for term, definition in zip(terms, definitions):
                    term_text = term.text.strip().lower()

                    # Comprobar qué campo es y asignarlo a la estructura de la respuesta
                    if "address" in term_text:
                        bank_info["address"] = definition.text.strip()
                    elif "bank" in term_text:
                        bank_info["bank"] = definition.text.strip()
                    elif "country" in term_text:
                        bank_info["country"] = definition.text.strip()
                    elif "country code" in term_text:
                        bank_info["countrycode"] = definition.text.strip()

            # Actualizar la estructura de la respuesta con los datos encontrados
            response_json["swiftCode"].update({
                "address": bank_info.get("address", ""),
                "bank": bank_info.get("bank", ""),
                "country": bank_info.get("country", ""),
                "countrycode": bank_info.get("countrycode", ""),
                "valid": True,
                "message": None,
                "error": None
            })

        else:
            # Si no se encuentra información sobre el código SWIFT, enviar un mensaje de error
            response_json["swiftCode"]["message"] = "No encontramos tu código, por favor verifica el código SWIFT."
            response_json["swiftCode"]["error"] = "1013"

        return jsonify(response_json)

    except requests.exceptions.RequestException as e:
        # Error de la petición HTTP
        return jsonify({
            "swiftCode": {
                "address": "",
                "bank": "",
                "country": "",
                "countrycode": "",
                "error": "1012",
                "message": f"Error al intentar buscar {e}",
                "swift": None,
                "valid": False
            }
        }), 400

    except Exception as e:
        # Error general
        return jsonify({
            "swiftCode": {
                "address": "",
                "bank": "",
                "country": "",
                "countrycode": "",
                "error": "1012",
                "message": f"Error desconocido: {e}",
                "swift": None,
                "valid": False
            }
        }), 500
