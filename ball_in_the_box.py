import pymunk
from anim import App

app = App()

pts = [(10, 10), (790, 10), (790, 790), (10, 790)]
for i in range(4):
    seg = pymunk.Segment(app.space.static_body, pts[i], pts[(i+1)%4], 2)
    seg.elasticity = 0.9
    seg.friction = 1
    app.space.add(seg)

body = pymunk.Body(mass=1, moment=10)
body.position = 400, 200
body.apply_impulse_at_local_point((300, 0))  # 초기 힘을 가해줌
circle = pymunk.Circle(body, radius=20)
circle.elasticity = 1
circle.friction = 1

app.space.add(body, circle)

app.run()
