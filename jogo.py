from urllib.request import build_opener

import pygame
import os

pygame.init()

LARGURA_TELA  = 800
ALTURA_TELA  = int(LARGURA_TELA  * 0.8)

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('Pixel Shooter')

relogio = pygame.time.Clock()
FPS = 60

GRAVIDADE = 0.75

movendo_esquerda = False
movendo_direita = False
atirando = False

#bala
imagem_bala = pygame.image.load('assets/img/icons/bala.png').convert_alpha()

COR_DE_FUNDO = (144, 201, 120)
LINHA_VERMELHA = (255, 0, 0)

def desenha_fundo():
    tela.fill(COR_DE_FUNDO)
    pygame.draw.line(tela, LINHA_VERMELHA, (0, 300), (LARGURA_TELA, 300))

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
        if pygame.sprite.spritecollide(inimigo, grupo_balas, False):
            if inimigo.vivo:
                inimigo.vida -= 25
                self.kill()

#cria grupos de sprites
grupo_balas = pygame.sprite.Group()

jogador = Soldado('player',200,200, 3, 5, 10)
inimigo = Soldado('enemy', 400,200,3,5,20)


rodando = True
while rodando:

    relogio.tick(FPS)
    desenha_fundo()

    jogador.update()
    jogador.desenho()

    inimigo.update()
    inimigo.desenho()

    grupo_balas.update()
    grupo_balas.draw(tela)


    if jogador.vivo:
        if atirando:
            jogador.atira()
        if jogador.no_ar:
            jogador.atualiza_acao(2)
        elif movendo_esquerda or movendo_direita:
            jogador.atualiza_acao(1)
        else:
            jogador.atualiza_acao(0)
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