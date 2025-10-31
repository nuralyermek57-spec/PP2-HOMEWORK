import pygame
import math
import datetime

pygame.init()
screen = pygame.display.set_mode((700, 700))
done = False
clock = pygame.time.Clock()
center = (350, 350)

base_micky_image = pygame.image.load("base_micky.jpg")
second_image = pygame.image.load("second.png")
second_image = pygame.transform.scale(second_image, (40, 410))
minute_image = pygame.image.load("images/minute_arrow.png")
minute_image = pygame.transform.scale(minute_image, (600, 600))

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        screen.fill((255, 255, 255))

        screen.blit(base_micky_image, (100, 100))
        base_micky_image = pygame.transform.scale(base_micky_image, (500, 500))

        now = datetime.datetime.now()
        seconds = now.second
        minutes = now.minute

        second_angle = -seconds * 6
        minute_angle = -minutes * 6 - seconds / 10

        rotated_second = pygame.transform.rotate(second_image, second_angle)
        rotated_minute = pygame.transform.rotate(minute_image, minute_angle)
        
        rect_second = rotated_second.get_rect(center=center)
        rect_minute = rotated_minute.get_rect(center=center)

        screen.blit(rotated_minute, rect_minute)

        screen.blit(rotated_second, rect_second)

        clock.tick(60)

        pygame.display.flip()