from flask import Blueprint, request, jsonify
from app.services.openai_service import process_openai_message
from app.services.whatsapp_service import send_whatsapp_message
from datetime import datetime
import numpy as np
from io import StringIO

main_blueprint = Blueprint("main", __name__)

user_message_count = {}

@main_blueprint.route('/endpoint', methods=['POST'])
def handle_post_request():
    data = request.get_json()
    telefono = data.get("telefono")
    mensaje = data.get("mensaje")
    #timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Procesar mensaje con OpenAI


    if telefono not in user_message_count:
        conversation_history = [{
            "role":
            "assistant",
            "content":
            "Crees que en el siguiente mensaje: " + mensaje +
            " contiene respuestas de las siguiente informacion: 1. Nombre y Apellido del invitado ||| 2. Preferencia Alimentaria siendo: 1 - celiaco; 2 - diabetico; 3 - vegetariano; 4 - vegano; 5 - Sin preferencia ||| 3. Si confirma a alguien más ||| contestame únicamente un texto con (en este orden): + número de pregunta este la informacion o no (1,2 o 3) // + '1' si estás 100% seguro que con la respuesta del usuario se le puede dar una respuesta a esa pregunta o '0' // + y que estes seguro de la respuesta cual es || ejemplo de output: 1, Si, Emilio Ferrero; 2, No, NA; 3, No, NA;"
        }]
        
        pre_respuestas, conversation_history = process_openai_message(conversation_history)
        print(conversation_history)
        print(pre_respuestas)
        csv_data = StringIO(pre_respuestas.replace(";", "\n"))
        pre_respuestas = np.genfromtxt(csv_data, delimiter=",", dtype=str)
        user_message_count[telefono] = 0
        if pre_respuestas[0, 1] == " No":
            user_message_count[telefono] += 1
            return jsonify({
                "pregunta": "Muchas gracias por tomarte estos minutos para hacer la confirmación a la fiesta de Pupe!..."
            })

    elif user_message_count[telefono] == 1:
        if pre_respuestas[1, 1] == "No":
            user_message_count[telefono] += 1
            return jsonify({
                "pregunta": "Queremos que la fiesta se disfrute al máximo..."
            })

    elif user_message_count[telefono] == 2:
        if pre_respuestas[2, 1] == "No":
            user_message_count[telefono] += 1
            return jsonify({
                "pregunta": "Muchas gracias por la info! ¿Necesitas confirmar asistencia de alguna persona más?"
            })

    else:
        return jsonify({
            "pregunta": "Gracias! Ante cualquier duda llamala a Pau."
        })
