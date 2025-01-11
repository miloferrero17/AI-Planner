from flask import Blueprint, request, jsonify
from app.services.openai_service import process_openai_message
from app.services.whatsapp_service import send_whatsapp_message
from datetime import datetime
import numpy as np
from io import StringIO

main_blueprint = Blueprint("main", __name__)

user_message_count = {}
user_questions = {}
pre_respuestas = {}
conversation_history = {}

@main_blueprint.route('/endpoint', methods=['POST'])
def handle_post_request():
    data = request.get_json()
    telefono = data.get("telefono")
    mensaje = data.get("mensaje")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    global pre_respuestas
    #print(pre_respuestas)
    conversation_history = [{
            "role":
            "user",
            "content": mensaje  }]
    
    
    # Procesar mensaje con OpenAI
    if telefono not in user_message_count:
        conversation_history.append({
            "role": "user",
            "content":  "Crees que en el siguiente mensaje: " + mensaje +
            " contiene respuestas de las siguiente informacion: 1. Nombre y Apellido del invitado ||| 2. Preferencia Alimentaria siendo: 1 - celiaco; 2 - diabetico; 3 - vegetariano; 4 - vegano; 5 - Sin preferencia ||| 3. Si confirma a alguien más ||| contestame únicamente un texto con (en este orden): + número de pregunta este la informacion o no (1,2 o 3) // + '1' si estás 100% seguro que con la respuesta del usuario se le puede dar una respuesta a esa pregunta o '0' // + y que estes seguro de la respuesta cual es || ejemplo de output: 1, 1, Emilio Ferrero; 2, 0, NA; 3, 0, NA;"
       })  
        pre_respuestas, conversation_history = process_openai_message(conversation_history)
        #print(conversation_history)
        #print(pre_respuestas)
        csv_data = StringIO(pre_respuestas.replace(";", "\n"))
        pre_respuestas = np.genfromtxt(csv_data, delimiter=",", dtype=str)
        user_message_count[telefono] = 0

        
        if pre_respuestas[0, 2] == " NA":
            user_message_count[telefono] += 1
            pregunta_1 = "Muchas gracias por tomarte estos minutos para hacer la confirmación a la fiesta de Pupe!. ¿Podrías decirme el nombre y apellido de la persona que confirmás y si va a asistir al evento?"
            conversation_history.append({"role": "assistant", "content": pregunta_1})
            #print(conversation_history)
            return jsonify({
                "pregunta": pregunta_1
            })
        else:
            user_message_count[telefono] = 1

    if user_message_count[telefono] == 1:
        print("2")
        if pre_respuestas[1, 1] == " 0":
            conversation_history.append({"role": "assistant", "content": "Queremos que <Nombre sin apellido> disfrute la fiesta al máximo, por eso nos gustaría saber si el invitado tiene alguna preferencia o restricción alimentaria (por ejemplo: celíaco, vegetariano, vegano, diabético). ¡Contanos y nos adaptamos!"})
            pregunta_2, conversation_history = process_openai_message(conversation_history)
            print(conversation_history)
            print(pre_respuestas)
            user_message_count[telefono] = 2
            return jsonify({
                "pregunta": pregunta_2
            })
        else:
            user_message_count[telefono] = 2


    if user_message_count[telefono] == 2:
        print("3")

        if pre_respuestas[2, 1] == " 0":
            pregunta_3 = "Muchas gracias por la info! ¿Necesitas confirmar asistencia de alguna persona más?"
            conversation_history.append({"role": "assistant", "content": pregunta_3})
            conversation_history.append({"role": "assistant", "content": "Podrias hacer un string afectuoso ycon el siguiente formato, tomando el nombre sin el apellido del historial de charlas: Además de <Nombre> ¿Necesitas confirmar asistencia de alguna persona más?"})
            user_message_count[telefono] += 1
            return jsonify({
                "pregunta": pregunta_3
            })
        
        else:
            user_message_count[telefono] = 3


    else:
        print("3")
        conversation_history.append({"role": "assistant", "content":  "Podrías darme 1 mensaje pelado para ser enviado a un chatbot con este concepto <Gracias, cualquier duda llamala a Pau>"})
        pregunta_4, conversation_history = process_openai_message(conversation_history)
    
        return jsonify({
            "pregunta": pregunta_4
        })
