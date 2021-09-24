import socket

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        self.server = "192.168.15.5" #Ip
        self.port = 41929 #Porta
        self.message = "initial"
        self.address = (self.server, self.port)

    def envia(self, msg): #Envia os dados ao servidor e retorna a resposta
        #Faz o encode para utf-8, e manda pelo socket criado da instância
        self.client.sendto(msg.encode('UTF-8'), self.address) 
    
    def recebe(self):
        return self.client.recvfrom(2048) #Recebe a resposta pelo socket

client = Client() #Instância o socket do cliente
msg = ""
while  True:
    msg = input("Digite a mensagem: ")
    client.envia(msg) #Envia a mensagem
    if msg == "QUIT": #Se for de quit, sai do loop antes de esperar retorno
        break
    client.message, addr = client.recebe() #Recebe a mensagem e o endereço
    #Imprime a mensagem e o endereço do remetente
    print("{}:{}".format(addr,client.message.decode())) 
    if client.message.decode() == "QUIT": #Sai se for uma mensagem QUIT
        break