import pygame
from pygame.time import Clock

pygame.init()

largura_tela = 800
altura_tela = 600

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Pixel Shooter')

relogio = pygame.time.Clock()
FPS = 60


movendo_esquerda = False
movendo_direita = False

fundo = (144, 201, 120)

def desenho_fundo():
    tela.fill(fundo)

class Soldado(pygame.sprite.Sprite):
    def __init__(self, tipo_personagem, x, y, escala, velocidade):
        pygame.sprite.Sprite.__init__(self)
        self.tipo_personagem = tipo_personagem
        self.velocidade = velocidade
        self.direcao = 1
        self.virado = False
        img = pygame.image.load(f'assets/img/{tipo_personagem}/Idle/0.png')
        self.imagem = pygame.transform.scale(img, (int(img.get_width()/escala), int(img.get_height()/escala)))
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

        self.rect.x += dx
        self.rect.y += dy

    def desenho(self):
        tela.blit(pygame.transform.flip(self.imagem, self.virado, False), self.rect)

jogador = Soldado('player',200,200, 3, 5)



rodando = True
while rodando:

    relogio.tick(FPS)
    desenho_fundo()
    jogador.desenho()
    jogador.mover(movendo_esquerda, movendo_direita)


    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        #apertando o botao
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                movendo_esquerda = True
            if evento.key == pygame.K_d:
                movendo_direita = True
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