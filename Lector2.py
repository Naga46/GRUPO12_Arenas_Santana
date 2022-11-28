import time
import board
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import numpy as np
import getpass
import picamera
import psycopg2
import os
from shutil import rmtree
import cv2
import face_recognition
import I2C_LCD_driver

################################ LCD###############
mylcd = I2C_LCD_driver.lcd()
###################################################

############################################    SQL     ########################################################
################################################################################################################
conn = psycopg2.connect(
    host="192.168.191.232",
    database="Proyecto_final",
    user="postgres",
    password="daniel123")
cursor=conn.cursor()
################################################################################################################
################################################################################################################

camera=picamera.PiCamera()

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
################ FUNCIONES ################
delete=0

################ BUSCAR HUELLA DACTILAR EN EL REGISTRO DEL LECTOR ################
def get_fingerprint():
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Ponga su dedo", 1)
    """Get a finger print image, template it, and see if it matches!"""
    print("Ponga su dedo")
    time.sleep(2)
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    mylcd.lcd_display_string("Retire Dedo", 2)
    print("Procesando...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Buscando...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True


################ ASIGNAR ID A UNA HUELLA ################
def get_num():
    """Use input() to get a valid number from 1 to 127. Retry till success!"""
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Ingrese ID", 1)
    i = 0
    while (i > 127) or (i < 1):
        try:
            i = int(input("Ingrese una ID # entre 1-127: "))
            
        except ValueError:
            pass
    return i


################ EXTRACCION DE HUELLA DACTILAR ################
def enroll_finger(location):
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
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
            mylcd.lcd_display_string("Retire Dedo", 2)
            time.sleep(2)
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Ponga su dedo", 1)
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
    mylcd.lcd_display_string("Retire Dedo", 2)
    time.sleep(2)
    return True
    

################## Obtener datos##############################
def get_data():
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Ingrese", 1)
    mylcd.lcd_display_string("Nombre:      ", 2)
    print("ingrese su nombre:\n")
    name=input(">")
    mylcd.lcd_display_string("Apellido:      ", 2)
    print("ingrese Apellido:\n")
    apellido=input(">")
    mylcd.lcd_display_string("Sexo:        ", 2)
    print("ingrese su Sexo:\n")
    sexo=input(">")
    mylcd.lcd_display_string("Carrera:      ", 2)
    print("ingrese su Carrera:\n")
    carrera=input(">")
    mylcd.lcd_display_string("Nivel seguridad:", 2)
    print("ingrese su seguridad:\n")
    seguridad=input(">")

    return name,apellido,sexo,carrera,seguridad


################ SACAR FOTO CON CAMARA ################
def get_picture(j):

    print("Presione enter para tomar la primera foto\n")
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Presione Enter", 1)
    mylcd.lcd_display_string("Para foto", 2)
    input(">")
    mylcd.lcd_clear()
    mylcd.lcd_display_string("sonria", 1)
    path_imagen=path_actual+"/"+ "imagenes" +"/" +j+"/frente.jpg"
    camera.capture(path_imagen)
    print("Foto tomada\n")
    time.sleep(3)
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Presione Enter", 1)
    mylcd.lcd_display_string("Para foto", 2)
    print("Presione enter para tomar la segunda foto\n")
    input(">")
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Sonria", 1)
    path_imagen2=path_actual+"/"+ "imagenes" +"/" +j+"/frente2.jpg"
    camera.capture(path_imagen2)
    print("Foto tomada\n")
    time.sleep(3)
    return path_imagen,path_imagen2


######## MANDAR INFO A LA BASE DE DATOS ###########
def send_to_Database(j,name,apellido,sexo,carrera,seguridad,path, path2):
    cursor.execute("INSERT INTO usuarios  VALUES({},'{}','{}','{}',{},'{}' )".format(j,name,apellido,sexo,carrera,seguridad))
    cursor.execute("INSERT INTO fotos VALUES({},'{}','{}')" .format(j,path,path2))
    conn.commit()
        

################# BORRAR INFO DE LA BASE DE DATOS ################################
def Delete_info_database (j):
    cursor.execute("DELETE FROM fotos WHERE id_estudiante = '{}'".format(j))
    cursor.execute("DELETE FROM Usuarios WHERE id_estudiante = '{}'".format(j))
    conn.commit()

###########################################################################

################ RECONOCIMIENTO FACIAL ################
def reconocimiento_facial (j):
    # imagen a comparar
    cursor.execute("SELECT Foto_location1, Foto_location2 FROM fotos WHERE id_estudiante  = {}".format(j))
    for fila in cursor:
        original1 = fila[0]
        original2 = fila[1]
        
    imagen=path_actual+"/imagenes/"+j+"/comparacion.jpg"
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Presione Enter", 1)
    mylcd.lcd_display_string("Para foto", 2)
    print("Presione enter para tomar la foto\n")
    input(">")
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Sonria", 1)
    camera.capture(imagen)
    time.sleep(2)
    print("\nFoto tomada")
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Buscando", 1)
    mylcd.lcd_display_string("Coincidencia", 2)
    print("\nBuscando coincidencia")

    im_comparacion=cv2.imread(imagen)
    face_loc1=face_recognition.face_locations(im_comparacion)[0]
    face_image_encodings0=face_recognition.face_encodings(im_comparacion, known_face_locations=[face_loc1])[0]

    #imagen1
    #original1=path_actual+"/imagenes/"+j+"/frente.jpg"
    original1=cv2.imread(original1)
    #imagen 2
    #original2=path_actual+"/imagenes/"+j+"/frente2.jpg"
    original2=cv2.imread(original2)

    face_locations1 = face_recognition.face_locations(original1)[0]
    face_image_encodings1=face_recognition.face_encodings(original1, known_face_locations=[face_locations1])[0]

    result = face_recognition.compare_faces([face_image_encodings0], face_image_encodings1)

    if result[0] == True:
        print("coincidencia encontrada")
        funciona=1
    else:
        face_locations2 = face_recognition.face_locations(original2)[0]
        face_image_encodings2=face_recognition.face_encodings(original2, known_face_locations=[face_locations2])[0]

        result = face_recognition.compare_faces([face_image_encodings0], face_image_encodings2)
        if result[0] == True:
            print("coincidencia encontrada")
            funciona=1

        else:
            funciona=0

    return funciona, imagen

################################################### CODIGO PRINCIPAL #################################################################################
path_actual=os.getcwd()
sala='RA 4-7'
cursor.execute("SELECT grado_seguridad FROM Sala WHERE sala_id ='{}'".format(sala))
for fila in cursor:
    permiso = fila[0]
find_user=0
Enroll_user=0
while True:
    ################ Escoger accion ####################
    c=0
    #print("Fingerprint templates:", finger.templates)
    print("e) Guardar Huella")
    print("f) Buscar Huella")
    print("d) Borrar Huella")
    print("----------------")
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Escoja Opcion", 1)  
    mylcd.lcd_display_string("e) Enroll User  ", 2) 
    time.sleep(1)
    mylcd.lcd_display_string("f) Find User    ", 2) 
    time.sleep(1)
    mylcd.lcd_display_string("d) Delete User  ", 2)
    time.sleep(1)
    c = input("> ") 
   
    print("----------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Error al leer las Plantillas")
    
    
    ################ SE DEFINE LA CONTRASEÑA ####################
    if c=="e" or c=="d":
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Ingrese", 1)
        mylcd.lcd_display_string("Contrasena", 2)
        password= getpass.getpass(prompt='Ingrese Contraseña\n')
        passwordR="1234"
    
############################################################################################
    ################ GUARDAR UN USUARIO ################
    if c == "e" and password==passwordR:
        listado_numeros=[]
        Enroll_user=1
        in_list=0
        j=get_num()
        j=str(j)
        cursor.execute("SELECT id_estudiante FROM usuarios")
        for fila in cursor:
            listado_numeros.append(fila)

        ### DETERMINAR SI USUARIO ESTA YA REGISTRADA O NO ###

        for n in listado_numeros:
            n=str(n)
            if j in n:
                print("Este numero ya se encuentra ocupado")
                mylcd.lcd_clear()
                mylcd.lcd_display_string("ID Ocupada", 1)
                in_list=1
                False

        listado_numeros=[]
        if in_list==0:
            j=int(j)
            print("Ponga su dedo en el Sensor")
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Ponga su dedo", 1)
            
            enroll_finger(j)
            j=str(j)
            name,apellido,sexo,carrera,seguridad=get_data()
            path_personal=path_actual+"/"+"imagenes"+"/"+j
            os.mkdir(path_personal)
            path,path2=get_picture(j)
            send_to_Database(j,name,apellido,sexo,carrera,seguridad,path,path2)
        Enroll_user=0
            
############################################################################################
    ##### ENCONTRAR UN USUARIO####
    elif c == "f":
        find_user=1
        if get_fingerprint():
            number=finger.finger_id
            number=str(number)
            try:
                reco, im_comparacion=reconocimiento_facial(number)
            except:
                reco=0
            number=int(number)
            if reco==1:
                mylcd.lcd_clear()
                mylcd.lcd_display_string("Coincidencia", 1)
                mylcd.lcd_display_string("Encontrada", 2)
                print("Detected #", number, "with confidence", finger.confidence)
                cursor.execute("SELECT nombre,Apellido,grado_seguridad FROM usuarios WHERE id_estudiante= {}".format(number))
                for fila in cursor:
                     nombre=fila[0]
                     apellido=fila[1]
                     seguridad=fila[2]
                     
                if seguridad<= permiso:
                    acceso='Permitido'
                else:
                    acceso='Denegado'
                

                cursor.execute("UPDATE fotos SET last_foto = '{}' WHERE id_estudiante = {}".format(im_comparacion,number))
                conn.commit()
                time.sleep(1)
                mylcd.lcd_clear()
                mylcd.lcd_display_string("Bienvenido", 1)
                mylcd.lcd_display_string("{}{}".format(nombre,apellido), 2)
                cursor.execute("INSERT INTO acceso(id_estudiante,sala_id,acceso) VALUES ({},'{}','{}')".format(number,sala,acceso))
                conn.commit()
                time.sleep(3)

            else:
                print("Rostro o huella no encontrada")
                mylcd.lcd_clear()
                mylcd.lcd_display_string("Huella o Rostro", 1)
                mylcd.lcd_display_string("No Identificado", 2)
                time.sleep(2)
        else:
            print("Huella no Encontrada")
        find_user=0

############################################################################################
    #### ELIMINAR UN USUARIO ####
    elif c == "d"and password==passwordR:
        delete=1
        j=get_num()
        try:
            if finger.delete_model(j) == adafruit_fingerprint.OK:
                j=str(j)
                rmtree(path_actual+"/"+ "imagenes" +"/" +j)
                j=int(j)
                Delete_info_database(j)
                mylcd.lcd_clear()
                mylcd.lcd_display_string("Borrando ID...", 1)
                time.sleep(1)
                mylcd.lcd_display_string("Borrado", 2)
                time.sleep(1)           

                print("Borrada!")
            else:
                print("Falla al Borrar")
        except:
            print("El usuario no existe")
        delete=0
        
    else:
        if password!=passwordR:
            print("Error en la contraseña")
        elif c!="d" and c!= "f" and c!="e":
            print("instruccion no reconocida")
