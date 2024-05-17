import pymunk

from anim import App

app = App()

segment = pymunk.Segment(app.space.static_body, (20, 420), (800, 320), 1)
segment.elasticity = 0.5
segment.friction = 1

body = pymunk.Body()
body.position = 400, 200
circle = pymunk.Circle(body, radius=20)
circle.elasticity = 1
circle.friction = 1
circle.density = 1  # 이거 안쓰면 에러남. 이걸 안쓰려면 Body 정의할 때 mass, inertia를 써주어야 함.

body2 = pymunk.Body()
body2.position = 500, 100
box = pymunk.Poly.create_box(body2, (50, 50))
box.density = 1
box.elasticity = 1
box.friction = 0.1

app.space.add(body, circle, segment)
app.space.add(body2, box)

app.run()
