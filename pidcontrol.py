import pymunk
import pygame
import pymunk.pygame_util

pygame.init()
size = (800, 800)  # 공간의 크기
fps = 50
clock = pygame.time.Clock()

space = pymunk.Space()  # 물리엔진 공간을 생성
space.gravity = 0, 1000

screen = pygame.display.set_mode(size)  # 800x800 크기의 pygame 영역을 잡는다.
# pygame과 pymunk의 좌표계가 다른걸 일치시킨다. pygame 기준으로 바꿈. 좌상단이 0, 0
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Space에 놓을 객체들 정의
# Ball Body와 Shape 정의
ball_body = pymunk.Body()
ball_body.position = 200, 200
ball_shape = pymunk.Circle(ball_body, radius=20)  # ball_shape에 ball_body 연결함
ball_shape.elasticity = 1
ball_shape.friction = 1
ball_shape.density = 1  # 이거 안쓰면 에러남. 이걸 안쓰려면 Body 정의할 때 mass, inertia를 써주어야 함.
space.add(ball_body, ball_shape)

# Beam Body와 Beam Shape 정의
# seesaw
beam_body = pymunk.Body()
beam_body.position = 400, 500
beam_shape = pymunk.Segment(beam_body, (-300, 0), (300, 0), 3)
beam_shape.density = 1
beam_shape.friction = 1
space.add(beam_body, beam_shape)

# Beam Center 정의
beam_center_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
beam_center_body.position = beam_body.position.x, beam_body.position.y
beam_center_joint = pymunk.PinJoint(beam_body, beam_center_body, (0, 0), (0, 0))
space.add(beam_center_body, beam_center_joint)

# Beam 오른쪽 매다는 handle 정의
handle_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
handle_body.position = beam_body.position.x + 300, beam_body.position.y - 200
handle_joint = pymunk.PinJoint(beam_body, handle_body, (300, 0), (0, 0))
space.add(handle_body, handle_joint)

running = True
prev_error = None
i_error = 0  # 오차의 누적

# 설정값
set_point = 400  # 중앙을 타겟으로 함
kp = 0.3
ki = 0.001
kd = 30

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # 그림을 그린다
    screen.fill((255, 255, 255))  # 흰색 배경
    # debug_draw를 쓰면 직접 pygame에 그리지 않아도 됨. 알아서 그려줌
    space.debug_draw(draw_options)
    pygame.display.update()
    clock.tick(fps)  # 지정한 fps가 되도록 delay를 준다.
    space.step(1 / fps)  # 물리엔진은 1/FPS만큼 진행한다.
    # 단순함을 위해 Error의 계산을 x 좌표로만 한다.
    pv = ball_body.position.x  # pv = process value
    error = set_point - pv  # set_point에서의 x 거리 차이를 error로 잡음
    d_error = 0  # 오차의 변화를 담음
    if prev_error is None:
        d_error = 0
    else:
        d_error = error - prev_error
    prev_error = error
    i_error += error
    delta = kp*error + ki*i_error + kd*d_error
    print(f"E={error}, P={kp*error} I={ki*i_error} D={kd*d_error} delta={delta}")
    # 급발진하지 않도록 제한
    if delta > 100:
        delta = 100
    elif delta < -100:
        delta = -100
    # 실제 process 수행
    handle_body.position = (handle_body.position.x, 300 + delta)

pygame.quit()

