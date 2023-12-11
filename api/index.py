from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/verificar_swift', methods=['POST'])
def verificar_swift():
    try:
        # Datos del formulario
        code = request.form.get('code', '')

        # URL de la página
        url = 'https://wise.com/es/swift-codes/bic-swift-code-checker'

        # Datos para la solicitud POST
        payload = {'code': code}

        response = requests.post(url, data=payload)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar la etiqueta <p> con la clase específica
        data_paragraph = soup.find('p', class_='visible-xs visible-sm')
        # Verificar si se encontró la etiqueta
        if data_paragraph:
            # Extraer datos específicos dentro de la etiqueta <span>
            spans = data_paragraph.find_all('span')
            # Construir lista de datos recuperados
            response_json = {
                "swiftCode": {
                    "swift": code,
                    "country": spans[3].text,
                    "countrycode": code[4:6],
                    "bank": spans[0].text,
                    "address": spans[1].text,
                    "valid": True,
                    "message": None,
                    "error": None
                }
            }
            return jsonify(response_json)

        return jsonify({
            "swiftCode": {
                "swift": None,
                "country": None,
                "countrycode": None,
                "bank": None,
                "address": None,
                "valid": False,
                "message": "No encontramos tu código, por favor a continuación escribe los datos del banco del beneficiario.",
                "error": "1013"
            }
        }), 400

    except requests.exceptions.RequestException as e:
        # Manejar error de solicitud
        return jsonify({
            "swiftCode": {
                "swift": None,
                "country": None,
                "countrycode": None,
                "bank": None,
                "address": None,
                "valid": False,
                "message": f"Error al intentar buscar {e}",
                "error": "1012"
            }
        }), 400     

    except Exception as e:
        # Manejar otros errores
        return jsonify({
            "swiftCode": {
                "swift": None,
                "country": None,
                "countrycode": None,
                "bank": None,
                "address": None,
                "valid": False,
                "message": f"Error desconocido {e}",
                "error": "1012"
            }
        }), 500 

if __name__ == '__main__':
    app.run(debug=True)
