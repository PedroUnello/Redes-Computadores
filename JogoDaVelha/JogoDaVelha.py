#Nathan Silva Macena - 41990404
#Pedro Unello Neto - 41929713

import pygame as pg
import re
import random
import sys

def IA(m,lado,alea): #Função para calcular a jogada do bot, usando recursão e parametros como flags
    loopAnterior,jogada = [-1,-1], [-1,-1]
    contador,controle = 0, 0
    indicePleno = [[0,1,2],[3,4,5],[6,7,8]]
    for i in range(len(m)):
        for l in range(len(m[i])):
            if m[i][l] == lado:
                contador +=1
    for j in range(contador):
        for i in range(len(m)):
            for l in range(len(m[i])):
                if m[i][l] == lado and controle < 1 and (i != loopAnterior[0] or l != loopAnterior[1]):   
                    copoI = [i,l]
                    controle += 1
                if m[i][l] == lado:
                    if copoI[0] != i or copoI[1] != l:

                        if copoI[1] == copoI[0] and i == l:
                            if copoI[0] == 0 and i == 1 or copoI[0] == 1 and i == 0:
                                jogada = [2,2]
                            elif copoI[0] == 1 and i == 2 or copoI[0] == 2 and i == 1:
                                jogada = [0,0]
                            elif copoI[0] == 0 and i == 2 or copoI[0] == 2 and i == 0:
                                jogada = [1,1]     

                        elif copoI[1] != l and copoI[0] != i:
                            if ((copoI[0] == 0 and copoI[1] == 2) and (l == 0 and i == 2)) or ((copoI[0] == 2 and copoI[1] == 0) and (i == 0 and l == 2)):
                                jogada = [1,1]
                            elif ((copoI[0] == 0 and copoI[1] == 2) and (l == 1 and i == 1)) or ((copoI[0] == 1 and copoI[1] == 1) and (i == 0 and l == 2)):
                                jogada = [2,0]
                            elif ((copoI[0] == 2 and copoI[1] == 0) and (l == 1 and i == 1)) or ((copoI[0] == 1 and copoI[1] == 1) and (i == 2 and l == 0)):
                                jogada = [0,2]
                            
                        elif copoI[1] == l and copoI[0] != i:

                            if i == 1 and copoI[0] == 0 or copoI[0] == 1 and i == 0:
                                jogada = [2,l]
                            elif i == 0 and copoI[0] == 2 or i == 2 and copoI[0] == 0:
                                jogada = [1,l]
                            elif i == 1 and copoI[0] == 2 or i == 2 and copoI[0] == 1:
                                jogada = [0,l]
                                        
                        elif copoI[0] == i and copoI[1] != l:

                            if l == 1 and copoI[1] == 0 or copoI[1] == 1 and l == 0:
                                jogada = [i,2]
                            elif l == 0 and copoI[1] == 2 or l == 2 and copoI[1] == 0:
                                jogada = [i,1]
                            elif l == 1 and copoI[1] == 2 or l == 2 and copoI[1] == 1:
                                jogada = [i,0]
                                
                    if jogada[0] == -1 and jogada[1] == -1:
                        pass
                    else:
                        if m[jogada[0]][jogada[1]] == 0:
                            return indicePleno[jogada[0]][jogada[1]]
                        
        controle = 0
        loopAnterior = copoI

    while alea:
        jogada = [random.randint(0,2),random.randint(0,2)]
        if m[jogada[0]][jogada[1]] != lado and m[jogada[0]][jogada[1]] == 0:
            return indicePleno[jogada[0]][jogada[1]]
        
    if lado == "X":
        retorno = IA(m,"O",True)
    else:
        retorno = IA(m,"X",True)

    return retorno

