import serial
import time

with open("ppp.csv","w") as f:
    f.write("temperatura atual, tempo")
    f.write("\n")
    t0 = time.time()
    porta = "COM5"
    baudrate = 115200

    arduino = serial.Serial(porta, baudrate, timeout=1)

    if arduino.is_open:
        print("Porta aberta com sucesso!")

    try:
        while True:
            if arduino.in_waiting > 0:
                dados = arduino.read(arduino.in_waiting)
                print(f'Dados recebidos: {dados.decode()}')
                a = (dados.decode()).split()
                tf = time.time()
                f.write(f"{float(a[0])}, {tf-t0}") 
                f.write("\n")
            else:
                print("Aguardando dados...")  
            
            time.sleep(0.1)  

    except KeyboardInterrupt:
        print("Leitura interrompida pelo usuário.")

    finally:
        arduino.close()
