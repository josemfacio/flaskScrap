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
        url = 'https://wise.com/es/swift-codes/bic-swift-code-checker?code='+code

        response = requests.post(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Escribir el contenido de la respuesta en un archivo HTML
        with open("swift_code_result.html", "w", encoding="utf-8") as file:
            file.write(str(soup.prettify()))

        # Buscar todos los elementos de definición (<dl>)
        data_items = soup.find_all('dl', class_='_detailsList_5tbr3_1')
        print(data_items)
        if data_items:
            bank_info = []  # Lista para almacenar la información

            for dl in data_items:
                terms = dl.find_all('dt')
                definitions = dl.find_all('dd')
                for term, definition in zip(terms, definitions):
                    term_text = term.text.strip()
                    definition_text = definition.text.strip()

                    # Añadir término y definición a la lista
                    bank_info.append({
                        "term": term_text,
                        "definition": definition_text
                    })

            # Respuesta en formato JSON
            response_json = {
                "swiftCode": {
                    "swift": code,
                    "info": bank_info,  # Aquí se incluye la lista
                    "valid": True,
                    "message": None,
                    "error": None
                }
            }
            return jsonify(response_json)

        # Respuesta si no se encuentra información
        return jsonify({
            "swiftCode": {
                "swift": None,
                "info": [],  # Lista vacía si no se encontró información
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

if __name__ == '__main__':
    app.run(debug=True)
