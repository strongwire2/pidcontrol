# 작성자: 세종과학고등학교 1714 이강현
# 연락처: strongwire2@gmail.com

import pymunk
import pygame
import pymunk.pygame_util
import sys


def pid_control(kp, ki, kd, use_bump):
    pygame.init()
    size = (800, 500)  # 공간의 크기
    fps = 50
    clock = pygame.time.Clock()

    space = pymunk.Space()  # 물리엔진 공간을 생성
    space.gravity = 0, 1000

    screen = pygame.display.set_mode(size)  # 800x800 크기의 pygame 영역을 잡는다.
    pygame.display.set_caption("PID Control: Ball and Beam")
    font = pygame.font.SysFont("Courier New", 16)
    # pygame과 pymunk의 좌표계가 다른걸 일치시킨다. pygame 기준으로 바꿈. 좌상단이 0, 0
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # Space에 놓을 객체들 정의
    # Ball Body와 Shape 정의
    ball_body = pymunk.Body()
    ball_body.position = 200, 270
    ball_shape = pymunk.Circle(ball_body, radius=20)  # ball_shape에 ball_body 연결함
    ball_shape.elasticity = 0
    ball_shape.friction = 1
    ball_shape.density = 1  # 이거 안쓰면 에러남. 이걸 안쓰려면 Body 정의할 때 mass, inertia를 써주어야 함.
    space.add(ball_body, ball_shape)

    # Beam Body와 Beam Shape 정의
    beam_body = pymunk.Body()
    beam_body.position = 400, 300
    beam_shape = pymunk.Segment(beam_body, (-300, 0), (300, 0), 3)
    beam_shape.density = 1
    beam_shape.friction = 1
    space.add(beam_body, beam_shape)
    if use_bump:
        # beam의 장애물
        bump_shape = pymunk.Segment(beam_body, (-170, 0), (-170, -7), 3)
        bump_shape.density = 1
        bump_shape.friction = 1
        space.add(bump_shape)

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
    i_count = 100  # 오차를 누적할 개수
    max_output = 200  # output의 최대
    past_errors = []  # i_count개의 오차를 저장함. i_count개 이상의 오래된 것은 지움

    # 설정값
    set_point = 400  # 중앙을 타겟으로 함
    current_set_point = set_point

    print("SetPoint,Error,P,I,D,Output")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    set_point = 200
                elif event.key == pygame.K_DOWN:
                    set_point = 400
                elif event.key == pygame.K_RIGHT:
                    set_point = 600
        # 그림을 그린다
        screen.fill((255, 255, 255))  # 흰색 배경
        # debug_draw를 쓰면 직접 pygame에 그리지 않아도 됨. 알아서 그려줌
        space.debug_draw(draw_options)

        # 단순함을 위해 Error의 계산을 x 좌표로만 한다.
        pv = ball_body.position.x  # pv = process value
        error = current_set_point - pv  # set_point에서의 x 거리 차이를 error로 잡음
        # 오차의 변화를 계산
        if prev_error is None:
            d_error = 0
        else:
            d_error = error - prev_error
        prev_error = error
        # 오차의 누적을 계산
        past_errors.append(error)
        if len(past_errors) > i_count:
            past_errors.pop(0)
        i_error = sum(past_errors)
        # output 계산
        output = kp*error + ki*i_error + kd*d_error
        # CSV 출력
        print(f"{set_point},{error},{kp*error},{ki*i_error},{kd*d_error},{output}")
        # 급발진하지 않도록 제한
        if output > max_output:
            output = max_output
        elif output < -max_output:
            output = -max_output
        # 실제 process 수행
        handle_body.position = (handle_body.position.x, 100 + output)

        # set-point 점진적 증가. 한꺼번에 set-point 400 -> 600 식으로 옮기면 beam이 공을 쳐서 공중으로 날린다.
        # 실제 장치이면 점진적으로 증가하지만, 시뮬레이션에서는 갑자기 값이 증가하므로 이를 완화시킴
        if current_set_point < set_point:
            current_set_point += 1
        elif current_set_point > set_point:
            current_set_point -= 1

        # 값을 화면에 출력
        settings_display = f"SP={set_point}, Kp={kp:}, Ki={ki:}, Kd:{kd:}"
        screen.blit(font.render(settings_display, True, pygame.Color("black")), (10, 10))
        values_display = f"E={error:7.2f}, P={kp*error:7.2f}, I={ki*i_error:7.2f}, D={kd*d_error:7.2f}, output={output:7.2f}"
        screen.blit(font.render(values_display, True, pygame.Color("black")), (10, 40))

        # 최종적으로 화면 업데이트하고, 다음 스텝으로 진행
        pygame.display.update()
        clock.tick(fps)  # 지정한 fps가 되도록 delay를 준다.
        space.step(1 / fps)  # 물리엔진은 1/FPS만큼 진행한다.
    pygame.quit()


Kp = 0.3
Ki = 0.01
Kd = 60
Use_bump = False

if len(sys.argv) > 1:
    Kp = float(sys.argv[1])
if len(sys.argv) > 2:
    Ki = float(sys.argv[2])
if len(sys.argv) > 3:
    Kd = float(sys.argv[3])
if len(sys.argv) > 4:
    Use_bump = bool(sys.argv[4])

pid_control(Kp, Ki, Kd, Use_bump)
