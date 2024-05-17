import pygame
import pymunk
import pymunk.pygame_util

pygame.init()
size = 800, 800
display = pygame.display.set_mode(size)  # 800 x 800 크기의 영역을 잡는다
# positive_y_is_up = True  # 좌하단을 0,0으로 만든다.
# pygame과 pymunk의 좌표계가 다른걸 일치시킨다. pygame 기준으로 바꿈. 좌상단이 0, 0
draw_options = pymunk.pygame_util.DrawOptions(display)

clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, 1000
FPS = 50  # 50 fps

# pymunk 는 왼쪽 아래가 0, 0, pygame은 왼쪽 위가 0,0 이라서 다르다.
# 이를 보정하기 위한 함수
def convert_coordinates(point):
    return point[0], 800-point[1]

# body는 물체의 질량을 정의
# shape는 물체의 모양을 정의 (충돌감지를 위해)
body = pymunk.Body(mass=1, moment=10)
body.position = 400, 400
shape = pymunk.Circle(body, 10)
shape.density = 1
shape.elasticity = 0.95

# segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
b0 = space.static_body
segment_shape = pymunk.Segment(b0, (0, 750), (800, 750), 5)
segment_shape.elasticity = 1
space.add(body, shape)
space.add(segment_shape)

#space.add(segment_shape)

def game():
    while True:
        for event in pygame.event.get():  # 이벤트 루프임. 안하면 먹통이 됨.
            if event.type == pygame.QUIT:
                return
        display.fill((255, 255, 255))
        x, y = body.position
        pygame.draw.circle(display, (255, 0, 0), (x, y), 10)
        pygame.draw.line(display, (0, 0, 0), (0, 750), (800, 750), 5)
        pygame.display.update()  # 화면 그리기
        clock.tick(FPS)  # 지정한 fps가 되도록 delay를 준다.
        space.step(1/FPS)  # 물리엔진은 1/FPS만큼 진행한다.

game()
pygame.quit()