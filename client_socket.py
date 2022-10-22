import socket
from getmac import get_mac_address as gma

HEADER = 64
PORT = 5064

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
MAC = str((gma()))
SERVER = '192.168.43.182'
#SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT) #encode the message in byte format o encode str in byte object
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)#encode the lenght of the message
    send_length += b' ' * (HEADER - len(send_length))# darle el largo al mensaje de 64
    #b'' byte representación
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


send("Dirección MAC:")
send (MAC)

input()
Casos_activos = 123
muertes = 123
msg = "Casos_activos," + str(Casos_activos)+ ", muertes," + str(123)
send(msg)



test_data = list()
test_data = [12, 12]
data_socket = 'temperature='+str(test_data[0])+','+'Humidity='+str(test_data[1])
send(data_socket)

send("Hello Everyone!")

send("Hello EIE!")



send(DISCONNECT_MESSAGE)
