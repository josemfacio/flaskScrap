from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/verificar_swift', methods=['POST'])
def verificar_swift():
    try:
        code = request.form.get('code', '')

        url = f'https://wise.com/es/swift-codes/bic-swift-code-checker?code={code}'
        response = requests.post(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')


        data_items = soup.find_all('dl', class_='_detailsList_5tbr3_1')
        if data_items:
            bank_info = []
            address = ""
            bank = ""
            country = ""
            for dl in data_items:
                terms = dl.find_all('dt')
                definitions = dl.find_all('dd')
                for term, definition in zip(terms, definitions):
                    term_text = term.text.strip().lower()
                    definition_text = definition.text.strip()
                    # Asignar valores manualmente en base a los términos específicos
                    if "dirección del banco" in term_text:
                        address = definition_text
                    elif "nombre del banco" in term_text:
                        bank = definition_text
                    elif "país" in term_text:
                        country = definition_text
            return jsonify({
            "swiftCode": {
                "swift": code,
                "address": address,
                "bank": bank,
                "country": country,
                "valid": True,
                "message": None,
                "error": None
            }
        })

        return jsonify({
            "swiftCode": {
                "swift": None,
                "info": [],
                "valid": False,
                "message": "No encontramos tu código, por favor a continuación escribe los datos del banco del beneficiario.",
                "error": "1013"
            }
        }), 400

    except requests.exceptions.RequestException as e:
        return jsonify({
            "swiftCode": {
                "swift": None,
                "info": [],
                "valid": False,
                "message": f"Error al intentar buscar {e}",
                "error": "1012"
            }
        }), 400

    except Exception as e:
        return jsonify({
            "swiftCode": {
                "swift": None,
                "info": [],
                "valid": False,
                "message": f"Error desconocido {e}",
                "error": "1012"
            }
        }), 500