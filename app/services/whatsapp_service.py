import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

WA_API_KEY = os.getenv("WA_API_KEY")

def send_whatsapp_message(phone_number, message_body):
    url = "https://graph.facebook.com/v21.0/535696316293576/messages"
    headers = {
        "Authorization": f"Bearer {WA_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message_body}
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Error al enviar mensaje de WhatsApp: {response.status_code}")

    return response.json()

def send_whatsapp_message_twilio(body, to):
    """
    Envía un mensaje de WhatsApp usando Twilio.

    Parámetros:
        body (str): Contenido del mensaje a enviar.
        to (str): Número de WhatsApp del destinatario, e.g., 'whatsapp:+123456789'.

    Retorna:
        Message: Objeto del mensaje de Twilio con detalles del mensaje enviado.
    """
    return client.messages.create(
        from_='whatsapp:+14155238886',  # Reemplaza con tu número de Twilio
        body=body,
        to=to
    )
