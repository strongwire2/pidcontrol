import pygame
import pymunk

pygame.init()
display = pygame.display.set_mode((800, 800))  # 800 x 800 크기의 영역을 잡는다
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 50  # 50 fps


def game():
    while True:
        for event in pygame.event.get():  # 이벤트 루프임. 안하면 먹통이 됨.
            if event.type == pygame.QUIT:
                return
        pygame.display.update()  # 화면 그리기
        clock.tick(FPS)  # 지정한 fps가 되도록 delay를 준다.
        space.step(1/FPS)  # 물리엔진은 1/FPS만큼 진행한다.

game()
pygame.quit()