import socket

addr = ("192.168.15.5", 41929) #Cria o endereço
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Conecta no tcp
try:
    server.bind(addr)
except socket.error as e:
    str(e)
server.listen(1) #Fica na escuta de 1 cliente

msg = ""
received = ""
conn, addr = server.accept() #Quando aceitar 1 conexão
while True:
    received = conn.recv(2048) #Fica a espera da msg
    if received: #Caso exista, printa a mensagem
        print("{}: {}".format(addr,received.decode()))
        if received.decode() == "QUIT": #Verifica o QUIT
            break
        msg = input("Digite a mensagem: ")
        conn.send(msg.encode('UTF-8')) #Manda a mensagem
        if msg == "QUIT":
            break
        received = ""