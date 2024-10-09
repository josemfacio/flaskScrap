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

        with open("swift_code_result.html", "w", encoding="utf-8") as file:
            file.write(str(soup.prettify()))

        data_items = soup.find_all('dl', class_='_detailsList_5tbr3_1')
        if data_items:
            bank_info = []
            for dl in data_items:
                terms = dl.find_all('dt')
                definitions = dl.find_all('dd')
                for term, definition in zip(terms, definitions):
                    bank_info.append({
                        "term": term.text.strip(),
                        "definition": definition.text.strip()
                    })

            return jsonify({
                "swiftCode": {
                    "swift": code,
                    "info": bank_info,
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
