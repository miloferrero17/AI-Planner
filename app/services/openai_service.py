import requests
import os
import numpy as np
from dotenv import load_dotenv

def process_openai_message(conversation_history):
    """
    Realiza una llamada a la API de OpenAI usando el historial de conversación 
    y devuelve la respuesta junto con el historial actualizado.

    Args:
        conversation_history (list): Lista de mensajes en el formato esperado por OpenAI.

    Returns:
        tuple: Una tupla con:
            - str: La respuesta generada por OpenAI como un string.
            - list: El historial de conversación actualizado.
        None: Si ocurre un error.
    """
    # Obtener la clave de API desde las variables de entorno
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("La clave de API de OpenAI (OPENAI_API_KEY) no está configurada.")

    # Crear el payload
    payload = {
        "model": "gpt-4",
        "messages": conversation_history,
        "temperature": 0
    }

    # Configurar la URL y encabezados
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        # Hacer la solicitud POST
        response = requests.post(url, json=payload, headers=headers)

        # Validar el código de estado de la respuesta
        if response.status_code == 200:
            # Parsear la respuesta
            response_data = response.json()
            respuesta_generada = response_data['choices'][0]['message']['content']

            # Actualizar el historial de conversación
            conversation_history.append({
                "role": "assistant",
                "content": respuesta_generada
            })

            return respuesta_generada, conversation_history
        else:
            print(f"Error al comunicarse con OpenAI: {response.status_code} - {response.text}")
            return None, conversation_history
    except Exception as e:
        print(f"Excepción al comunicarse con OpenAI: {e}")
        return None, conversation_history
