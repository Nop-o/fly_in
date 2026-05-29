import pygame


pygame.init()


screen = pygame.display.set_mode((1640, 1000))  #turn on screen

dog_img = pygame.image.load("../png/dog.png").convert() #get my image
dog_img = pygame.transform.scale(dog_img,
                                (dog_img.get_width() * 0.5,
                                dog_img.get_height() * 0.5)) #resize the image
dog_img.set_colorkey((255, 255, 255))

os_img = pygame.image.load("../png/os.png").convert() #get my image
os_img = pygame.transform.scale(os_img,
                                (os_img.get_width() * 0.8,
                                os_img.get_height() * 0.8)) #resize the image
os_img.set_colorkey((0, 0, 0))

dog_house_img = pygame.image.load("../png/dog_house.png").convert() #get my image
dog_house_img = pygame.transform.scale(dog_house_img,
                                      (dog_house_img.get_width() * 0.8,
                                      dog_house_img.get_height() * 0.8)) #resize the image
dog_house_img.set_colorkey((255, 255, 255))

running = True #cond to keep screen on
x = 0
clock = pygame.time.Clock()

while running: #to keep screen on

    screen.fill((0, 0, 0)) # refresh the background to black (255, 255, 255) is white
    screen.blit(dog_img, (x, 30)) #render the image
    screen.blit(os_img, (x, 500)) #render the image
    screen.blit(dog_house_img, (x, 800)) #render the image
    x += 1
    for event in pygame.event.get():
        if event.zone == pygame.QUIT: #if cross is clicked
            running = False
    pygame.display.flip() #show the rendered image

    clock.tick(60) #time of refresh per sec
pygame.quit()

