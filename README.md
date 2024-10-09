# Verificador de Código SWIFT

Esta aplicación es una API creada con Flask que permite verificar códigos SWIFT. Al enviar un código SWIFT, la API realiza una solicitud a un servicio externo y devuelve información relacionada con el banco asociado a dicho código, incluyendo dirección, nombre del banco, país y código de país.

## Características

- Verificación de códigos SWIFT a través de un servicio externo.
- Devolución de detalles del banco, como dirección, nombre, país y código de país.
- Respuesta JSON estructurada, incluso en caso de error.

## Estructura de la respuesta

La API siempre devuelve una respuesta en el siguiente formato:

```json
{
    "swiftCode": {
        "address": "JUNIN Y PANAMA 200",
        "bank": "BANCO BOLIVARIANO C.A.",
        "country": "Ecuador",
        "error": null,
        "message": null,
        "swift": "BBOLECEGXXX",
        "valid": true
    }
}

```

## Ejecución Local

agrega esta linea al final
```
if __name__ == "__main__":
    app.run(debug=True)
```
- cd app
- python index.py

- Abre tu navegador o utiliza herramientas como Postman para enviar solicitudes POST a:
http://127.0.0.1:5000/verificar_swift
- Envía el código SWIFT como parte del formulario en la solicitud POST:
```
{
  "code": "ABCUS33XXX"
}
```

## Requisitos

- Python 3.7 o superior
- Pip (el gestor de paquetes de Python)