def ManipularPlacar(modo,imprimir,filtrar): #função com parametros opcionais como flags, para manipular e em casos alterar o placar
    placarGeral = open("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/placar.txt", modo)
    texto = placarGeral.read().splitlines()
    placarGeral.close()
    if imprimir:
        textoOrd = [0] * len(texto)
        for i in range(len(texto)):
            textoOrd[i] = re.findall(".[0-9][0-9]$", texto[i])[0]
        textoOrd.sort(reverse=True)
        for i in range(len(textoOrd)):
            for l in range(len(texto)):
                if re.findall(".[0-9][0-9]$", texto[l])[0] == textoOrd[i]:
                    if texto[l] not in textoOrd:
                        textoOrd[i] = texto[l]
        ranking = [0] * len(textoOrd)
        for i in range(len(textoOrd)):
            ranking[i] = str(i + 1) + " - "
        if filtrar:
            match = []
            for i in range(len(textoOrd)):
                if re.match(searchPatter, textoOrd[i]):
                    match += [re.findall(searchPatter, textoOrd[i])[0]]
            ranking = [0] * len(match)
            for i in range(len(match)):
                ranking[i] = str(i+1) + " - "
            textoOrd = match
        ImprimirVisual(ranking, None, None, 330, 465, 25, 25, cor=(0, 0, 0))
        ImprimirVisual(textoOrd, None, None, 330, 505, 25, 25, cor=(0, 0, 0))
    else:
        return texto

def PrepararBotao(jaEscolhidos): #função idiota para escoher cor, não préviamente escolhida
    while True:
        escolha = random.randint(1,5)
        if escolha not in jaEscolhidos:
            jaEscolhidos.append(escolha)
            return str(escolha)

def CompararPosição(Mouse, Posição, Tamanho): #função para procurar a posição do mouse dentro dos limites fornecidos
    if Mouse[1] >= Posição[1] and Mouse[1] <= Posição[1] + Tamanho[1]:
        if Mouse[0] >= Posição[0] and Mouse[0] <= Posição[0] + Tamanho[0]:
            return True
    return False

