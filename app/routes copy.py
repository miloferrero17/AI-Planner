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
#collection_name = "users"




@main_blueprint.route('/endpoint', methods=['POST'])
def handle_post_request():
    global conversation_history
    global pre_respuestas
    print(pre_respuestas)

    data = request.get_json()
    telefono = data.get("telefono")
    mensaje = data.get("mensaje")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    if telefono not in user_message_count or user_message_count[telefono] == -1:
        #conversation_history = [{"role": "user", "content": "Respuesta abierta: " + mensaje}]
        user_message_count[telefono] = 0
        conversation_history.append({"role": "assistant", "content": "Contexto: sos un asistente para padres/madres/tutores de invitados a una fiesta de 15 años. La información a recabar es: Nombre/Apodo y Apellido y preferencia alimentaria. El resultado buscado es un listado de 3 columnas: el telefono del responsable, el nombre y apellido del invitado y la preferencia alimentaria del invitado" })
        conversation_history.append({"role": "user", "content": "Mensaje de apertura: " + mensaje})
        conversation_history.append({
            "role": "assistant",
            "content":   "Razonamiento: Crees que el mensaje previo contiene respuestas válidas de las siguiente informacion: 1. Nombre (o Apodo) y Apellido del invitado ||| 2. Preferencia Alimentaria siendo: 1 - celiaco; 2 - diabetico; 3 - vegetariano; 4 - vegano; 5 - Sin preferencia ||| 3. Si confirma a más de una perona, cuantas? ||| contestame únicamente un texto con (en este orden): + número de pregunta este la informacion o no (1,2 o 3) // + '1' si estás 100% seguro que con la respuesta del usuario se le puede dar una respuesta a esa pregunta o '0' // + y que estes seguro de la respuesta cual es, en caso de nombre/apodo y apellido con este formato: 'Nombre y apodo' ' ' ''Apellido' y del primero que mencione || ejemplo de output: 1, 1, Emilio Ferrero; 2, 0, NA; 3, 0, NA."
       })  
        print(conversation_history)
        
        pre_respuestas, conversation_history = process_openai_message(conversation_history)

        conversation_history.append({
            "role": "assistant",
            "content": pre_respuestas   
            })
        print()
        print(conversation_history)
        
        
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
        print(pre_respuestas[0][1])

        

        #### Pre cargo en el vector las variables que me contestó en la respuesta abierta
        #if pre_respuestas[0, 1] == " 1":
        #    conversation_history.append({"role": "assistant", "content": "Razonamiento: en base a "+ pre_respuestas[0, 2]+ "extrae un nombre/apodo y apellido"})
        #    nombre_aux, conversation_history = process_openai_message(conversation_history)
        #    print(nombre_aux)

            #user_data = { 
            #    "Last_Interaction_Timespam": timestamp,
            #    "Invitado_1": pre_respuestas[0, 2]}    
            #create_or_update_document(collection_name, document_id, user_data)
         

        #### Pregunta cerrada de nombre
        if pre_respuestas[0, 1] == " 0":
            user_message_count[telefono] = 1
            conversation_history.append({"role": "assistant", "content": "Pregunta nombre: Muchas gracias por tomarte estos minutos para hacer la confirmación a la fiesta de Pupe!. ¿Podrías decirme el nombre y apellido de la persona que confirmás y si va a asistir al evento?"})            
            return jsonify({
                "pregunta": "Muchas gracias por tomarte estos minutos para hacer la confirmación a la fiesta de Pupe!. ¿Podrías decirme el nombre y apellido de la persona que confirmás y si va a asistir al evento?"
            })
        
        else:
            user_message_count[telefono] = 1

    if user_message_count[telefono] == 1:
            ### Pregunta cerrada de preferencia_alimenticia
            if pre_respuestas[1, 1] == " 0":
                user_message_count[telefono] = 2
                pregunta_2 = "Queremos que <nombre del invitado> disfrute al máximo de la fiesta, por eso nos gustaría saber si tiene alguna preferencia o restricción alimentaria (por ejemplo: celíaco, vegetariano, vegano, diabético). ¡Contanos y nos adaptamos!"               
                conversation_history.append({"role": "assistant", "content": "Podrías adaptar esta pregunta modificando el nombre declarado por el del niño" + pregunta_2})
                pregunta_2, conversation_history = process_openai_message(conversation_history)
                
                return jsonify({
                    "pregunta": pregunta_2
                })

            else:
                user_message_count[telefono] = 2    
    
    
    if user_message_count[telefono] == 2:
        ### Respuesta cerrada de preferencia alimenticia        
        if pre_respuestas[1, 1] == " 0":
            #conversation_history.append({"role": "user", "content": "Respuesta preferencia alimenticia: " + mensaje})
            conversation_history.append({"role": "assistant", "content":mensaje + "Razonamineto: en este mensaje se puede detectar la preferencia alimentaria? Me darías el número?"})
            prefe_aux, conversation_history = process_openai_message(conversation_history)
            print(prefe_aux)
            
            if prefe_aux == "Schema Error":
                user_message_count[telefono] = 2
                return jsonify({
                "pregunta": error_prefe
                })
        
            #user_data = { 
            #    "Last_Interaction_Timespam": timestamp,
            #    "Preferencias_1":prefe_aux}    
            #create_or_update_document(collection_name, document_id, user_data)

        ### Pregunta cerrada de acompañante
        if pre_respuestas[2, 1] == " 0":
            conversation_history.append({"role": "assistant", "content": "Pregunta Acompañante:" + pregunta_acompa_1})
            user_message_count[telefono] = 3
            return jsonify({
                "pregunta": pregunta_acompa_1
            })
        
        else:
            user_message_count[telefono] = 3


    if user_message_count[telefono] == 3:
        ### Respuesta abierta de acompañante        
        if pre_respuestas[2, 1] == " 1":
            user_message_count[telefono] = -1
            return jsonify({
                "pregunta": pregunta_acompa_2
            })
        
      
        ### Respuesta cerrada de acompañante        
        if pre_respuestas[2, 1] == " 0":
            #print(pre_respuestas)
            #conversation_history.append({"role": "user", "content": "Respuesta acompa: " + mensaje})
            conversation_history.append({"role": "assistant", "content": mensaje + razonamiento_acomp})
            print(conversation_history)
            acompa_aux, conversation_history = process_openai_message(conversation_history)
            if acompa_aux == "Schema Error":
                user_message_count[telefono] = 3
                return jsonify({
                "pregunta": error_acomp
                })
            
            
            
            print(acompa_aux)
            


            if acompa_aux == "1":
                user_message_count[telefono] = -1
                return jsonify({ 
                    "pregunta": pregunta_acompa_2
                })
            else:
                user_message_count[telefono] = 4
                return jsonify({
                    "pregunta": "Genial! Ya lo agregamos a la lista de invitados. ¿Tenes alguna otra duda?"
                })
      
        ### Fin de la charla-agradecimiento       

    else:
        return jsonify({
            "pregunta": "Fin de la conversación, cualquier duda habla con Pau :)"
        })