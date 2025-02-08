import pygame
import os
import random

pygame.init()

LARGURA_TELA  = 800
ALTURA_TELA  = int(LARGURA_TELA  * 0.8)

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('Pixel Shooter')

relogio = pygame.time.Clock()
FPS = 60

GRAVIDADE = 0.6
TAMANHO_TILE = 40

movendo_esquerda = False
movendo_direita = False
atirando = False

#bala
imagem_bala = pygame.image.load('assets/img/icons/bala.png').convert_alpha()
#caixas de itens
imagem_caixa_vida = pygame.image.load('assets/img/icons/caixa_de_saude.png').convert_alpha()
imagem_caixa_municao = pygame.image.load('assets/img/icons/caixa_de_municao.png').convert_alpha()
caixas_itens = {
    'Vida'   : imagem_caixa_vida,
    'Municao'    : imagem_caixa_municao,
}

COR_DE_FUNDO = (144, 201, 120)
VERMELHO  = (255, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
PRETO = (0, 0, 0)

#define fonte
fonte = pygame.font.SysFont('Futura', 30)

def desenhar_texto(texto, fonte, cor_texto, x, y):
    imagem = fonte.render(texto, True, cor_texto)
    tela.blit(imagem, (x, y))

def desenha_fundo():
    tela.fill(COR_DE_FUNDO)
    pygame.draw.line(tela, VERMELHO, (0, 300), (LARGURA_TELA, 300))

class Soldado(pygame.sprite.Sprite):
    def __init__(self, tipo_personagem, x, y, escala, velocidade, municao):
        pygame.sprite.Sprite.__init__(self)
        self.vivo = True
        self.tipo_personagem = tipo_personagem
        self.velocidade = velocidade
        self.municao = municao
        self.municao_inicial = municao
        self.cooldown_tiro = 0
        self.vida = 100
        self.vida_maxima = self.vida
        self.direcao = 1
        self.vel_y = 0
        self.pular = False
        self.no_ar = True
        self.virado = False
        self.lista_de_animacao = []
        self.frame_index = 0
        self.acao = 0
        self.update_time = pygame.time.get_ticks()
        # variáveis específicas da IA
        self.contador_movimento = 0
        self.visao = pygame.Rect(0, 0, 150, 20)
        self.ocioso = False
        self.contador_ocioso = 0

        #carregar a imagens do jogador
        tipos_de_animacao = ['Idle', 'Run', 'Jump', 'Death']
        for animacao in tipos_de_animacao:
            temp_lista = []
            num_de_frames = len(os.listdir(f'assets/img/{self.tipo_personagem}/{animacao}'))
            for i in range(num_de_frames):
                img = pygame.image.load(f'assets/img/{tipo_personagem}/{animacao}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width()/escala), int(img.get_height()/escala)))
                temp_lista.append(img)
            self.lista_de_animacao.append(temp_lista)
        self.imagem = self.lista_de_animacao[self.acao][self.frame_index]
        self.rect = self.imagem.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animacao()
        self.verifica_vivo()
        # atualiza cooldown
        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1

    def mover(self, movendo_esquerda, movendo_direita):

        dx = 0
        dy = 0

        if movendo_esquerda:
            dx = -self.velocidade
            self.virado = True
            self.direcao = -1
        if movendo_direita:
            dx = self.velocidade
            self.virado = False
            self.direcao = 1

        if self.pular == True and self.no_ar == False:
            self.vel_y = -11
            self.pular = False
            self.no_ar = True

        #aplica a gravidade
        self.vel_y += GRAVIDADE
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #checa a colisao com o chao
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.no_ar = False

        self.rect.x += dx
        self.rect.y += dy

    def atira(self):
        if self.cooldown_tiro == 0 and self.municao > 0:
            self.cooldown_tiro = 20
            bala = Bala(self.rect.centerx + (0.6 * self.rect.size[0] * self.direcao), self.rect.centery, self.direcao)
            grupo_balas.add(bala)
            # reduz munição
            self.municao -= 1

    def ia(self):
        if self.vivo and jogador.vivo:  # Assuming 'player' is now 'jogador'
            if self.ocioso == False and random.randint(1, 200) == 1:
                self.atualiza_acao(0)  # 0: ocioso
                self.ocioso = True
                self.contador_ocioso = 50
            # verifica se a IA está perto do jogador
            if self.visao.colliderect(jogador.rect):
                # para de correr e encara o jogador
                self.atualiza_acao(0)  # 0: ocioso
                # atira
                self.atira()
            else:
                if self.ocioso == False:
                    if self.direcao == 1:
                        ia_movendo_direita = True
                    else:
                        ia_movendo_direita = False
                    ia_movendo_esquerda = not ia_movendo_direita
                    self.mover(ia_movendo_esquerda, ia_movendo_direita)
                    self.atualiza_acao(1)  # 1: correndo
                    self.contador_movimento += 1
                    # atualiza a visão da IA conforme o inimigo se move
                    self.visao.center = (self.rect.centerx + 75 * self.direcao, self.rect.centery)

                    if self.contador_movimento > TAMANHO_TILE:
                        self.direcao *= -1
                        self.contador_movimento *= -1
                else:
                    self.contador_ocioso -= 1
                    if self.contador_ocioso <= 0:
                        self.ocioso = False

    def update_animacao(self):
        ANIMATION_COOLDOWN = 100
        self.imagem = self.lista_de_animacao[self.acao][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.lista_de_animacao[self.acao]):
            if self.acao == 3:
                self.frame_index = len(self.lista_de_animacao[self.acao]) - 1
            else:
                self.frame_index = 0

    def atualiza_acao(self, nova_acao):
        if nova_acao != self.acao:
            self.acao = nova_acao
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def verifica_vivo(self):
        if self.vida <= 0:
            self.vida = 0
            self.velocidade = 0
            self.vivo = False
            self.atualiza_acao(3)

    def desenho(self):
        tela.blit(pygame.transform.flip(self.imagem, self.virado, False), self.rect)

class CaixaItem(pygame.sprite.Sprite):
    def __init__(self, tipo_item, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.tipo_item = tipo_item
        self.image = caixas_itens[self.tipo_item]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TAMANHO_TILE // 2, y + (TAMANHO_TILE - self.image.get_height()))

    def update(self):
        #verifica se o jogador pegou a caixa
        if pygame.sprite.collide_rect(self, jogador):  # Assuming 'player' is now 'jogador'
            #verifica que tipo de caixa era
            if self.tipo_item == 'Vida':
                jogador.vida += 25
                if jogador.vida > jogador.vida_maxima:
                    jogador.vida = jogador.vida_maxima
            elif self.tipo_item == 'Municao':
                jogador.municao += 15
            #remove a caixa de item
            self.kill()

class BarraVida():
    def __init__(self, x, y, vida, vida_maxima):
        self.x = x
        self.y = y
        self.vida = vida
        self.vida_maxima = vida_maxima

    def desenhar(self, vida):
        #atualiza com a nova vida
        self.vida = vida
        #calcula a proporção da vida
        proporcao = self.vida / self.vida_maxima
        pygame.draw.rect(tela, PRETO, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(tela, VERMELHO, (self.x, self.y, 150, 20))
        pygame.draw.rect(tela, VERDE, (self.x, self.y, 150 * proporcao, 20))

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.velocidade = 10
        self.image = imagem_bala
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direcao = direcao

    def update(self):
        #move bala
        self.rect.x += (self.direcao * self.velocidade)
        #verifica se bala saiu da tela
        if self.rect.right < 0 or self.rect.left > LARGURA_TELA:
            self.kill()

        #verifica colisão com personagens
        if pygame.sprite.spritecollide(jogador, grupo_balas, False):
            if jogador.vivo:
                jogador.vida -= 5
                self.kill()
        #colisão com inimigo
        for inimigo in grupo_inimigos:
            if pygame.sprite.spritecollide(inimigo, grupo_balas, False):
                if inimigo.vivo:
                    inimigo.vida -= 25
                    self.kill()

#cria grupos de sprites
grupo_inimigos = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()
grupo_caixas_itens = pygame.sprite.Group()

#temporário - cria caixas de itens
caixa_item = CaixaItem('Vida', 100, 260)
grupo_caixas_itens.add(caixa_item)
caixa_item = CaixaItem('Municao', 400, 260)
grupo_caixas_itens.add(caixa_item)

jogador = Soldado('player',200,200, 3, 5, 10)
barra_vida = BarraVida(10, 10, jogador.vida, jogador.vida)
inimigo = Soldado('enemy', 500,200,3,5,20)
inimigo2 = Soldado('enemy', 300,200,3,5,20)
grupo_inimigos.add(inimigo)
grupo_inimigos.add(inimigo2)

rodando = True
while rodando:

    relogio.tick(FPS)
    desenha_fundo()
    # mostra a vida do jogador
    barra_vida.desenhar(jogador.vida)
    # mostra munição
    desenhar_texto(f'Balas:', fonte, BRANCO, 10, 35)
    for x in range(jogador.municao):
        tela.blit(imagem_bala, (90 + (x * 10), 40))

    jogador.update()
    jogador.desenho()

    for inimigo in grupo_inimigos:
        inimigo.ia()
        inimigo.update()
        inimigo.desenho()

    grupo_balas.update()
    grupo_caixas_itens.update()

    grupo_balas.draw(tela)
    grupo_caixas_itens.draw(tela)

    if jogador.vivo:
        if atirando:
            jogador.atira()
        if jogador.no_ar:
            jogador.atualiza_acao(2)# jump
        elif movendo_esquerda or movendo_direita:
            jogador.atualiza_acao(1)# run
        else:
            jogador.atualiza_acao(0)# idle
        jogador.mover(movendo_esquerda, movendo_direita)

    for evento in pygame.event.get():
        #quit
        if evento.type == pygame.QUIT:
            rodando = False
        #apertando o botao
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                movendo_esquerda = True
            if evento.key == pygame.K_d:
                movendo_direita = True
            if evento.key == pygame.K_SPACE:
                atirando = True
            if evento.key == pygame.K_w and jogador.vivo:
                jogador.pular = True
            if evento.key == pygame.K_ESCAPE:
                rodando = False

        # soltando o botao
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_a:
                movendo_esquerda = False
            if evento.key == pygame.K_d:
                movendo_direita = False
            if evento.key == pygame.K_SPACE:
                atirando = False

    pygame.display.update()

pygame.quit()