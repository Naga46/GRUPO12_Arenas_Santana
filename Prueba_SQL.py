import psycopg2

conn = psycopg2.connect(
    host="192.168.191.232",
    database="Proyecto_final",
    user="postgres",
    password="daniel123")

j=3
name = 'Joaquin Sandoval'

cursor=conn.cursor()
cursor.execute("INSERT INTO usuarios  VALUES({},'{}','M','92','2' )".format(j,name))
conn.commit()
