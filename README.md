Guada-Bot Tech Specs

Descripción General

La aplicación permite gestionar la lista de invitados para un cumpleaños de 15 a través de WhatsApp. Está potenciada por ChatGPT con el fin de asegurar una UX fluida. Los datos a recolectar son: **Asistencia**, **Nombre y Apellido**, **Preferencia Alimentaria** y **si asistirán acompañados**.

Características Principales

- **Integración con WhatsApp**: Utiliza la API de WhatsApp Business vía Twilio para enviar y recibir mensajes automáticamente.
- **Motor de IA**: ChatGPT interpreta los mensajes y responde de manera natural para recopilar la información necesaria.
- **Base de Datos Centralizada**: Los datos recolectados se almacenan en tiempo real en una base de datos segura.
- **Interfaz de Administración**: Visualiza y exporta la lista de invitados en formatos Google Sheet.

1. Casos de Uso

#1: Proactivo

1. **Configuración Inicial**:

   - El anfitrión recopila y proporciona los números de teléfono de los invitados.
   - Personaliza los mensajes iniciales según las necesidades del evento.

2. **Interacción Inicial**:

   - La aplicación envía un mensaje automático (a definir el wording) personalizado a cada invitado:
     "Hola [Nombre], me encantaría que compartamos mi cumpleaños de 15. Por favor, si te sumas, respóndeme con la siguiente información:
     1. Nombre y Apellido.
     2. Preferencia alimentaria (Ej: vegetariana, vegana, sin restricciones).
     3. ¿Vendrás acompañado/a? (Sí/No y cuántas personas)."

3. **Interacción Automática**:

   - ChatGPT interpreta las respuestas y solicita aclaraciones en caso de ser necesario.
   - Ejemplo: "¿Podrías especificar cuántas personas te acompañarán y sus nombres?"

4. **Almacenamiento de Datos**:

   - Los datos se guardan automáticamente en la base de datos SQL.

5. **Reporte Final**:

   - Las respuestas estan sincronizadas con un Google Sheet.

#2: Fifteen Planner

1. **Acceso por Enlace**:

   - Se proporciona un enlace público o privado con el texto "Habla, me encantaría que vengas a mi cumple de 15, hablá con mi wedding planner AI que tiene algunas preguntas".
   - El enlace dirige al invitado a una interfaz de chat (via WhatsApp o web).

2. **Interacción Inicial**:

   - En el chat, el sistema solicita la siguiente información:
     - Nombre y Apellido.
     - Preferencia alimentaria.
     - Detalles de acompañantes (si aplica).

3. **Confirmación y Seguimiento**:

   - El sistema verifica que toda la información requerida sea clara.
   - En caso de dudas, se realiza una pregunta de seguimiento.

4. **Finalización**:

   - La información recolectada se almacena en la base de datos.

#3: ABM Listado
1. **Conexión con Google Sheet**:
ABM de un super-user con capacidad de alta, baja o modificación de registros.

2 Requisitos Técnicos

2.1 Infraestructura

- **Servidor**:

  - Hosting en la nube (AWS, Google Cloud, o similar).
  - Python para backend.
  - Base de datos MySQL.

- **WhatsApp Business API**:

  - Cuenta verificada de WhatsApp Business. (Lo que le pedí a Ger)
  - Acceso a la API mediante Twilio como proveedor autorizado.

2.2 Dependencias

- SDK o biblioteca para integración con WhatsApp Business API.
- OpenAI API para la funcionalidad de ChatGPT.
- Google Sheets

2.3 Implementación de IA

- **Modelo Utilizado**: GPT-4.

Consideraciones Finales

La aplicación está diseñada para optimizar la gestión de eventos mediante el uso de tecnología moderna, asegurando una experiencia fluida para el anfitrión y los invitados.


Anexo I - Wordings

#1 - Proactivo (WIP)

#2 - Fifteen Planner

Step 1 - Link a WhatsApp: “"Me encantaría compartir mi cumple con ustedes. Les dejo el contacto de María, mi Fifteen Planner AI, que les va a hacer unas preguntitas para organizar todo mejor. ¡Gracias!"

Transición al WA de Maria

Step 2 - Mensaje de Bienvenida: “Hola, soy Maria, la planner de Guada. A Guada le encantaría que compartas con ella ese día especial, el 20 de Agosto en Campo Chico. En caso de asistir, ¿podrías decirme tu nombre y apellido?"

Step 3 - Restricción alimentaria: Queremos que disfrutes de la noche al máximo, por eso nos gustaría saber si tenés alguna preferencia o restricción alimentaria (por ejemplo: celíaco, vegetariano, vegano, diabético). ¡Contanos y nos adaptamos!

Step 4 - ¿Acompañado?: ¿Vas a venir acompañada?

Anexo I - Wordings revisados

Step 1 - Link a WhatsApp: “Hola! Ya falta poco para el cumple de Pupe y quería pasarles el contacto del AI Planner  para que puedan confirmar la asistencia a la fiesta ¡Gracias!"

Transición al WA del AI Planner 

Step 2 - Mensaje de Bienvenida: “Muchas gracias por tomarte estos minutos para hacer la confirmación a la fiesta de Pupe!. ¿Podrías decirme el nombre y apellido de la persona que confirmás y si va a asistir al evento?"

Step 3 - Restricción alimentaria: Queremos que la fiesta se disfrute al máximo, por eso nos gustaría saber si el invitado tiene alguna preferencia o restricción alimentaria (por ejemplo: celíaco, vegetariano, vegano, diabético). ¡Contanos y nos adaptamos!

Step 4 - Muchas gracias por la info! ¿Necesitas confirmar asistencia de alguna persona más?

