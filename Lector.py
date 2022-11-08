# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import time
import board
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import numpy as np
import getpass

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

#uart = busio.UART(board.TX, board.RX, baudrate=57600)

# If using with a computer such as Linux/RaspberryPi, Mac, Windows with USB/serial converter:
# import serial
# uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi and hardware UART:
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

##################################################
names=[]
numbers=[]
del_num=0

def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Esperando Imagen...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Procesando...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Buscando...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True


# pylint: disable=too-many-branches
#def get_fingerprint_detail():
#    """Get a finger print image, template it, and see if it matches!
#    This time, print out each error instead of just returning on failure"""
#    print("Oteniendo Imagen...", end="")
#    i = finger.get_image()
#    if i == adafruit_fingerprint.OK:
#        print("Imagen Obtenida")
#    else:
#        if i == adafruit_fingerprint.NOFINGER:
#            print("No se detectan una huella")
#        elif i == adafruit_fingerprint.IMAGEFAIL:
#            print("Error de compilacion")
#        else:
#            print("Otro error")
#        return False


#    print("Compilando...", end="")
#    i = finger.image_2_tz(1)
#    if i == adafruit_fingerprint.OK:
#        print("Compilado")
#    else:
#        if i == adafruit_fingerprint.IMAGEMESS:
#            print("Imagen esta muy borrosa")
#        elif i == adafruit_fingerprint.FEATUREFAIL:
#            print("No se pudo identificar una huella")
#        elif i == adafruit_fingerprint.INVALIDIMAGE:
#            print("Imagen Invalida")
#        else:
#            print("Otro error")
#        return False

#    print("Buscando...", end="")
#    i = finger.finger_fast_search()
    # pylint: disable=no-else-return
    # This block needs to be refactored when it can be tested.
#    if i == adafruit_fingerprint.OK:
#        print("Huella Encontrada!")
#        return True
#    else:
#        if i == adafruit_fingerprint.NOTFOUND:
#            print("No se encontro coincidencia")
#        else:
#            print("Otro error")
#        return False


# pylint: disable=too-many-statements
def enroll_finger(location):
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        #if fingerimg == 1:
           # print("Place finger on sensor...", end="")
        #else:
             #print("Place same finger again...", end="")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("\nImagen Otenida")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Error en la imagen")
                return False
            else:
                print("Otro Error")
                return False

        print("Compilando ...", end="")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Compilado")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Imagen muy borrosa")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("No se pudieron distinguir caracteristicas de la imagen")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Imagen Invalida")
            else:
                print("Otro error")
            return False

        if fingerimg == 1:
            print("\n Remueva el dedo y vuelva a ponerlo.")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creando modelo...", end="")
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Modelo Creado")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Las huellas no coincidieron")
        else:
            print("Otro error")
        return False

    print("Guardando modelo #%d..." % location, end="")
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Modelo Guardado")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Lugar de almacenaminto errado")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Error de la memoria Flash")
        else:
            print("Otro error")
        return False

    return True


##################################################


def get_num():
    """Use input() to get a valid number from 1 to 127. Retry till success!"""
    i = 0
    while (i > 127) or (i < 1):
        try:
            i = int(input("Ingrese una ID # entre 1-127: "))
            print("Ponga su dedo en el Sensor")
        except ValueError:
            pass
    return i


while True:
    print("----------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Error al leer las Plantillas")
    print("Fingerprint templates:", finger.templates)
    print("e) Guardar Huella")
    print("f) Buscar Huella")
    print("d) Borrar Huella")
    print("----------------")
    c = input("> ")
    if c=="e" or c=="d":
        password= getpass.getpass(prompt='Ingrese Contraseña\n')
        passwordR="1234"
    

    if c == "e" and password==passwordR:
        enroll_finger(get_num())

    elif c == "f":
        if get_fingerprint():
            print("Detected #", finger.finger_id, "with confidence", finger.confidence)
        else:
            print("Huella no Encontrada")
    elif c == "d"and password==passwordR:

        if finger.delete_model(get_num()) == adafruit_fingerprint.OK:

            print("Borrada!")
        else:
            print("Falla al Borrar")
    else:
        print("Error en la contraseña")
