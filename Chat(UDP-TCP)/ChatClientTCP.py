import socket

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #UDP
        self.server = "192.168.15.5" #Ip
        self.port = 41929 #Porta
        self.message = "initial"
        self.client.connect((self.server,self.port))

    def envia(self, msg): #Envia os dados ao servidor e retorna a resposta
        try:
            self.client.send(msg.encode('UTF-8')) #Faz o encode para utf-8, e manda pelo socket criado da instância
        except socket.error as e:
            print(e)
    
    def recebe(self):
        return self.client.recv(2048).decode() #Recebe a resposta pelo socket

client = Client() #Instância o socket do cliente
msg = ""
while  True:
    msg = input("Digite a mensagem: ")
    client.envia(msg) #Envia a mensagem
    if msg == "QUIT": #Se for de quit, sai do loop antes de esperar retorno
        break
    client.message = client.recebe() #Recebe a confirmação
    print("{}:{}".format("Servidor",client.message)) #Imprime a mensagem
    if client.message == "QUIT":
        break