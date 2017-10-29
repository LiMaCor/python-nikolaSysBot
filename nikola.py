#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Librerías
import telebot
from telebot import types # Tipos para la API del bot.
from datetime import datetime
import time # Librería para hacer que el programa que controla el bot no se acabe.
from modules.uptime import uptime_string
from modules.uptime import logs_size

# Librerías de acciones en el sistema
import sys
import subprocess

# Importamos el TOKEN y USERS desde settings
from settings import TOKEN
from settings import USERS
from settings import LOGDIR
from settings import LOGFILE
from settings import PATH

bot = telebot.TeleBot(TOKEN) # Creamos el objeto del bot.
print("Bot iniciado y listo para servir:")

############ VARS #######################
start_time = time.time()
last_error_time = None

#########################################
############ LISTENER ###################
# Con esto, estamos definiendo una función llamada 'listener', que recibe como
#   parámetro un dato llamado 'messages'.
def listener(messages):
    for m in messages: # Por cada dato 'm' en el dato 'messages'
        if m.content_type == 'text': # Filtramos mensajes que sean tipo texto.
            cid = m.chat.id # Almacenaremos el ID de la conversación.
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            if cid > 0:
                # Si 'cid' es positivo, usaremos 'm.chat.first_name' para el nombre.
                mensaje = "[" + now + "]: " + str(m.chat.first_name) + "(" + str(cid) + "): " + m.text
            else:
                # Si 'cid' es negativo, usaremos 'm.from_user.first_name' para el nombre.
                mensaje = "[" + now + "]: " + str(m.from_user.first_name) + "(" + str(cid) + "): " + m.text
            f = open( LOGDIR + LOGFILE, 'a') # Abrimos nuestro fichero log en modo 'Añadir'.
            f.write(mensaje + "\n") # Escribimos la linea de log en el fichero.
            f.close() # Cerramos el fichero para que se guarde.
            #mensaje = update.mensaje.text.encode('utf-8')
            print(mensaje) # Imprimimos el mensaje tambien en la terminal

# Ejecutamos funcion que "escucha" los mensajes
bot.set_update_listener(listener)

#########################################
############ FUNCIONES ##################
##### Comandos publicos #####
## Funcion de inicio
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    # Si no esta en la lista de chats permitidos, deniega acceso
    if not str(cid) in USERS:
        bot.send_message( cid, "Usuario no autorizado. Funciones limitadas.")
    else:
        bot.send_message( cid, "Usuario autorizado.")

## Funcion basica de testeo
@bot.message_handler(commands=['helloworld']) # comando '/helloworld'
def command_helloworld(m): # Definimos la función
    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
    # funcion 'send_message()' del bot: enviamos al ID de chat guardado el texto indicado
    bot.send_message( cid, 'Hello World')

# Comando que redirige al respositorio del propio bot
@bot.message_handler(commands=['repo'])
def command_repo(m):
    markup = types.InlineKeyboardMarkup()
    itembtnrepo = types.InlineKeyboardButton('Pulsar aqui!', url='https://github.com/andoniaf/python-nikolaSysBot')
    markup.row(itembtnrepo)
    bot.send_message(m.chat.id, '\U000021b3 Github repo:', reply_markup=markup)

# Muestra el uptime del servidor
@bot.message_handler(commands=['uptime'])
def command_uptime(m):
    cid = m.chat.id
    bot.send_chat_action(cid, "typing")
    message = uptime_string(start_time, last_error_time)
    bot.send_message(cid, message)

##### Comandos reservados para usuarios reconocidos #####
# Muestra el tamaño de los logs del bot
@bot.message_handler(commands=['logsize'])
def command_logsize(m):
    cid = m.chat.id
    if not str(cid) in USERS:
        bot.send_message( cid, "Permiso denegado")
    else:
        bot.send_chat_action(cid, "typing")
        message = logs_size(PATH)
        bot.send_message(cid, message)

# Detiene el bot
@bot.message_handler(commands=['stop'])
def command_stop(m):
    cid = m.chat.id
    if not str(cid) in USERS:
        bot.send_message( cid, "Permiso denegado")
    else:
        bot.send_message(cid, "One more time, bye!")
        sys.exit()

# Reinicia el bot
@bot.message_handler(commands=['re_bot'])
def command_rebot(m):
    chatID = m.chat.id
    if not str(chatID) in USERS:
        bot.send_message(chatID, "Permiso denegado")
    else:
        bot.send_message(chatID, "Reiniciando . . .")
        proceso = subprocess.Popen(['./script_rebot'])

        proceso
        bot.send_chat_action(chatID, "typing")
        #reboot_msg = "¡Reiniciado!" + str(os.getpid())
        reboot_msg = "¡Reiniciado!"
        bot.send_message(chatID, reboot_msg)
        sys.exit()







#########################################
# Con esto, le decimos al bot que siga funcionando incluso si encuentra
#   algún fallo.
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        last_error_time = time.time()
