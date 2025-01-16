from flask import Blueprint, request, jsonify
from app.services.openai_service import process_openai_message
from app.services.whatsapp_service import send_whatsapp_message
from app.services.firebase_service import (
    add_user,
    create_or_update_document,
    read_document,
    update_document,
    delete_document
)
from datetime import datetime
import numpy as np
from io import StringIO


main_blueprint = Blueprint("main", __name__)

user_message_count = {}
user_questions = {}
pre_respuestas = {}
conversation_history = []
collection_name = "users"

@main_blueprint.route('/endpoint', methods=['POST'])
def handle_post_request():
    global conversation_history
    data = request.get_json()
    telefono = data.get("telefono")
    mensaje = data.get("mensaje")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    global pre_respuestas

    # Actualiza la conversación específica del teléfono
    conversation_history.append({"role": "user", "content": "Respuesta: " + mensaje})


    #document_id = telefono  # Un ID único para el documento (por ejemplo, el número del usuario)
    #user_data = {
    #    "Creation_Timespam": timestamp,
    #    "Last_Interaction_Timespam": timestamp,
    #    "Number": telefono
    #}

    # Llamar a la función para crear o actualizar el documento
    #create_or_update_document(collection_name, document_id, user_data)'''
    
    
    #print(conversation_history)
    # Procesar mensaje con OpenAI
    if telefono not in user_message_count or user_message_count[telefono] == -1:
        #conversation_history = [{"role": "user", "content": "Respuesta abierta: " + mensaje}]
        conversation_history.append({
            "role": "assistant",
            "content":  "Razonamiento: Crees que en el siguiente mensaje: " + mensaje +
            " contiene respuestas de las siguiente informacion: 1. Nombre (o Apodo) y Apellido del invitado ||| 2. Preferencia Alimentaria siendo: 1 - celiaco; 2 - diabetico; 3 - vegetariano; 4 - vegano; 5 - Sin preferencia ||| 3. Si confirma a más de una perona, cuantas? ||| contestame únicamente un texto con (en este orden): + número de pregunta este la informacion o no (1,2 o 3) // + '1' si estás 100% seguro que con la respuesta del usuario se le puede dar una respuesta a esa pregunta o '0' // + y que estes seguro de la respuesta cual es, en caso de nombre/apodo y apellido con este formato: 'Nombre y apodo' ' ' ''Apellido' y del primero que mencione || ejemplo de output: 1, 1, Emilio Ferrero; 2, 0, NA; 3, 0, NA;"
       })  
        pre_respuestas, conversation_history = process_openai_message(conversation_history)
        #print(conversation_history)
        #print(pre_respuestas)
        
        #Valido si las dimensiones de pre_respuestas en 3x3 o la inicio
        pre_respuestas_text = "1, 0, NA; 2, 0, NA; 3, 0, NA"
        csv_data = StringIO(pre_respuestas.replace(";", "\n"))
        pre_respuestas = np.genfromtxt(csv_data, delimiter=",", dtype=str)
        # Verifica las dimensiones del array
        expected_shape = (3, 3)
        # Si las dimensiones no coinciden
        if pre_respuestas.shape != expected_shape:
            print(f"Dimensiones incorrectas: {pre_respuestas.shape}. Ajustando...")
            # Crear un array vacío con valores por defecto ("NA" para texto)
            fixed_respuestas = np.full(expected_shape, "NA", dtype=str)
            # Copiar valores existentes si es posible
            rows_to_copy = min(pre_respuestas.shape[0], expected_shape[0])
            cols_to_copy = min(pre_respuestas.shape[1], expected_shape[1])
            fixed_respuestas[:rows_to_copy, :cols_to_copy] = pre_respuestas[:rows_to_copy, :cols_to_copy]
            pre_respuestas = fixed_respuestas

        user_message_count[telefono] = 0

        #### Pre cargo en la dB las variables que me contestó en la respuesta abierta
        if pre_respuestas[0, 1] == " 1":
            conversation_history.append({"role": "assistant", "content": "Razonamiento: Necesito que extraigas el nombre/apodo y apellido del invitado que primero menciona con este formato: 'Nombre o apodo Apellido'"})
            nombre_aux, conversation_history = process_openai_message(conversation_history)
            print(nombre_aux)

            #user_data = { 
            #    "Last_Interaction_Timespam": timestamp,
            #    "Invitado_1": pre_respuestas[0, 2]}    
            #create_or_update_document(collection_name, document_id, user_data)
         
        if pre_respuestas[1, 1] == " 1":
            conversation_history.append({"role": "assistant", "content": "Razonamiento: Necesito que extraigas la preferencia alimentaria con este formato: Preferencia Alimentaria siendo: 1 - celiaco; 2 - diabetico; 3 - vegetariano; 4 - vegano; 5 - otro, y me contestes con el numero"})
            prefe_aux, conversation_history = process_openai_message(conversation_history)
            print(prefe_aux)

            #user_data = { 
            #    "Last_Interaction_Timespam": timestamp,
            #    "Preferencias_1": pre_respuestas[1, 1]}    
            #create_or_update_document(collection_name, document_id, user_data)


        #### Pregunta cerrada de nombre
        if pre_respuestas[0, 1] == " 0":
            user_message_count[telefono] = 1
            pregunta_1 = "Muchas gracias por tomarte estos minutos para hacer la confirmación a la fiesta de Pupe!. ¿Podrías decirme el nombre y apellido de la persona que confirmás y si va a asistir al evento?"
            conversation_history.append({"role": "assistant", "content": "Pregunta nombre:" + pregunta_1})
            #print(conversation_history)
            #send_whatsapp_message(telefono, pregunta_1)
            return jsonify({
                "pregunta": pregunta_1
            })
        
        else:
            user_message_count[telefono] = 1

    if user_message_count[telefono] == 1:
            ### Respuesta cerrada de nombre
            if pre_respuestas[0, 1] == " 0":
                #print(conversation_history)
                #conversation_history.append({"role": "user", "content": "Respuesta nombre: " + mensaje})
                conversation_history.append({"role": "assistant", "content": "Razonamiento: Necesito que extraigas el nombre/apodo y apellido del invitado con este formato: //Nombre o apodo Apellido//"})
                nombre_aux, conversation_history = process_openai_message(conversation_history)
                #print(conversation_history)
                print("Nombre declarado: " +nombre_aux)

                #user_data = { 
                #    "Last_Interaction_Timespam": timestamp,
                #    "Invitado_1": nombre_aux}    
                #create_or_update_document(collection_name, document_id, user_data)

            ### Pregunta cerrada de preferencia_alimenticia
            if pre_respuestas[1, 1] == " 0":
                #conversation_history.append({"role": "user", "content": "Respuesta preferencias alimenticias: " + mensaje})
                conversation_history.append({"role": "assistant", "content": "Razonamiento: En base a la historia de preguntas y respuestas por favor escribí el siguiente mensaje: 'Queremos que (Nombre del invitado sin el apellido) disfrute la fiesta al máximo, por eso nos gustaría saber si el invitado tiene alguna preferencia o restricción alimentaria (por ejemplo: celíaco, vegetariano, vegano, diabético). ¡Contanos y nos adaptamos!'"})
                pregunta_2, conversation_history = process_openai_message(conversation_history)
                #print(conversation_history)
                #print(pre_respuestas)
                user_message_count[telefono] = 2
                return jsonify({
                    "pregunta": pregunta_2
                })

            else:
                user_message_count[telefono] = 2    
    
    
    if user_message_count[telefono] == 2:
        ### Respuesta cerrada de preferencia alimenticia        
        if pre_respuestas[1, 1] == " 0":
            #conversation_history.append({"role": "user", "content": "Respuesta preferencia alimenticia: " + mensaje})
            conversation_history.append({"role": "assistant", "content": "Razonamiento: En base a este mensaje: "+mensaje+" Que preferencia alimentaria tiene (solo el numero)? Preferencia Alimentaria siendo: 1 - celiaco; 2 - diabetico; 3 - vegetariano; 4 - vegano; 5 - Sin preferencia. "})
            prefe_aux, conversation_history = process_openai_message(conversation_history)
            print(prefe_aux)

            #user_data = { 
            #    "Last_Interaction_Timespam": timestamp,
            #    "Preferencias_1":prefe_aux}    
            #create_or_update_document(collection_name, document_id, user_data)

        ### Pregunta cerrada de acompañante
        if pre_respuestas[2, 1] == " 0":
            pregunta_3 = "Muchas gracias por la info! ¿Necesitas confirmar asistencia de alguna persona más?"
            conversation_history.append({"role": "assistant", "content": "Pregunta Acompañante:" + pregunta_3})
            user_message_count[telefono] = 3
            return jsonify({
                "pregunta": pregunta_3
            })
        
        else:
            user_message_count[telefono] = 3


    elif user_message_count[telefono] == 3:
        ### Respuesta abierta de acompañante        
        if pre_respuestas[2, 1] == " 1":
            return jsonify({
                        "pregunta": "AAA"
                    })   
        
      
        ### Respuesta cerrada de acompañante        
        if pre_respuestas[2, 1] == " 0":
            #print(pre_respuestas)
            #conversation_history.append({"role": "user", "content": "Respuesta acompa: " + mensaje})
            conversation_history.append({"role": "assistant", "content": "Razonamiento: En base a este mensaje: "+mensaje+" tiene que confirmar la asistencia de otro invitado? Responde con 1 por si o opr 0 por no.   "})
            print(conversation_history)
            acompa_aux, conversation_history = process_openai_message(conversation_history)
            print(acompa_aux)

            if acompa_aux == "1":
                user_message_count[telefono] = -1
                return jsonify({
                    "pregunta": "Avancemos con el proximo, contame de él!"
                })
            else:
                user_message_count[telefono] = 4
                return jsonify({
                    "pregunta": "Genial! Ya lo agregamos a la lista de invitados, si tenes alguna duda preguntale a Pau."
                })
      
        ### Fin de la charla-agradecimiento       

        else:
            return jsonify({
                "pregunta": "Fin de la conversación :)"
            })