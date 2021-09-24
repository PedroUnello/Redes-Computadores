import socket

addr = ("192.168.15.5", 41929) #Cria o endereço
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Conecta no udp
server.bind(addr)

msg = ""
received = ""
while True:
    received, addr = server.recvfrom(2048) #Espera uma mensagem
    #Printa a mensagem e o endereço do remetente
    print("{}: {}".format(addr,received.decode()))
    if received.decode() == "QUIT": #Verifica o QUIT
        break
    if received != "": #caso tenha recebido uma mensagem
        msg = input("Digite a mensagem: ") #Escreve uma msg
        server.sendto(msg.encode('UTF-8'), addr) #Manda a mensagem
        if msg == "QUIT": #Se for quit...
            break
        received = ""