def ImprimirVisual(texto, fonte = None, tamanho = None, alturaInicial = None, posiçãoInicial = None, espaço = None, limite = None, cor = None): #Função com parametros opcionais para imprimir texto na janela do pygame
    fonte = fonte or "Helvetiva"
    tamanho = tamanho or 30
    alturaInicial = alturaInicial or 15
    posiçãoInicial = posiçãoInicial or False
    espaço = espaço or 15
    limite = limite or len(texto)
    cor = cor or (0,0,255)
    fonteTexto = pg.font.SysFont(fonte,tamanho)
    alturaT = alturaInicial
    if limite > len(texto):
        limite = len(texto)
    for index in range(limite):
        if posiçãoInicial == False:
            larguraT = fonteTexto.size(texto[index])[0]
            larguraDinamica = (largura//2) - (larguraT//2)
        else:
            larguraDinamica = posiçãoInicial
        tImprimir = fonteTexto.render(texto[index], True, cor)
        screen.blit(tImprimir, [larguraDinamica,alturaT])
        alturaT += espaço

def Checar(matriz): #Função para checar estado do jogo da velha
    contDiagP, contDiagS = ["","",""],["","",""]
    
    for i in range(len(matriz)):
        contLin,contCol = ["","",""],["","",""]

        if matriz[i][i] == "X":
            contDiagP[i] = "X"
        elif matriz[i][i] == "O":
            contDiagP[i] = "O"
        if matriz[i][2-i] == "X":
            contDiagS[i] = "X"
        elif matriz[i][2-i] == "O":
            contDiagS[i] = "O"
        for j in range(len(matriz[i])):
            if matriz[i][j] == "X":
                contLin[j] = "X"
            elif matriz[i][j] == "O":
                contLin[j] = "O"
            if matriz[j][i] == "X":
                contCol[j] = "X"
            elif matriz[j][i] == "O":
                contCol[j] = "O"
                
        if contLin == ["X","X","X"] or contCol == ["X","X","X"] or contDiagS == ["X","X","X"] or contDiagP == ["X","X","X"]:
            return True, "X"
        if contLin == ["O","O","O"] or contCol == ["O","O","O"] or contDiagS == ["O","O","O"] or contDiagP == ["O","O","O"]:
            return True, "O"
    return False, None

class Jogador():
    valido = False
    def __init__(self, Nome, Pontuação, Lado): #Construtor/instaciador.
        self.Nome = Nome
        self.Pontuação = Pontuação
        self.Lado = Lado

    def Jogar(self, pos,colliders): #Metodo para criar a jogada, caso possível na colisão fornecida
        for i in range(len(colliders)):
            if colliders[i].collidepoint(pos[0],pos[1]):
                posMatriz = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
                posMatriz = posMatriz[i]
                if tabuleiro.matriz[posMatriz[0]][posMatriz[1]] != "X" and tabuleiro.matriz[posMatriz[0]][posMatriz[1]] != "O":
                    tabuleiro.CriarPontos(self.Lado[0], posMatriz)
                    Ijogada = pg.image.load(str(self.Lado[1]))
                    screen.blit(Ijogada,(colliders[i][0]+10,colliders[i][1]-10))
                    print(tabuleiro.matriz)
                    tabuleiro.histJogada = posMatriz
                    self.valido = True
                else:
                    self.valido = False

    def Voltar(self): #metodo para voltar turno
        tabuleiro.matriz[tabuleiro.histJogada[0]][tabuleiro.histJogada[1]] = 0
        screen.fill((0,0,0))
        screen.blit(tabuleiro.Imagem, (0, 0))
        for i in range(len(tabuleiro.matriz)):
            for j in range(len(tabuleiro.matriz)):
                if tabuleiro.matriz[i][j] == "O":
                    Ijogada = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/O1.png")
                    screen.blit(Ijogada,(slots[3*i+j][0]+10,slots[3*i+j][1]-10))
                if tabuleiro.matriz[i][j] == "X":
                    Ijogada = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/X1.png")
                    screen.blit(Ijogada,(slots[3*i+j][0]+10,slots[3*i+j][1]-10))
        return (0,0)

    def Desistir(self): #metodo para desistir do jogo
        for i in range(len(tabuleiro.matriz)):
            for j in range(len(tabuleiro.matriz)):
                if self.Lado[0] == "X":
                    tabuleiro.matriz[i][j] = "O"
                else:
                    tabuleiro.matriz[i][j] = "X"
        screen.fill((0,0,0))
        backGround = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/BackGround.jpeg")
        premio = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Premio1.png")
        screen.blit(backGround, (0, 0))
        screen.blit(premio, (0, 0))
        ImprimirVisual(["Jogador", " "+self.Nome, "Desistiu"],espaço = 27, alturaInicial=480, posiçãoInicial=535, cor=(0, 255, 0))
        self.valido = True
        return (0,0)

class Botão():

    def __init__(self,Imagem,Posição,Nome): #Construtor/instaciador.
        self.Imagem = Imagem
        self.Posição = Posição
        self.Nome = Nome

    def Ação(self, offsetX, offsetY): #metodo para blitar botão
        screen.blit(self.Imagem, self.Posição)
        ImprimirVisual(self.Nome, None, None, self.Posição[1] + offsetY, self.Posição[0] + offsetX)

    def __delete__(self): #metodo mágico para deletar referencia do objeto
        del self

class Tabuleiro():
    Imagem = ''
    ganhador,finalizado = False, False
    histJogada = []
    matriz = [[0,0,0],[0,0,0],[0,0,0]]

    def CriarPontos(self,lado,pos): #metodo para criar ponto no atributo tabuleiro.
        if lado != None:
            self.matriz[pos[0]][pos[1]] = lado

    def Status(self): #metodo para checar ganhador usando a função referente
        if Checar(self.matriz)[0]:
            self.finalizado = True
            if Checar(self.matriz)[1] != None:
                self.ganhador = Checar(self.matriz)[1]


pg.init() #Inicia bloco para atribuir variaveis necessárias
largura = 1000
altura = 1000
screen = pg.display.set_mode((largura, altura))
pg.display.set_caption("Jogo da Velha WIP")
screen.fill((0,0,0))
pg.display.flip()
menu = True
jogar, placar, créditos, enter, procurando, criando, jogandoM, jogandoS, jogando, Preparado = False, False, False, False, False, False, False, False, False, False
Jog1, Jog2 = None, None
lado,userInput = ["X","O"], ['']
contTurno = 0
pos = (0,0)
slots = [(400,430),(500,430),(600,430),(400,520),(500,520),(600,520),(400,610),(500,610),(600,610)]
colliders = [0] * 9 #Finaliza bloco para atribuir variaveis necessárias

while True: #laço de jogo, segura os outros laços de modos, visto que trabalha em laços referentes
    while menu: #enquanto permanecer no menu de jogo / laço de menu
        
        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0]:
                    pos = pg.mouse.get_pos()
                    print(pos)
                
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        if not Preparado:
            jaEscolhidos = []
            backGround = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/BackGround.jpeg")
            screen.blit(backGround, (0,0))
            BotãoJogar = Botão(pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Botão"+ PrepararBotao(jaEscolhidos) +".png"),(500,300),["Jogar"])
            BotãoPlacar = Botão(pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Botão"+ PrepararBotao(jaEscolhidos) +".png"),(500,400),["Placar"])
            BotãoSair = Botão(pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Botão"+ PrepararBotao(jaEscolhidos) +".png"),(500,500),["Sair"])
            BotãoCréditos = Botão(pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Botão"+ PrepararBotao(jaEscolhidos) +".png"),(500,600),["Créditos"])
            BotãoJogar.Ação(40,15)
            BotãoPlacar.Ação(40,15)
            BotãoSair.Ação(50,15)
            BotãoCréditos.Ação(20,15)
            Preparado = True

        if CompararPosição(pos, BotãoJogar.Posição, BotãoJogar.Imagem.get_rect().size):
            del BotãoJogar
            Tcor = str(random.randint(1,2))
            screen.fill((0,0,0))
            backGround = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/TabuD" + Tcor +".png")
            screen.blit(backGround, (0,0))
            tabuleiro = Tabuleiro()
            tabuleiro.matriz = [[0,0,0],[0,0,0],[0,0,0]]
            tabuleiro.Imagem = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Tabu" + Tcor + ".png")
            for i in range(9):
                colliders[i] = pg.Rect(slots[i],(85,95))
            Jog2,Jog1 = None, None
            Preparado = False
            jogar =True
            menu = False
            
        elif CompararPosição(pos, BotãoPlacar.Posição, BotãoPlacar.Imagem.get_rect().size):
            del BotãoPlacar
            screen.fill((0,0,0))
            backGround = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/BackGround.jpeg")
            placarBG = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Placar.png")
            screen.blit(backGround, (0,0))
            screen.blit(placarBG,(0,0))
            ManipularPlacar("r",True, False)
            placar = True
            menu = False
                
        elif CompararPosição(pos, BotãoSair.Posição, BotãoSair.Imagem.get_rect().size):
            pg.quit()
            sys.exit()

        elif CompararPosição(pos, BotãoCréditos.Posição, BotãoCréditos.Imagem.get_rect().size):
            del BotãoCréditos
            screen.fill((0,0,0))
            backGround = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/BackGround.jpeg")
            posti = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Postite.png")
            screen.blit(backGround, (0,0))
            screen.blit(posti,(0,0))
            ncréditos = ['Pedro Unello Neto','- 41929713','Nathan Silva Macena','- 41990404']
            ImprimirVisual(ncréditos, 'Lucida Grande', 30, 600, 480, 30, cor = (0,0,0))
            créditos = True
            menu, Preparado = False, False
                
        pg.display.flip()
        
    while placar: #enquanto permanecer no placar / laço de placar
        
        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0]:
                    pos = pg.mouse.get_pos()
                    print(pos)
                if barraPesquisa.collidepoint(event.pos):
                    pesquisa = not pesquisa
                    cor = corA
                else:
                    cor = corI
                    pesquisa = False
                    
            if event.type == pg.KEYDOWN:
                if pesquisa:
                    if event.key == pg.K_RETURN:
                        enter = True
                    elif event.key == pg.K_BACKSPACE:
                        userInput[0] = userInput[0][:-1]
                        pg.draw.rect(screen,(0,0,0),(50,50,tLargura,31))
                        
                    elif len(userInput[0]) < 20:
                        userInput[0] += event.unicode
                    
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        barraPesquisa = pg.Rect(50,50,90,30)
        corA = (0,255,0)
        corI = (0,180,0)
        BotãoVoltar = Botão(pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Botão1.png"),(250,300),["Voltar"])
        BotãoProcurar = Botão(pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Botão2.png"),(250,250),["Procurar"])
        BotãoVoltar.Ação(40,15)
        BotãoProcurar.Ação(25,16)

        if CompararPosição(pos, BotãoProcurar.Posição, BotãoProcurar.Imagem.get_rect().size):
            pesquisa = False
            procurando = True
            font = pg.font.Font(None, 32)
            
        elif CompararPosição(pos, BotãoVoltar.Posição, BotãoVoltar.Imagem.get_rect().size):
            del BotãoVoltar
            userInput = ['']
            menu = True
            placar, Preparado, Procurando = False, False, False

        if procurando:
            text = font.render(userInput[0], True, cor)
            tLargura = max(200,text.get_width() +10)
            barraPesquisa.w = tLargura
            pg.draw.rect(screen,(0,0,0),barraPesquisa)
            screen.blit(text, (barraPesquisa.x+5, barraPesquisa.y+5))
            pg.draw.rect(screen, cor, barraPesquisa, 2)
            
        if enter:
            procurando = False
            searchPatter = re.compile('^'+userInput[0] + '.*[0-9]$', re.IGNORECASE)
            screen.fill((0,0,0))
            backGround = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/BackGround.jpeg")
            placarBG = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Placar.png")
            screen.blit(backGround, (0,0))
            screen.blit(placarBG,(0,0))
            ManipularPlacar("r",True, True)
            userInput = ['']
        
        pg.display.flip()
        enter = False
        
    while créditos: #enquanto permanecer nos créditos / laço de crédito
        
        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0]:
                    pos = pg.mouse.get_pos()
                    print(pos)
                
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
        if not Preparado:
            BotãoVoltar = Botão(pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Botão3.png"),(520,450),["Voltar"])
            BotãoVoltar.Ação(40,15)
            Preparado = True
        
        if CompararPosição(pos, BotãoVoltar.Posição, BotãoVoltar.Imagem.get_rect().size):
            del BotãoVoltar
            menu = True
            Preparado, créditos = False, False
            
        pg.display.flip()
            
    while jogar: #enquanto permanecer no jogo / laço de jogo
        
        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:
                if jogando:
                    if pg.mouse.get_pressed()[0]:
                        pos = pg.mouse.get_pos()
                        print(pos)                        
                else:
                    if pg.mouse.get_pressed()[0] and not (CompararPosição(pos, BotãoMulti.Posição, (90,30)) or CompararPosição(pos, BotãoSingle.Posição, (90,30))):
                        pos = pg.mouse.get_pos()
                        print(pos)


            if event.type == pg.KEYDOWN:
                if criando:
                    if event.key == pg.K_RETURN:
                        enter = True
                    elif event.key == pg.K_BACKSPACE:
                        userInput[0] = userInput[0][:-1]
                        pg.draw.rect(screen,(0,0,0),(50,50,tLargura,31))
                    elif len(userInput[0]) < 20:
                        userInput[0] += event.unicode
              
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        if not jogando:
            if not Preparado:
                pg.time.delay(2000)
                screen.blit(tabuleiro.Imagem,(0,0))
                Preparado = True
            barraCriacao = pg.Rect(50,50,90,30)
            corA = (0,255,0)
            BotãoSingle = Botão(pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Botão2.png"),(355,300),["Single"])
            BotãoMulti = Botão(pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Botão4.png"),(640,300),["Multi"])
            BotãoVoltar = Botão(pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Botão5.png"),(495,720),["Voltar"])
            BotãoSingle.Ação(25,16)
            BotãoMulti.Ação(40,15)
            BotãoVoltar.Ação(40,15)

        if criando and not enter:
            text = font.render(userInput[0], True, corA)
            tLargura = max(200,text.get_width() +10)
            barraCriacao.w = tLargura
            pg.draw.rect(screen,(0,0,0),barraCriacao)
            screen.blit(text, (barraCriacao.x+5, barraCriacao.y+5))
            pg.draw.rect(screen, corA, barraCriacao, 2)

        if criando and enter:
            userInput[0] = userInput[0].lower()
            userInput[0] = userInput[0][0].upper() + userInput[0][1:]
            if Jog1 == None:
                Jog1 = Jogador(userInput[0],0,["X","/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/X1.png"])
            elif Jog2 == None:
                Jog2 = Jogador(userInput[0],0,["O","/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/O1.png"])
            userInput = ['']
            criando = False
            
        listaJogadores = [Jog1,Jog2]

        if CompararPosição(pos, BotãoVoltar.Posição, BotãoVoltar.Imagem.get_rect().size) and not jogando:
            del BotãoVoltar
            userInput = ['']
            menu = True
            Preparado, jogar, criando = False, False, False
            
        
        if CompararPosição(pos, BotãoMulti.Posição, BotãoMulti.Imagem.get_rect().size) or CompararPosição(pos, BotãoSingle.Posição, BotãoSingle.Imagem.get_rect().size) and not jogando:
            
            if CompararPosição(pos, BotãoMulti.Posição, BotãoMulti.Imagem.get_rect().size):
                if Jog1 == None or Jog2 == None:
                    font = pg.font.Font(None, 32)
                    criando = True
                else:
                    jogandoM = True
                    recompensa = 10
                pg.display.flip()
   
            if CompararPosição(pos, BotãoSingle.Posição, BotãoSingle.Imagem.get_rect().size):
                if Jog1 == None:
                    font = pg.font.Font(None,32)
                    criando = True
                else:
                    if random.randint(1,2) == 1:
                        Jog2 = Jog1
                        Jog1 = Jogador("Bot134679",0,["O","/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/O1.png"])
                    else:
                        Jog2 = Jogador("Bot134679",0,["O","/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/O1.png"])
                    jogandoS = True
                    recompensa = 5
                pg.display.flip()

            if jogandoS or jogandoM:    
                textoL = ManipularPlacar("r",False, False)
                for i in range(len(textoL)):
                    if re.match("\A" + str(Jog1.Nome), textoL[i]):
                        Jog1.Pontuação = int(re.findall(".[0-9][0-9]$",textoL[i])[0])
                    if re.match("\A" + str(Jog2.Nome), textoL[i]):
                        Jog2.Pontuação = int(re.findall(".[0-9][0-9]$",textoL[i])[0])
                pos = (0,0)
                screen.blit(tabuleiro.Imagem,(0,0))
                jogando = True
                
        if jogando:

            ImprimirVisual(["Vez de"],alturaInicial=310,posiçãoInicial=535,cor = (0,0,0))
            pg.draw.line(screen,(100,0,0),(460,300),(500,340),3)
            pg.draw.line(screen,(100,0,0),(500,300),(460,340),3)
            pg.draw.circle(screen,(0,0,100),(650,310),20,3)
            ImprimirVisual([Jog1.Nome], alturaInicial=265, posiçãoInicial=450, cor=(0, 0, 0))
            ImprimirVisual([Jog2.Nome], alturaInicial=265, posiçãoInicial=620, cor=(0, 0, 0))

            if Jog1.Nome == "Bot134679":
                if lado[contTurno%2] == "O":
                    pg.draw.line(screen,(255,0,0),(460,300),(500,340),3)
                    pg.draw.line(screen,(255,0,0),(500,300),(460,340),3)
                elif lado[contTurno%2] == "X":
                    pg.draw.circle(screen,(0,0,255),(650,310),20,3)
            else:
                if lado[contTurno%2] == "X":
                    pg.draw.line(screen,(255,0,0),(460,300),(500,340),3)
                    pg.draw.line(screen,(255,0,0),(500,300),(460,340),3)
                elif lado[contTurno%2] == "O":
                    pg.draw.circle(screen,(0,0,255),(650,310),20,3)

            if jogandoS:

                BotãoRetroceder = Botão(pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Botão4.png"),(595,720),["Retroceder"])
                BotãoDesistir = Botão(pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Botão5.png"),(395,720),["Desistir"])
                BotãoRetroceder.Ação(20,15)
                BotãoDesistir.Ação(30,15)
                if CompararPosição(pos, BotãoRetroceder.Posição, BotãoRetroceder.Imagem.get_rect().size) and contTurno != 0:
                    if Jog1.Nome != "Bot134679":
                        pos = Jog1.Voltar()
                    else:
                        pos = Jog2.Voltar()
                    contTurno -= 1
                if CompararPosição(pos, BotãoDesistir.Posição, BotãoDesistir.Imagem.get_rect().size):
                    if Jog1.Nome != "Bot134679":
                        pos = Jog1.Desistir()
                    else:
                        pos = Jog2.Desistir()

                jogadorAtual = listaJogadores[contTurno%2]
                if jogadorAtual.Nome == "Bot134679":
                    jogadaBot = IA(tabuleiro.matriz,jogadorAtual.Lado[0],False)
                    if jogadaBot != None:
                        pos = (slots[jogadaBot][0] + 50,slots[jogadaBot][1] +50)
                        jogadaBot = None
                jogadorAtual.Jogar(pos,colliders)
                if jogadorAtual.valido:
                    contTurno +=1
                    jogadorAtual.valido = False
                    jogadorAtual = None
                    pos = (0,0)
                    tabuleiro.Status()
                    pg.display.flip()
                    
            if jogandoM:
                jogadorAtual = listaJogadores[contTurno%2]
                jogadorAtual.Jogar(pos,colliders)
                if jogadorAtual.valido:
                    contTurno +=1
                    jogadorAtual.valido = False
                    jogadorAtual = None
                    pos = (0,0)
                    tabuleiro.Status()
                    pg.display.flip()
                
        if tabuleiro.finalizado or contTurno == 9:            
            if tabuleiro.finalizado:
                pg.time.delay(2000)
                screen.fill((0,0,0))
                backGround = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/BackGround.jpeg")
                premio = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Premio1.png")
                screen.blit(backGround,(0,0))
                screen.blit(premio,(0,0))
                textoL = ManipularPlacar("r",False,False)
                placarGeral = open("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/placar.txt", "w")

                if Jog2.Nome != "Bot134679" and Jog1.Nome != "Bot134679":
                    existente = False
                    if contTurno%2 == 0:
                        jogadorVencedor = Jog2
                    elif contTurno % 2 == 1:
                        jogadorVencedor = Jog1
                    jogadorVencedor.Pontuação += recompensa
                    ImprimirVisual(["Vencedor","********","{}!".format(jogadorVencedor.Nome)],alturaInicial = 480, posiçãoInicial = 530,espaço = 20, cor = (255,0,0))
                    searchPatter = re.compile("^" + str(jogadorVencedor.Nome) + ".*[0-9]$")
                    
                    for i in range(len(textoL)):
                        if re.match(searchPatter, textoL[i]):
                            existente = True
                            textoL[i] = searchPatter.sub(str(jogadorVencedor.Nome) + " - " + str(jogadorVencedor.Pontuação),textoL[i])
                    if not existente:
                        textoL.append(str(jogadorVencedor.Nome) + " - " + str(jogadorVencedor.Pontuação))

                else:
                    ImprimirVisual(["Vencedor","********","Máquina!"],espaço = 27,alturaInicial = 480, posiçãoInicial = 530, cor = (0,255,0))
                    
                texto = "\n"
                texto = texto.join(textoL)    
                placarGeral.write(texto)
                placarGeral.close()
                pg.display.flip() 

            else:
                ImprimirVisual(["Empate <-> Deu velha"], alturaInicial = 750, posiçãoInicial = 470,cor = (0,0,0))
                pg.display.flip()
                
            pg.time.delay(4000)
            del tabuleiro
            contTurno = 0
            jogadorVencedor = None
            jogandoM, jogandoS, jogando, Preparado, jogar = False, False, False, False, False
            menu = True
            
        pg.display.flip()
        enter = False