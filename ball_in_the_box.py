from random import randint

import pymunk
from anim import App

app = App()

# 사각형의 테두리를 만든다.
pts = [(10, 10), (790, 10), (790, 790), (10, 790)]
for i in range(4):
    seg = pymunk.Segment(app.space.static_body, pts[i], pts[(i+1)%4], 2)
    seg.elasticity = 0.9
    seg.friction = 1
    app.space.add(seg)

many_balls = True
if not many_balls:
    body = pymunk.Body(mass=1, moment=10)
    body.position = 400, 200
    body.apply_impulse_at_local_point((300, 0))  # 초기 힘을 가해줌
    circle = pymunk.Circle(body, radius=20)
    circle.elasticity = 1
    circle.friction = 1
    app.space.add(body, circle)
else:
    for i in range(40):
        body = pymunk.Body(mass=1, moment=10)
        body.position = randint(40, 660), randint(40, 200)
        impulse = randint(-100, 100), randint(-100, 100)
        body.apply_impulse_at_local_point(impulse)
        circle = pymunk.Circle(body, radius=10)
        circle.elasticity = 0.999
        circle.friction = 0.5
        app.space.add(body, circle)

app.run()
