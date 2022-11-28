import psycopg2

conn = psycopg2.connect(
    host="192.168.191.232",
    database="Proyecto_final",
    user="postgres",
    password="daniel123")

cursor=conn.cursor()
cursor.execute("SELECT nombre from Usuarios WHERE id_estudiante = 3")
for fila in cursor:
    data = fila[0]
    print(data)
conn.close()
