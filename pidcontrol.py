import pymunk
import pygame
import pymunk.pygame_util


class PidApp:
    def __init__(self):
        self.seesaw_body = None
        self.seesaw = None
        self.circle = None
        self.body = None
        self.seesaw: pymunk.Segment

        pygame.init()

        self.segment = None
        self.size = (800, 800)
        self.fps = 50
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(self.size)  # 800 x 800 크기의 영역을 잡는다
        # pygame과 pymunk의 좌표계가 다른걸 일치시킨다. pygame 기준으로 바꿈. 좌상단이 0, 0
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True

        self.space = pymunk.Space()
        self.space.gravity = 0, 1000

    def setup(self):
        self.seesaw_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.seesaw_body.position = 100, 400
        self.seesaw = pymunk.Segment(self.seesaw_body, (100, 400), (700, 300), 1)
        self.seesaw.elasticity = 0.5
        self.seesaw.friction = 1

        self.body = pymunk.Body()
        self.body.position = 300, 200
        self.circle = pymunk.Circle(self.body, radius=20)
        self.circle.elasticity = 1
        self.circle.friction = 1
        self.circle.density = 1  # 이거 안쓰면 에러남. 이걸 안쓰려면 Body 정의할 때 mass, inertia를 써주어야 함.
        self.space.add(self.body, self.circle, self.seesaw_body, self.seesaw)

        self.arm_body = pymunk.Body(10)
        self.arm_body.position = 300, 300
        self.arm_shape = pymunk.Segment(self.arm_body, (-100, 0), (100, 0), 1)
        self.arm_shape.density = 1
        self.space.add(self.arm_body, self.arm_shape)

        self.fixed_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.fixed_body.position = self.arm_body.position.x-100, self.arm_body.position.y
        self.joint = pymunk.PinJoint(self.arm_body, self.fixed_body, (-100, 0), (0, 0))
        self.space.add(self.fixed_body, self.joint)

        self.upper_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.upper_body.position = self.arm_body.position.x+100, self.arm_body.position.y-100
        self.upper_joint = pymunk.PinJoint(self.arm_body, self.upper_body, (100, 0), (0, 0))
        self.space.add(self.upper_body, self.upper_joint)

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
            self.upper_body.position = (self.upper_body.position.x, self.upper_body.position.y+1)
        pygame.quit()


app = PidApp()
app.setup()
app.run()
