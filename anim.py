import pygame
import pymunk
import pymunk.pygame_util


class App:
    def __init__(self):
        pygame.init()
        self.size = (800, 800)
        self.fps = 50
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(self.size)  # 800 x 800 크기의 영역을 잡는다
        # pygame과 pymunk의 좌표계가 다른걸 일치시킨다. pygame 기준으로 바꿈. 좌상단이 0, 0
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True

        self.space = pymunk.Space()
        self.space.gravity = 0, 1000

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    # pygame.image.save(self.screen,'intro.png')
            self.screen.fill((255, 255, 255))  # white background
            # debug_draw를 쓰면 직접 pygame에 그리지 않아도 됨. 알아서 그려줌
            self.space.debug_draw(self.draw_options)
            pygame.display.update()
            self.clock.tick(self.fps)  # 지정한 fps가 되도록 delay를 준다.
            self.space.step(1 / self.fps)  # 물리엔진은 1/FPS만큼 진행한다.
        pygame.quit()


if __name__ == '__main__':
    app = App()

    # body는 물체의 질량을 정의
    # shape는 물체의 모양을 정의 (충돌감지를 위해)
    ball_radius = 30
    body = pymunk.Body()
    body.position = 400, 400
    shape = pymunk.Circle(body, ball_radius)
    shape.density = 1
    shape.friction = 1
    shape.elasticity = 0.95

    # static body는 이미 space에 정의되어 있음.
    b0 = app.space.static_body
    segment_shape = pymunk.Segment(b0, (0, 700), (800, 750), 5)
    segment_shape.elasticity = 1
    app.space.add(body, shape)
    app.space.add(segment_shape)

    app.run()
