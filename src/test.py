import pygame


pygame.init()


screen = pygame.display.set_mode((1640, 1000))  #turn on screen

pikachu_img = pygame.image.load("../png/pikachu.png").convert() #get my image
pikachu_img = pygame.transform.scale(pikachu_img,
                                     (pikachu_img.get_width() * 0.2,
                                     pikachu_img.get_height() * 0.2))

shrek_img = pygame.image.load("../png/shrek.png").convert() #get my image
shrek_img = pygame.transform.scale(shrek_img,
                                   (shrek_img.get_width() * 0.8,
                                   shrek_img.get_height() * 0.8))

running = True #cond to keep screen on
x = 0
clock = pygame.time.Clock()

while running: #to keep screen on

    screen.fill((0, 0, 0)) # refresh the background to black (255, 255, 255) is white
    screen.blit(shrek_img, (x, 30)) #render the image
    screen.blit(pikachu_img, (x, 500)) #render the image
    x += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if cross is clicked
            running = False
    pygame.display.flip() #show the rendered image

    clock.tick(60) #time of refresh per sec
pygame.quit()

