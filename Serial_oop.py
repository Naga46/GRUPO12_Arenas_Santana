import serial
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            class temp:
                def __init__(self, temperatura):
                    self.temperatura=temperatura
                
                def consulta(self):
                    print("la temperatura actual es de:", self.temperatura)

            #print(line)
            termometro= temp (line)
            termometro.consulta()


