import pygame
import os

pygame.init()

largura_tela = 800
altura_tela = int(largura_tela * 0.8)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Pixel Shooter')

relogio = pygame.time.Clock()
FPS = 60


GRAVIDADE = 0.75

movendo_esquerda = False
movendo_direita = False

fundo = (144, 201, 120)
linha_vermelha = (255, 0, 0)

def desenho_fundo():
    tela.fill(fundo)
    pygame.draw.line(tela, linha_vermelha, (0, 300), (largura_tela, 300))

class Soldado(pygame.sprite.Sprite):
    def __init__(self, tipo_personagem, x, y, escala, velocidade):
        pygame.sprite.Sprite.__init__(self)
        self.vivo = True
        self.tipo_personagem = tipo_personagem
        self.velocidade = velocidade
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
        tipos_de_animacao = ['Idle', 'Run', 'Jump']
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

    def update_animacao(self):
        ANIMATION_COOLDOWN = 100
        self.imagem = self.lista_de_animacao[self.acao][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.lista_de_animacao[self.acao]):
            self.frame_index = 0

    def updade_acao(self, nova_acao):
        if nova_acao != self.acao:
            self.acao = nova_acao
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def desenho(self):
        tela.blit(pygame.transform.flip(self.imagem, self.virado, False), self.rect)

jogador = Soldado('player',200,200, 3, 5)



rodando = True
while rodando:

    relogio.tick(FPS)
    desenho_fundo()
    jogador.update_animacao()
    jogador.desenho()


    if jogador.vivo:
        if jogador.no_ar:
            jogador.updade_acao(2)
        elif movendo_esquerda or movendo_direita:
            jogador.updade_acao(1)
        else:
            jogador.updade_acao(0)
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




    pygame.display.update()

pygame.quit()