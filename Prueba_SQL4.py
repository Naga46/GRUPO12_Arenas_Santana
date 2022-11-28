
import psycopg2

conn = psycopg2.connect(
    host="192.168.191.232",
    database="Proyecto_final",
    user="postgres",
    password="daniel123")

cursor=conn.cursor()

cursor.execute("SELECT Foto_location1, Foto_location2 FROM fotos WHERE id_estudiante =1")
for fila in cursor:
    original1 = fila[0]
    original2 = fila[1]
    print(original1)
    print(original2)
    
