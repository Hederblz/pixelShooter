import pygame


pygame.init()

largura_tela = 800
altura_tela = 600

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Pixel Shooter')

movendo_esquerda = False
movendo_direita = False

class Soldado(pygame.sprite.Sprite):
    def __init__(self, x, y, escala):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/img/player/Idle/0.png')
        self.imagem = pygame.transform.scale(img, (int(img.get_width() * escala), int(img.get_height() * escala)))
        self.rect = self.imagem.get_rect()
        self.rect.center = (x, y)

    def desenho(self):
        tela.blit(self.imagem, self.rect)

jogador = Soldado(200,200,2)



rodando = True
while rodando:


    jogador.desenho()


    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False



        tela.fill((140,40,0))


    pygame.display.update()

pygame.quit()